import sqlite3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CRITICAL: This allows your GitHub website to talk to this server
CORS(app)

def init_db():
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS clipboard (room TEXT PRIMARY KEY, content TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "Cloud Clipboard Backend is Online!"

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
        return jsonify({"error": "Missing room code"}), 400
    
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO clipboard (room, content) VALUES (?, ?)', (room, content))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Render provides a specific PORT; this line grabs it automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
