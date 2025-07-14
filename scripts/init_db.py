#!/usr/bin/env python3
"""
Script d'initialisation de la base de données ImmoPilot
"""

import os
import sys
from datetime import datetime, date, time

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Agent, Client, Bien, Contrat, DemandeVisite
from app.models.bien import TypeBien, TypeTransaction
from app.models.contrat import TypeContrat, StatutContrat
from app.models.demande_visite import StatutDemande

def create_admin_user():
    """Crée un utilisateur administrateur"""
    print("🔧 Création de l'utilisateur administrateur...")
    
    # Vérifier si un admin existe déjà
    admin = Agent.query.filter_by(is_admin=True).first()
    if admin:
        print(f"✅ Administrateur existant: {admin.get_full_name()}")
        return admin
    
    # Créer un nouvel admin
    admin = Agent(
        nom="Admin",
        prenom="ImmoPilot",
        email="admin@immopilot.com",
        telephone="0123456789",
        password="admin123",
        is_admin=True
    )
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"✅ Administrateur créé: {admin.get_full_name()}")
    print("📧 Email: admin@immopilot.com")
    print("🔑 Mot de passe: admin123")
    print("⚠️  Changez ce mot de passe après la première connexion !")
    
    return admin

def create_sample_data():
    """Crée des données d'exemple"""
    print("📊 Création des données d'exemple...")
    
    # Créer des agents
    agents = []
    agent_data = [
        {"nom": "Dupont", "prenom": "Marie", "email": "marie.dupont@immopilot.com", "telephone": "0123456781"},
        {"nom": "Martin", "prenom": "Pierre", "email": "pierre.martin@immopilot.com", "telephone": "0123456782"},
        {"nom": "Bernard", "prenom": "Sophie", "email": "sophie.bernard@immopilot.com", "telephone": "0123456783"}
    ]
    
    for data in agent_data:
        agent = Agent(
            nom=data["nom"],
            prenom=data["prenom"],
            email=data["email"],
            telephone=data["telephone"],
            password="agent123"
        )
        agents.append(agent)
        db.session.add(agent)
    
    # Créer des clients
    clients = []
    client_data = [
        {"nom": "Durand", "prenom": "Jean", "email": "jean.durand@email.com", "telephone": "0123456791", "budget_min": 200000, "budget_max": 350000, "type_recherche": "vente"},
        {"nom": "Leroy", "prenom": "Anne", "email": "anne.leroy@email.com", "telephone": "0123456792", "budget_min": 800, "budget_max": 1200, "type_recherche": "location"},
        {"nom": "Moreau", "prenom": "Paul", "email": "paul.moreau@email.com", "telephone": "0123456793", "budget_min": 150000, "budget_max": 250000, "type_recherche": "les_deux"}
    ]
    
    for data in client_data:
        client = Client(
            nom=data["nom"],
            prenom=data["prenom"],
            email=data["email"],
            telephone=data["telephone"],
            budget_min=data["budget_min"],
            budget_max=data["budget_max"],
            type_recherche=data["type_recherche"],
            ville="Paris",
            code_postal="75001"
        )
        clients.append(client)
        db.session.add(client)
    
    # Créer des biens
    biens = []
    bien_data = [
        {
            "reference": "REF-202412-001",
            "titre": "Appartement T3 moderne",
            "type_bien": TypeBien.APPARTEMENT,
            "type_transaction": TypeTransaction.VENTE,
            "adresse": "15 rue de la Paix",
            "ville": "Paris",
            "code_postal": "75001",
            "surface_habitable": 65.0,
            "nombre_pieces": 3,
            "nombre_chambres": 2,
            "prix_vente": 450000,
            "description": "Bel appartement rénové avec vue dégagée"
        },
        {
            "reference": "REF-202412-002",
            "titre": "Maison avec jardin",
            "type_bien": TypeBien.MAISON,
            "type_transaction": TypeTransaction.VENTE,
            "adresse": "25 avenue des Champs",
            "ville": "Lyon",
            "code_postal": "69001",
            "surface_habitable": 120.0,
            "surface_terrain": 300.0,
            "nombre_pieces": 5,
            "nombre_chambres": 3,
            "prix_vente": 650000,
            "description": "Maison familiale avec grand jardin"
        },
        {
            "reference": "REF-202412-003",
            "titre": "Studio meublé",
            "type_bien": TypeBien.APPARTEMENT,
            "type_transaction": TypeTransaction.LOCATION,
            "adresse": "8 rue du Commerce",
            "ville": "Marseille",
            "code_postal": "13001",
            "surface_habitable": 25.0,
            "nombre_pieces": 1,
            "prix_location": 850,
            "description": "Studio meublé idéal pour étudiant"
        }
    ]
    
    for i, data in enumerate(bien_data):
        bien = Bien(
            reference=data["reference"],
            titre=data["titre"],
            type_bien=data["type_bien"],
            type_transaction=data["type_transaction"],
            adresse=data["adresse"],
            ville=data["ville"],
            code_postal=data["code_postal"],
            surface_habitable=data.get("surface_habitable"),
            surface_terrain=data.get("surface_terrain"),
            nombre_pieces=data.get("nombre_pieces"),
            nombre_chambres=data.get("nombre_chambres"),
            prix_vente=data.get("prix_vente"),
            prix_location=data.get("prix_location"),
            description=data.get("description"),
            agent_id=agents[i % len(agents)].id
        )
        biens.append(bien)
        db.session.add(bien)
    
    # Créer des contrats
    contrat_data = [
        {
            "numero": "CON-202412-001",
            "type_contrat": TypeContrat.VENTE,
            "montant": 450000,
            "statut": StatutContrat.SIGNE
        },
        {
            "numero": "CON-202412-002",
            "type_contrat": TypeContrat.LOCATION,
            "montant": 850,
            "statut": StatutContrat.EN_COURS
        }
    ]
    
    for i, data in enumerate(contrat_data):
        contrat = Contrat(
            numero=data["numero"],
            type_contrat=data["type_contrat"],
            montant=data["montant"],
            statut=data["statut"],
            client_id=clients[i].id,
            bien_id=biens[i].id,
            agent_id=agents[i % len(agents)].id
        )
        db.session.add(contrat)
    
    # Créer des demandes de visite
    demande_data = [
        {
            "date_souhaitee": date.today(),
            "heure_souhaitee": time(14, 0),
            "nom_contact": "Jean Durand",
            "telephone_contact": "0123456791",
            "motivation": "achat"
        },
        {
            "date_souhaitee": date.today(),
            "heure_souhaitee": time(16, 0),
            "nom_contact": "Anne Leroy",
            "telephone_contact": "0123456792",
            "motivation": "location"
        }
    ]
    
    for i, data in enumerate(demande_data):
        demande = DemandeVisite(
            date_souhaitee=data["date_souhaitee"],
            heure_souhaitee=data["heure_souhaitee"],
            nom_contact=data["nom_contact"],
            telephone_contact=data["telephone_contact"],
            motivation=data["motivation"],
            bien_id=biens[i].id,
            client_id=clients[i].id
        )
        db.session.add(demande)
    
    db.session.commit()
    print("✅ Données d'exemple créées avec succès !")

def main():
    """Fonction principale"""
    print("🚀 Initialisation de la base de données ImmoPilot")
    print("=" * 50)
    
    # Créer l'application Flask
    app = create_app()
    
    with app.app_context():
        # Créer les tables
        print("🗄️  Création des tables...")
        db.create_all()
        print("✅ Tables créées avec succès !")
        
        # Créer l'admin
        admin = create_admin_user()
        
        # Demander si on veut créer des données d'exemple
        response = input("\n📊 Voulez-vous créer des données d'exemple ? (o/n): ").lower()
        if response in ['o', 'oui', 'y', 'yes']:
            create_sample_data()
        
        print("\n🎉 Initialisation terminée !")
        print("🌐 Lancez l'application avec: python app.py")
        print("🔗 Accédez à: http://localhost:5000")

if __name__ == '__main__':
    main() 