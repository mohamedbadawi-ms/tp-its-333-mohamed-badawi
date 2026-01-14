from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET = "dev-secret"
TOKEN_TTL_MINUTES = 60

VALID_USER = {"username": "momo", "password": "1234"}

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if username == VALID_USER["username"] and password == VALID_USER["password"]:
        payload = {
            "sub": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_TTL_MINUTES)
        }
        token = jwt.encode(payload, SECRET, algorithm='HS256')
        return jsonify({"token": token})
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/verify', methods=['POST'])
def verify():
    token = request.get_json().get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 400
    try:
        jwt.decode(token, SECRET, algorithms=["HS256"])
        return jsonify({"valid": True}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
