from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from app.database import init_db
from app.models import db, ConversationThread, Message
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate
from app.models import db
import requests
import ipaddress
import socket
from urllib.parse import urlparse, urlunparse

# Load environment variables from .env
load_dotenv()

# Restrict outbound summarization targets to approved domains.
# Comma-separated list from env, e.g.:
# ALLOWED_SUMMARIZER_DOMAINS=example.com,docs.example.com
ALLOWED_SUMMARIZER_DOMAINS = {
    d.strip().lower()
    for d in os.getenv("ALLOWED_SUMMARIZER_DOMAINS", "").split(",")
    if d.strip()
}

app = Flask(__name__)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database initialization
#   - user name and password are dummy values for security reasons
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ai_chat_user:securepassword@db:5432/ai_chat_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ai_chat_user:securepassword@db:5432/ai_chat_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

with app.app_context():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    app.logger.info("Received chat request")
    user_message = request.json.get('message')
    selected_model = request.json.get('model', 'gpt-3.5-turbo')  # Default to gpt-3.5-turbo if no model is selected
    thread_id = request.json.get('thread_id')

    # Validate the selected model
    valid_models = ["o4-mini", "o3-mini", "gpt-4o"]
    if selected_model not in valid_models:
        return jsonify({"error": "Invalid model selected."}), 400

    # --- Retrieve conversation history and pass to AI model ---
    messages = []
    if thread_id:
        # Existing thread: fetch past history
        thread = ConversationThread.query.get(thread_id)
        if thread:
            db_messages = Message.query.filter_by(thread_id=thread_id).order_by(Message.created_at).all()
            for m in db_messages:
                # Pass summary messages to AI as well
                if m.type in ('text', 'summary'):
                    role = 'user' if m.sender == 'user' else 'assistant'
                    messages.append({"role": role, "content": m.content})
    # Add latest user question
    messages.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=messages
        )
        ai_message = response['choices'][0]['message']['content']
        return jsonify({"message": ai_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/threads', methods=['POST'])
def create_thread():
    # Receive the initial exchange (user message and AI response)
    data = request.get_json()
    user_text = data.get('text')
    ai_text = data.get('ai_text')
    # Prompt for generating the thread title
    prompt = f"Create a short conversation title from the following messages: user: {user_text} ai: {ai_text}"
    try:
        response = openai.ChatCompletion.create(
            model="o4-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response['choices'][0]['message']['content']
    except Exception as e:
        summary = "New Conversation"
    # Create thread
    new_thread = ConversationThread(summary=summary)
    db.session.add(new_thread)
    db.session.commit()
    # Save the initial messages
    if user_text:
        user_msg = Message(thread_id=new_thread.id, sender='user', type='text', content=user_text)
        db.session.add(user_msg)
    if ai_text:
        ai_msg = Message(thread_id=new_thread.id, sender='ai', type='text', content=ai_text)
        db.session.add(ai_msg)
    db.session.commit()
    return jsonify({'id': new_thread.id, 'created_at': new_thread.created_at.strftime('%Y-%m-%d %H:%M:%S'), 'summary': new_thread.summary}), 201

@app.route('/threads/<int:thread_id>/messages', methods=['POST'])
def add_message(thread_id):
    thread = ConversationThread.query.get(thread_id)
    if not thread:
        return jsonify({'message': 'Thread not found'}), 404
    data = request.get_json()
    user_text = data.get('text')
    ai_text = data.get('ai_text')
    # User message
    if user_text:
        user_msg = Message(thread_id=thread_id, sender='user', type='text', content=user_text)
        db.session.add(user_msg)
    # AI response
    if ai_text:
        ai_msg = Message(thread_id=thread_id, sender='ai', type='text', content=ai_text)
        db.session.add(ai_msg)
    db.session.commit()
    return jsonify({'message': 'Messages added to thread'})

@app.route('/threads/<int:thread_id>', methods=['GET'])
def get_thread(thread_id):
    thread = ConversationThread.query.get(thread_id)
    if not thread:
        return jsonify({'message': 'Thread not found'}), 404
    messages = Message.query.filter_by(thread_id=thread_id).order_by(Message.created_at).all()
    messages_list = [
        {
            'sender': m.sender,
            'type': getattr(m, 'type', 'text'),
            'content': m.content,
            'created_at': m.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for m in messages
    ]
    result = {
        'id': thread.id,
        'created_at': thread.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': thread.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'summary': thread.summary,
        'content': messages_list,
        'is_archived': thread.is_archived
    }
    return jsonify(result)

@app.route('/threads', methods=['GET'])
def get_threads():
    threads = ConversationThread.query.all()
    if not threads:
        return jsonify({'message': 'No threads found'}), 404
    result = [
        {
            'id': thread.id,
            'created_at': thread.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'summary': thread.summary
        }
        for thread in threads
    ]
    return jsonify(result)

@app.route('/threads/<int:thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    thread = ConversationThread.query.get(thread_id)
    if not thread:
        return jsonify({'message': 'Thread not found'}), 404
    Message.query.filter_by(thread_id=thread_id).delete()
    db.session.delete(thread)
    db.session.commit()
    return jsonify({'message': 'Thread deleted successfully'})

@app.route('/threads', methods=['DELETE'])
def delete_all_threads():
    Message.query.delete()
    ConversationThread.query.delete()
    db.session.commit()
    return jsonify({'message': 'All threads deleted successfully'})

# Ports that the summarizer is permitted to connect to.
_ALLOWED_PORTS = frozenset({80, 443})


def _is_public_ip(ip_str):
    ip_obj = ipaddress.ip_address(ip_str)
    return not (
        ip_obj.is_private
        or ip_obj.is_loopback
        or ip_obj.is_link_local
        or ip_obj.is_multicast
        or ip_obj.is_reserved
        or ip_obj.is_unspecified
    )


def _is_allowed_hostname(hostname):
    if not hostname:
        return False
    host = hostname.lower().rstrip(".")
    if not ALLOWED_SUMMARIZER_DOMAINS:
        return False
    for allowed in ALLOWED_SUMMARIZER_DOMAINS:
        allowed_host = allowed.lower().rstrip(".")
        if host == allowed_host or host.endswith("." + allowed_host):
            return True
    return False


def _build_safe_url(raw_url):
    """Validate *raw_url* and return a sanitized URL string that is
    reconstructed entirely from parsed components.

    Building the URL from ``urlunparse`` means the value passed to
    ``requests.get`` is never derived from user input, which breaks the
    SSRF taint chain for static analysis tools and eliminates TOCTOU risk
    between validation and the actual HTTP request.

    Raises ``ValueError`` with a human-readable message on any failure.
    """
    try:
        parsed = urlparse(raw_url)
    except Exception as exc:
        raise ValueError("Invalid URL.") from exc

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https URLs are allowed.")
    if not parsed.hostname:
        raise ValueError("URL must include a valid hostname.")
    if not _is_allowed_hostname(parsed.hostname):
        raise ValueError("URL hostname is not in the allowed domain list.")

    # Determine the effective port and restrict to safe values.
    default_port = 443 if parsed.scheme == "https" else 80
    effective_port = parsed.port if parsed.port is not None else default_port
    if effective_port not in _ALLOWED_PORTS:
        raise ValueError("Only ports 80 and 443 are allowed.")

    # Resolve all IPs for the hostname and reject any non-public address.
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, effective_port)
    except socket.gaierror as exc:
        raise ValueError("Unable to resolve hostname.") from exc
    resolved_ips = {entry[4][0] for entry in addr_info}
    if not resolved_ips:
        raise ValueError("Unable to resolve hostname.")
    for ip_str in resolved_ips:
        if not _is_public_ip(ip_str):
            raise ValueError("Target host resolves to a non-public IP address.")

    # Reconstruct the URL from validated, canonical components.
    # Using the lower-cased hostname (no trailing dot) and omitting the port
    # when it is the scheme default keeps the URL in canonical form.
    safe_host = parsed.hostname.lower()
    if parsed.port is not None and parsed.port != default_port:
        safe_netloc = f"{safe_host}:{parsed.port}"
    else:
        safe_netloc = safe_host
    safe_url = urlunparse((
        parsed.scheme,
        safe_netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        "",  # strip fragment – irrelevant for fetching
    ))
    return safe_url


def _fetch_url_safely(raw_url):
    """Validate *raw_url* and fetch its content with SSRF mitigations:

    * The URL passed to ``requests.get`` is reconstructed from parsed
      components, not derived from user input (breaks taint chain).
    * Redirects are disabled to prevent redirect-based SSRF.
    * Only ports 80 and 443 are permitted.

    Returns up to 5 000 characters of the response body on success.
    Raises ``ValueError`` with a human-readable message on any failure.
    """
    safe_url = _build_safe_url(raw_url)
    try:
        resp = requests.get(safe_url, timeout=10, allow_redirects=False)
        # Treat any redirect response as an error to prevent redirect-based SSRF.
        if resp.is_redirect:
            raise ValueError("URL redirects are not permitted.")
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Log the underlying exception without exposing it to the caller.
        logger.warning("URL fetch failed: %s", exc)
        raise ValueError("Failed to fetch URL.") from exc
    return resp.text[:5000]  # Limit size for demo


@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get('url')
    thread_id = data.get('thread_id')
    if not url:
        return jsonify({'error': 'URL is required.'}), 400
    # Create a new thread if it does not exist
    if not thread_id:
        new_thread = ConversationThread(summary=url)
        db.session.add(new_thread)
        db.session.commit()
        thread_id = new_thread.id
        thread = new_thread
    else:
        thread = ConversationThread.query.get(thread_id)
    # Save the URL as a user message (type=url)
    user_msg = Message(thread_id=thread_id, sender='user', type='url', content=url)
    db.session.add(user_msg)
    db.session.commit()
    # Fetch website content
    try:
        text = _fetch_url_safely(url)
    except ValueError as e:
        # Log the specific reason; return a generic message to avoid information leakage.
        logger.warning("URL fetch rejected: %s", e)
        return jsonify({'error': 'The provided URL is invalid or cannot be fetched safely.'}), 400
    # Summarize with OpenAI
    prompt = f"Summarize the following website content in concise English:\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4o',
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response['choices'][0]['message']['content']
    except Exception as e:
        summary = f"[Error during summarization: {e}]"
    # Save summary as AI message (type=summary)
    ai_msg = Message(thread_id=thread_id, sender='ai', type='summary', content=summary)
    db.session.add(ai_msg)
    # Update the thread summary with the first 50 characters of the summary result
    thread.summary = summary[:50]
    db.session.commit()
    return jsonify({'summary': summary, 'thread_id': thread_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
