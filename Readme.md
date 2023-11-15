# OpenAI Chat Completion API Integration

This is a simple integration of the OpenAI Chat Completion API. It is a simple Flask app that takes a prompt and returns a completion.

# Overview
This is a Flask API with an endpoint that interfaces with the OpenAI Chat Completion API. It takes a prompt and returns a completion. It takes care of all the authentication and logging of the API requests and responses. It also handles edge cases and rate limiting. The endpoint expects a JSON payload with a prompt field.

# Features
- Securely handle OpenAI API credentials and manage API interactions
- Log both the incoming requests and the API responses to a SQLite database.
- Rate limiting to prevent abuse of the OpenAI API quota.
- Any errors from the OpenAI API are caught and logged, and an appropriate response is returned to the client.
- A unique ID that can be used to identify a user and continue their chat with the OpenAI API. 

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. Create a virtual environment and install dependencies:

    ```bash
    python -m venv venv
    
    For Linux/MacOS
    source venv/bin/activate  
    
    For Windows, use 
    venv\Scripts\activate
    
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    - Set your OpenAI API key as `OPENAI_API_KEY` environment variable.
    For Windows:
    ```bash
    set OPENAI_API_KEY=YOUR_ACTUAL_API_KEY
    ```

    For Linux/macOS:
    ```bash
    export OPENAI_API_KEY=YOUR_ACTUAL_API_KEY
    ```

4. Run the Flask application:

    ```bash
    python main.py
    ```

## Usage

- **Endpoint:** `/openai-completion` (POST)
- **Request Payload:** JSON

    ```json
    {
        "user_id": "unique_user_id",
        "prompt": "Your message prompt here"
    }
    ```

- **Response:**

    - Success: 

        ```json
        {
            "user_id": "unique_user_id",
            "completion": "Generated completion text"
        }
        ```

    - Error:

        ```json
        {
            "error": "Error message details"
        }
        ```
