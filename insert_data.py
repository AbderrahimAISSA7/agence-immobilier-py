from app import app, db
from app import Immeuble, Appartement, Client, Visite, PromesseVente, Desistement, Avocat, ContratVente, RemiseCles
from datetime import date
# Ajout des données dans la base de données
with app.app_context():
    # Insertion d'un immeuble
    immeuble = Immeuble(nom='Immeuble 1', adresse='123 Rue de Paris')
    db.session.add(immeuble)
    db.session.commit()

    # Insertion d'un appartement
    appartement = Appartement(numero=101, superficie=75.0, nombre_chambres=3, prix_previsionnel=150000.0, immeuble_id=immeuble.id)
    db.session.add(appartement)
    db.session.commit()

    # Insertion d'un client
    client = Client(CIN='ABC123', nom='Dupont', prenom='Jean', adresse='45 Rue des Champs', telephone='0123456789', profession='Ingénieur')
    db.session.add(client)
    db.session.commit()

    # Insertion d'une visite
    visite = Visite(date_visite=date.today(), remarques='Très bon état', decision='Acheter', client_id=client.id, appartement_id=appartement.id)
    db.session.add(visite)
    db.session.commit()

    # Insertion d'un avocat
    avocat = Avocat(nom='Martin', prenom='Pierre', adresse='10 Rue des Avocats', telephone='0987654321', numero_autorisation='AV123')
    db.session.add(avocat)
    db.session.commit()

    # Insertion d'une promesse de vente
    promesse = PromesseVente(prix_definitif=145000.0, avance=5000.0, date_signature=date.today(), client_id=client.id, appartement_id=appartement.id, avocat_id=avocat.id)
    db.session.add(promesse)
    db.session.commit()

    # Insertion d'un désistement
    desistement = Desistement(date_desistement=date.today(), cause='Financement impossible', promesse_id=promesse.id)
    db.session.add(desistement)
    db.session.commit()

    # Insertion d'un contrat de vente
    contrat = ContratVente(description_appartement='Appartement avec 3 chambres et 1 salle de bain', prix_vente=145000.0, type_payement='Prêt immobilier', date_signature=date.today(), client_id=client.id, appartement_id=appartement.id, avocat_id=avocat.id)
    db.session.add(contrat)
    db.session.commit()

    # Insertion d'une remise des clés
    remise_cles = RemiseCles(date_remise=date.today(), proces_verbal='Remis en bon état', client_id=client.id, appartement_id=appartement.id, contrat_id=contrat.id)
    db.session.add(remise_cles)
    db.session.commit()

    print("Données insérées avec succès.")