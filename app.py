from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agence_immobiliere.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return "Bienvenue sur le site de l'agence immobilière."


# Table Immeuble
class Immeuble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)
    appartements = db.relationship('Appartement', backref='immeuble', lazy=True)

# Table Appartement
class Appartement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    superficie = db.Column(db.Float, nullable=False)
    nombre_chambres = db.Column(db.Integer, nullable=False)
    prix_previsionnel = db.Column(db.Float, nullable=False)
    immeuble_id = db.Column(db.Integer, db.ForeignKey('immeuble.id'), nullable=False)

# Table Client
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CIN = db.Column(db.String(20), unique=True, nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    profession = db.Column(db.String(100), nullable=True)

# Table Visite
class Visite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_visite = db.Column(db.Date, nullable=False)
    remarques = db.Column(db.Text, nullable=True)
    decision = db.Column(db.String(50), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    appartement_id = db.Column(db.Integer, db.ForeignKey('appartement.id'), nullable=False)

# Table Promesse de Vente
class PromesseVente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prix_definitif = db.Column(db.Float, nullable=False)
    avance = db.Column(db.Float, nullable=False)
    date_signature = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    appartement_id = db.Column(db.Integer, db.ForeignKey('appartement.id'), nullable=False)
    avocat_id = db.Column(db.Integer, db.ForeignKey('avocat.id'), nullable=False)

# Table Désistement
class Desistement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_desistement = db.Column(db.Date, nullable=False)
    cause = db.Column(db.Text, nullable=True)
    promesse_id = db.Column(db.Integer, db.ForeignKey('promesse_vente.id'), nullable=False)

# Table Avocat
class Avocat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    numero_autorisation = db.Column(db.String(50), unique=True, nullable=False)

# Table Contrat de Vente
class ContratVente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description_appartement = db.Column(db.Text, nullable=False)
    prix_vente = db.Column(db.Float, nullable=False)
    type_payement = db.Column(db.String(50), nullable=False)
    date_signature = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    appartement_id = db.Column(db.Integer, db.ForeignKey('appartement.id'), nullable=False)
    avocat_id = db.Column(db.Integer, db.ForeignKey('avocat.id'), nullable=False)

# Table Remise des Clés
class RemiseCles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_remise = db.Column(db.Date, nullable=False)
    proces_verbal = db.Column(db.Text, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    appartement_id = db.Column(db.Integer, db.ForeignKey('appartement.id'), nullable=False)
    contrat_id = db.Column(db.Integer, db.ForeignKey('contrat_vente.id'), nullable=False)


# Créer la base de données (définir les tables)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


# Routes
@app.route('/appartements')
def afficher_appartements():
    appartements = Appartement.query.all()
    return render_template('appartements.html', appartements=appartements)

@app.route('/ajouter_client', methods=['GET', 'POST'])
def ajouter_client():
    if request.method == 'POST':
        CIN = request.form['CIN']
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']
        telephone = request.form['telephone']
        profession = request.form.get('profession')

        client = Client(CIN=CIN, nom=nom, prenom=prenom, adresse=adresse, telephone=telephone, profession=profession)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('ajouter_client.html')

@app.route('/promesse_vente', methods=['GET', 'POST'])
def creer_promesse_vente():
    if request.method == 'POST':
        appartement_id = request.form['appartement_id']
        prix_definitif = request.form['prix_definitif']
        avance = request.form['avance']
        client_id = request.form['client_id']
        avocat_id = request.form['avocat_id']
        date_signature = request.form['date_signature']

        promesse = PromesseVente(
            appartement_id=appartement_id,
            prix_definitif=prix_definitif,
            avance=avance,
            client_id=client_id,
            avocat_id=avocat_id,
            date_signature=datetime.strptime(date_signature, '%Y-%m-%d')
        )

        db.session.add(promesse)
        db.session.commit()
        return redirect(url_for('afficher_appartements'))
    return render_template('promesse_vente_form.html')

@app.route('/desistement', methods=['GET', 'POST'])
def creer_desistement():
    if request.method == 'POST':
        promesse_id = request.form['promesse_id']
        date_desistement = request.form['date_desistement']
        cause = request.form['cause']

        desistement = Desistement(
            promesse_id=promesse_id,
            date_desistement=datetime.strptime(date_desistement, '%Y-%m-%d'),
            cause=cause
        )

        db.session.add(desistement)
        db.session.commit()
        return redirect(url_for('afficher_appartements'))
    return render_template('desistement_form.html')

@app.route('/promesse_vente')
def afficher_promesses():
    # Exemple de données ou récupérer depuis la base de données
    promesses = [
        {"id": 1, "appartement_id": 101, "prix_vente": 150000, "avance": 15000, "client_nom": "Dupont", "client_prenom": "Jean", "date_signature": "2024-11-10"},
        # Ajouter d'autres promesses ici
    ]
    return render_template('promesse_vente_form.html', promesses=promesses)

