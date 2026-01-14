
from app import app, db


if __name__ == "__main__":
	# create DB tables if they don't exist
	with app.app_context():
		db.create_all()
	app.run(debug=True)