from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
PERSON_SERVICE_URL = os.environ.get("PERSON_SERVICE_URL", "http://person:5001")
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth:5003")

try:
    from flask_cors import CORS
    CORS(app)
except Exception:
    pass

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def person_exists(person_id):
    resp = requests.get(f"{PERSON_SERVICE_URL}/persons/{person_id}")
    return resp.status_code == 200

def verify_token_from_request():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return False
    token = auth.split(" ", 1)[1]
    resp = requests.post(f"{AUTH_SERVICE_URL}/verify", json={"token": token})
    return resp.status_code == 200

@app.route("/health/<int:person_id>", methods=["GET"])
def get_health(person_id):
    if not person_exists(person_id):
        return jsonify({"error": "Person not found"}), 404
    data = load_data()
    if str(person_id) not in data:
        return jsonify({"error": "No health data"}), 404
    return jsonify(data[str(person_id)])

@app.route("/health/<int:person_id>", methods=["POST"])
def create_health(person_id):
    if not verify_token_from_request():
        return jsonify({"error": "Unauthorized"}), 401
    if not person_exists(person_id):
        return jsonify({"error": "Person not found"}), 404

    data = load_data()
    if str(person_id) in data:
        return jsonify({"error": "Health data already exists"}), 409

    body = request.get_json()
    data[str(person_id)] = body
    save_data(data)

    return jsonify({"person_id": person_id, "health": body}), 201

@app.route("/health/<int:person_id>", methods=["PUT"])
def update_health(person_id):
    if not verify_token_from_request():
        return jsonify({"error": "Unauthorized"}), 401
    if not person_exists(person_id):
        return jsonify({"error": "Person not found"}), 404

    data = load_data()
    if str(person_id) not in data:
        return jsonify({"error": "No health data"}), 404

    body = request.get_json()
    data[str(person_id)].update(body)
    save_data(data)

    return jsonify({"person_id": person_id, "health": data[str(person_id)]})

@app.route("/health/<int:person_id>", methods=["DELETE"])
def delete_health(person_id):
    if not verify_token_from_request():
        return jsonify({"error": "Unauthorized"}), 401
    if not person_exists(person_id):
        return jsonify({"error": "Person not found"}), 404

    data = load_data()
    if str(person_id) not in data:
        return jsonify({"error": "No health data"}), 404

    del data[str(person_id)]
    save_data(data)

    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
