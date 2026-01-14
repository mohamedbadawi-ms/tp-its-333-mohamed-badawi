from flask import Flask, render_template, request, redirect, url_for
import models

app = Flask(__name__)
models.init_db()

@app.route('/')
def index():
    etudiants = models.get_etudiants()
    return render_template('index.html', etudiants=etudiants)

@app.route('/new', methods=['GET', 'POST'])
def new_etudiant():
    if request.method == 'POST':
        nom = request.form['nom']
        addr = request.form['addr']
        pin = request.form['pin']
        models.ajouter_etudiant(nom, addr, pin)
        return redirect(url_for('index'))
    return render_template('new.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_etudiant(id):
    if request.method == 'POST':
        addr = request.form['addr']
        pin = request.form['pin']
        models.update_etudiant(id, addr, pin)
        return redirect(url_for('index'))
    etudiants = models.get_etudiants()
    etudiant = next((e for e in etudiants if e[0] == id), None)
    return render_template('new.html', etudiant=etudiant)

if __name__ == "__main__":
    app.run(debug=True)