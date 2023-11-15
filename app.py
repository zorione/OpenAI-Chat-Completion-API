import os
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from openai import OpenAI
import sqlite3
import uuid
from datetime import datetime
import openai

app = Flask(__name__)
api_key = os.environ.get('OPENAI_API_KEY')

conn = sqlite3.connect('chat_logs.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chat_logs 
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id TEXT,
             timestamp TEXT,
             request TEXT,
             response TEXT)''')
conn.commit()

def generate_user_id():
    return str(uuid.uuid4())

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

@app.route('/openai-completion', methods=['POST'])
@limiter.limit("2 per minute")
def chat():
    data = request.get_json()
    user_id = data.get('user_id')
    prompt = data.get('prompt')

    if user_id is None:
        user_id = generate_user_id()

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=100
        )

        completion = response.choices[0]
        message_content = completion.message.content

        timestamp = datetime.now().isoformat()
        c.execute("INSERT INTO chat_logs (user_id, timestamp, request, response) VALUES (?, ?, ?, ?)",
                  (user_id, timestamp, prompt, message_content))
        conn.commit()

        return jsonify({'user_id': user_id, 'completion': message_content}), 200
    
    except openai.error.OpenAIError as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500

    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
