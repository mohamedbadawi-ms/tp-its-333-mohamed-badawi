Person Service
===============

Simple Flask microservice managing persons.

Run:

- Install deps: `python -m pip install -r requirements.txt`
- Start: `python app.py` (listens on port 5001)

API:

- POST /persons
  - Body: {"name": "Alice"}
  - Response: 201 {"id": 1, "name": "Alice"}

- GET /persons/<id>
  - 200 {"id": 1, "name": "Alice"} or 404 if not found

- DELETE /persons/<id>
  - 204 on success, 404 if not found

Curl examples:

- Create:
  curl -i -X POST -H "Content-Type: application/json" -d '{"name":"Alice"}' http://localhost:5001/persons

- Get:
  curl -i http://localhost:5001/persons/1

- Delete:
  curl -i -X DELETE http://localhost:5001/persons/1
