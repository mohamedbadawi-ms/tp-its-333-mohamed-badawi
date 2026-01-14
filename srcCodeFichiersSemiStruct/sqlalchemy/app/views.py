from flask import render_template, request, redirect, url_for, make_response, current_app
from app import app
from app import models
import jwt
import datetime
from functools import wraps

# Try to import Flasgger helpers; if unavailable, provide a no-op `swag_from` so
# the application can run without the Swagger UI installed.
try:
    from flasgger import swag_from
except ModuleNotFoundError:
    def swag_from(_=None):
        def decorator(f):
            return f
        return decorator

PASSWORD = "1234"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except Exception:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@swag_from({
    'responses': {
        200: {
            'description': 'Liste des étudiants',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nom': {'type': 'string'},
                        'addr': {'type': 'string'},
                        'pin': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def index():
    etudiants = models.get_etudiants()
    return render_template('index.html', etudiants=etudiants)


@app.route('/login', methods=['GET', 'POST'])
@swag_from({
    'parameters': [
        {
            'name': 'password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Mot de passe administrateur'
        }
    ],
    'responses': {
        200: {'description': 'Connexion réussie'},
        403: {'description': 'Mot de passe incorrect'}
    }
})
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != PASSWORD:
            return "Mot de passe incorrect", 403
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        resp = make_response(redirect(url_for('new_etudiant')))
        resp.set_cookie('token', token)
        return resp

    return render_template('login.html')


@app.route('/new')
@token_required
@swag_from({
    'security': [{'Bearer': []}],
    'responses': {
        200: {'description': 'Formulaire d\'ajout d\'étudiant'}
    }
})
def new_etudiant():
    return render_template('new.html')


@app.route('/add', methods=['POST'])
@token_required
@swag_from({
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'nom',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nom de l\'étudiant'
        },
        {
            'name': 'addr',
            'in': 'formData',
            'type': 'string',
            'description': 'Adresse de l\'étudiant'
        },
        {
            'name': 'pin',
            'in': 'formData',
            'type': 'string',
            'description': 'PIN de l\'étudiant'
        }
    ],
    'responses': {
        302: {'description': 'Étudiant ajouté, redirection vers la liste'}
    }
})
def add_etudiant():
    nom = request.form.get('nom')
    addr = request.form.get('addr')
    pin = request.form.get('pin')
    models.ajouter_etudiant(nom, addr, pin)
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@token_required
@swag_from({
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de l\'étudiant'
        },
        {
            'name': 'addr',
            'in': 'formData',
            'type': 'string',
            'description': 'Nouvelle adresse'
        },
        {
            'name': 'pin',
            'in': 'formData',
            'type': 'string',
            'description': 'Nouveau PIN'
        }
    ],
    'responses': {
        200: {'description': 'Formulaire de modification'},
        302: {'description': 'Étudiant modifié, redirection vers la liste'}
    }
})
def edit_etudiant(id):
    if request.method == 'POST':
        addr = request.form.get('addr')
        pin = request.form.get('pin')
        models.update_etudiant(id, addr, pin)
        return redirect(url_for('index'))

    etudiants = models.get_etudiants()
    etudiant = next((e for e in etudiants if e.id == id), None)
    return render_template('new.html', etudiant=etudiant)


@app.route('/delete/<int:id>', methods=['POST'])
@token_required
@swag_from({
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de l\'étudiant à supprimer'
        }
    ],
    'responses': {
        302: {'description': 'Étudiant supprimé, redirection vers la liste'}
    }
})
def delete_etudiant(id):
    models.delete_etudiant(id)
    return redirect(url_for('index'))


@app.route('/docs')
def docs():
    return redirect('/apidocs/')