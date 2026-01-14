from flask import Flask, request, jsonify, g
import sqlite3
import os
import requests

DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth:5003")

app = Flask(__name__)

try:
    from flask_cors import CORS
    CORS(app)
except Exception:
    pass

def verify_token_from_request():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return False
    token = auth.split(" ", 1)[1]
    try:
        resp = requests.post(f"{AUTH_SERVICE_URL}/verify", json={"token": token})
        return resp.status_code == 200
    except Exception:
        return False

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/persons', methods=['POST'])
def create_person():
    if not verify_token_from_request():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing field: name"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO persons (name) VALUES (?)", (name,))
    db.commit()

    return jsonify({"id": cur.lastrowid, "name": name}), 201

@app.route('/persons', methods=['GET'])
def list_persons():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, name FROM persons")
    persons = [{"id": row["id"], "name": row["name"]} for row in cur.fetchall()]
    return jsonify(persons)

@app.route('/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, name FROM persons WHERE id=?", (person_id,))
    row = cur.fetchone()
    if row is None:
        return jsonify({"error": "Person not found"}), 404

    return jsonify({"id": row["id"], "name": row["name"]})

@app.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    if not verify_token_from_request():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM persons WHERE id=?", (person_id,))
    db.commit()

    if cur.rowcount == 0:
        return jsonify({"error": "Person not found"}), 404

    return "", 204

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=True)
