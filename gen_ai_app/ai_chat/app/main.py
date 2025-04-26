from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
