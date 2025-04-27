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

## Running the Application with Docker Compose

1. Ensure you have Docker and Docker Compose installed on your system.

2. Navigate to the project directory:
   ```bash
   cd gen_ai_app/ai_chat
   ```

3. Create a `.env` file with your OpenAI API key. You can use `.env.example` as a template:
   ```bash
   cp .env.example .env
   # Edit .env to add your OpenAI API key
   ```

4. Build and start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

5. Access the application in your browser at `http://localhost:5000`.

6. To stop the application, press `Ctrl+C` and run:
   ```bash
   docker-compose down
   ```

## File Structure

The project directory is organized as follows:

```
├── .env                # Environment variables (not included in the repository)
├── .env.example        # Example environment variables file
├── Dockerfile          # Dockerfile for building the application image
├── docker-compose.yml  # Docker Compose configuration file
├── README.md           # Project documentation
├── app/                # Application source code
├── requirements.txt    # Python dependencies
```

This structure ensures a clean separation of concerns and simplifies deployment using Docker Compose.

## License
This project is licensed under the MIT License.
