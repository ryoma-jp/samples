from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from app.database import init_db
from app.models import db, ConversationThread
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate
from app.models import db

# Load environment variables from .env
load_dotenv()

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

    # Validate the selected model
    valid_models = ["o4-mini", "o3-mini", "gpt-4o"]
    if selected_model not in valid_models:
        return jsonify({"error": "Invalid model selected."}), 400

    try:
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=[{"role": "user", "content": user_message}]
        )
        ai_message = response['choices'][0]['message']['content']
        return jsonify({"message": ai_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/threads', methods=['POST'])
def save_thread():
    app.logger.info("Received save_thread request")
    data = request.get_json()
    if 'content' not in data or not data['content']:
        return jsonify({'message': 'Content is required'}), 400

    try:
        prompt=f"Create the conversation title from the following conversation: {data['content']}"
        response = openai.ChatCompletion.create(
            model="o4-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        app.logger.info(f"OpenAI response: {response}")
        summary = response['choices'][0]['message']['content']
        app.logger.info(f"Generated summary: {summary}")
    except Exception as e:
        return jsonify({'message': f'Error generating summary: {str(e)}'}), 500

    new_thread = ConversationThread(summary=summary, content=data['content'])
    db.session.add(new_thread)
    db.session.commit()

    # 新規スレッドIDも返す
    return jsonify({'message': 'Thread saved successfully', 'id': new_thread.id}), 201

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

@app.route('/threads/<int:thread_id>', methods=['GET'])
def get_thread(thread_id):
    thread = ConversationThread.query.get(thread_id)
    if not thread:
        return jsonify({'message': 'Thread not found'}), 404

    result = {
        'id': thread.id,
        'created_at': thread.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': thread.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'summary': thread.summary,
        'content': thread.content,
        'is_archived': thread.is_archived
    }
    return jsonify(result)

@app.route('/threads/<int:thread_id>', methods=['PUT'])
def update_thread(thread_id):
    data = request.get_json()
    thread = ConversationThread.query.get(thread_id)
    if not thread:
        return jsonify({'message': 'Thread not found'}), 404

    if 'summary' in data:
        thread.summary = data['summary']
    if 'content' in data:
        thread.content = data['content']
    if 'is_archived' in data:
        thread.is_archived = data['is_archived']

    db.session.commit()
    return jsonify({'message': 'Thread updated successfully'})

@app.route('/threads/<int:thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    thread = ConversationThread.query.get(thread_id)
    if not thread:
        return jsonify({'message': 'Thread not found'}), 404

    db.session.delete(thread)
    db.session.commit()
    return jsonify({'message': 'Thread deleted successfully'})

@app.route('/threads/new', methods=['POST'])
def create_new_thread():
    try:
        # Create a new empty thread with default values
        new_thread = ConversationThread(summary="New Conversation", content=[])  # 空リストで初期化
        db.session.add(new_thread)
        db.session.commit()
        return jsonify({
            'message': 'New thread created successfully',
            'thread': {
                'id': new_thread.id,
                'created_at': new_thread.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'summary': new_thread.summary
            }
        }), 201
    except Exception as e:
        return jsonify({'message': f'Error creating new thread: {str(e)}'}), 500

@app.route('/threads', methods=['DELETE'])
def delete_all_threads():
    try:
        num_deleted = ConversationThread.query.delete()
        db.session.commit()
        return jsonify({'message': f'All threads deleted successfully ({num_deleted} threads removed)'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error deleting all threads: {str(e)}'}), 500

# 既存スレッドにメッセージを追加するAPI
@app.route('/threads/<int:thread_id>/messages', methods=['POST'])
def add_message_to_thread(thread_id):
    thread = ConversationThread.query.get(thread_id)
    if not thread:
        return jsonify({'message': 'Thread not found'}), 404

    data = request.get_json()
    user_message = {'sender': 'user', 'text': data.get('text')}
    ai_message = {'sender': 'ai', 'text': data.get('ai_text')}
    if not isinstance(thread.content, list):
        thread.content = []
    thread.content.append(user_message)
    thread.content.append(ai_message)
    db.session.commit()
    return jsonify({'message': 'Messages added to thread'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
