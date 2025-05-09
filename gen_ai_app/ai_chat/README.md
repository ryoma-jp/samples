# AI Chat Application

This application is an AI chat service using the OpenAI ChatGPT API. It is built with Flask and PostgreSQL, and can be easily deployed using Docker and Docker Compose.

## Features
- AI chat using the ChatGPT API
- Save, retrieve, and delete conversation threads
- Simple web UI
- Easy setup with Docker/Docker Compose

## Directory Structure
```
├── .env                # Environment variables (only dummy values are committed)
├── .env.example        # Example environment variable file
├── Dockerfile          # Dockerfile for the app
├── docker-compose.yml  # Docker Compose configuration
├── app/                # Flask app source
│   ├── main.py         # Endpoint definitions
│   ├── models.py       # DB models
│   ├── database.py     # DB initialization
│   └── ...             # Static files, templates, etc.
├── requirements.txt    # Python dependencies
└── ...
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd gen_ai_app/ai_chat
```

### 2. Create the environment variable file
```bash
cp .env.example .env
# Edit .env and set your OpenAI API key
```

### 3. Build the Docker image
```bash
docker-compose build
```

### 4. Start the application
```bash
docker-compose up
```

### 5. Access in your browser
Go to `http://localhost:5000`.

### 6. Stop the application
```bash
docker-compose down
```

## Security Notes for Production

- **Never commit real API keys or DB credentials to a public repository.**
    - Store production secrets only in `.env` (not committed), and keep only dummy values in `.env.example`.
- **Always disable debug mode (`debug=True`) in production.**
- **Error handling**
    - Do not return detailed error messages or stack traces to users.
    - Ensure logs do not contain sensitive information.
- **Authentication/Authorization and CSRF protection**
    - This app does not implement authentication or CSRF protection by default. If you deploy as a public service, implement authentication (e.g., Flask-Login) and CSRF protection.
- **SQL Injection**
    - The app uses SQLAlchemy ORM, so direct SQL injection risk is low. For future features, always use ORM for DB access.
- **Dependency management**
    - Regularly update dependencies and monitor for security advisories.

---

### Summary
This is a Flask-based AI chat app using the OpenAI ChatGPT API. For production, never commit real API keys or DB credentials, always disable debug mode, and implement authentication/CSRF protection if you deploy as a public service.
