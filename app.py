import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
# This line tells the backend to accept requests from ANYWHERE
CORS(app, resources={r"/*": {"origins": "*"}}))

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    # We use 'room' as the unique key to find your specific text
    cursor.execute('CREATE TABLE IF NOT EXISTS clipboard (room TEXT PRIMARY KEY, content TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/get-text/<room>', methods=['GET'])
def get_text(room):
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM clipboard WHERE room = ?', (room,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"content": row[0]})
    return jsonify({"content": "", "error": "Room not found"}), 404

@app.route('/save-text', methods=['POST'])
def save_text():
    data = request.json
    room = data.get('room')
    content = data.get('content')
    
    if not room:
        return jsonify({"error": "No room code provided"}), 400

    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    # This replaces the old text if the room code already exists
    cursor.execute('INSERT OR REPLACE INTO clipboard (room, content) VALUES (?, ?)', (room, content))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5000)
