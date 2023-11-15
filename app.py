# Import necessary modules and libraries
from flask import Flask, request, jsonify
from openai import OpenAI
import sqlite3
import uuid
from datetime import datetime
import openai

# Initialize the Flask application
app = Flask(__name__)

# Define the OpenAI API key (replace 'OPENAI_KEY' with the actual API key)
api_key = 'OPENAI_KEY'

# Connect to the SQLite database and create a cursor
conn = sqlite3.connect('chat_logs.db', check_same_thread=False)
c = conn.cursor()

# Create the chat_logs table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS chat_logs 
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id TEXT,
             timestamp TEXT,
             request TEXT,
             response TEXT)''')
conn.commit()

# Function to generate a unique user ID using UUID
def generate_user_id():
    return str(uuid.uuid4())

# The '/chat' endpoint for handling chat requests
@app.route('/chat', methods=['POST'])
def chat():
    # Get JSON data from the incoming request
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')

    # Generate a user ID if not provided in the request
    if user_id is None:
        user_id = generate_user_id()

    try:
        # Initialize the OpenAI client
        client = OpenAI(api_key=api_key)

        # Make a chat completion request to the OpenAI API
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": message}
            ],
            model="gpt-3.5-turbo",
            max_tokens=100
        )

        # Extract the completed message from the response
        completion = response.choices[0]
        message_content = completion.message.content

        # Record the chat request and response in the database
        timestamp = datetime.now().isoformat()
        c.execute("INSERT INTO chat_logs (user_id, timestamp, request, response) VALUES (?, ?, ?, ?)",
                  (user_id, timestamp, message, message_content))
        conn.commit()

        # Return the user ID and completed message as a JSON response
        return jsonify({'user_id': user_id, 'completion': message_content}), 200

    except openai.error.OpenAIError as e:
        # Handling OpenAI errors and return an appropriate JSON response
        error_message = str(e)
        return jsonify({'error': error_message}), 500

    except Exception as e:
        # Handing other unexpected errors and return an appropriate JSON response
        error_message = str(e)
        return jsonify({'error': error_message}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)