from app import db


class Etudiant(db.Model):
    __tablename__ = 'etudiants'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), nullable=False)
    addr = db.Column(db.Text)
    pin = db.Column(db.String(20))


def get_etudiants():
    return Etudiant.query.all()


def ajouter_etudiant(nom, addr, pin):
    e = Etudiant(nom=nom, addr=addr, pin=pin)
    db.session.add(e)
    db.session.commit()


def update_etudiant(id, addr, pin):
    e = Etudiant.query.get(id)
    if not e:
        return False
    e.addr = addr
    e.pin = pin
    db.session.commit()
    return True


def delete_etudiant(id):
    e = Etudiant.query.get(id)
    if not e:
        return False
    db.session.delete(e)
    db.session.commit()
    return True