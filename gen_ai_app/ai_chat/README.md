# AI Chat Application

This is a simple AI chat application that uses the ChatGPT API to provide AI-generated responses. The application is built with Flask and runs inside a Docker container.

## Features
- Chat with an AI using the ChatGPT API.
- Simple and clean user interface.
- Dockerized for easy deployment.

## Prerequisites
- Docker installed on your system.
- OpenAI API key.

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd gen_ai_app/ai_chat
   ```

2. Create a `.env` file from the provided `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Build the Docker image:
   ```bash
   docker build -t ai-chat-app .
   ```

4. Run the Docker container:
   ```bash
   docker run -p 5000:5000 --env-file .env ai-chat-app
   ```

5. Open your browser and navigate to `http://localhost:5000` to use the application.

## File Structure
```
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   ├── templates/
│   │   └── index.html
│   ├── __init__.py
│   └── main.py
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## License
This project is licensed under the MIT License.
