import sqlite3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# This line is CRITICAL for the website to talk to the backend
CORS(app)

def init_db():
    # This creates the database file in the cloud environment
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS clipboard (room TEXT PRIMARY KEY, content TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "Backend is Live!"

@app.route('/get-text/<room>', methods=['GET'])
def get_text(room):
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM clipboard WHERE room = ?', (room,))
    row = cursor.fetchone()
    conn.close()
    return jsonify({"content": row[0] if row else ""})

@app.route('/save-text', methods=['POST'])
def save_text():
    data = request.json
    room = data.get('room')
    content = data.get('content')
    if not room:
        return jsonify({"error": "No room code"}), 400
        
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO clipboard (room, content) VALUES (?, ?)', (room, content))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Use the port Render expects
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
