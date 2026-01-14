Health Service
==============

Depends on `person-service` for person existence (calls http://127.0.0.1:5001/persons/<id>) and `auth-service` for token verification.

Run:
- `python -m pip install -r requirements.txt`
- `python app.py` (listens on 5002)

Endpoints:
- GET /health/<person_id>
- POST /health/<person_id> (requires Authorization: Bearer <token>)
- PUT /health/<person_id> (requires Authorization)
- DELETE /health/<person_id> (requires Authorization)

Data stored in `data.json` mapping person_id -> health object.

Example:
- Create health: curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"weight":70}' http://localhost:5002/health/1
