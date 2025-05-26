from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
CORS(app)
load_dotenv()

# Database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
print("DB URL:", DATABASE_URL)

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/write_memory', methods=['POST'])
def write_memory():
    data = request.json
    user_input = data.get("user_input")
    response = data.get("response")
    timestamp = datetime.utcnow()

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hikari_memory (
                id SERIAL PRIMARY KEY,
                user_input TEXT,
                response TEXT,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            INSERT INTO hikari_memory (user_input, response, timestamp)
            VALUES (%s, %s, %s)
        """, (user_input, response, timestamp))

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read_memory', methods=['GET'])
def read_memory():
    limit = request.args.get("limit", default=5, type=int)
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_input, response, timestamp
            FROM hikari_memory
            ORDER BY timestamp DESC
            LIMIT %s
        """, (limit,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        results = [{"user_input": r[0], "response": r[1], "timestamp": r[2].isoformat()} for r in rows]
        return jsonify(results), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
