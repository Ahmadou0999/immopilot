#!/usr/bin/env python3
"""
Script de gestion pour ImmoPilot
Commandes Flask personnalisées
"""

import os
import click
from flask.cli import FlaskGroup
from app import create_app, db
from app.models import Agent, Client, Bien, Contrat, DemandeVisite
from app.models.bien import TypeBien, TypeTransaction
from app.models.contrat import TypeContrat, StatutContrat
from app.models.demande_visite import StatutDemande
from datetime import datetime, date, time

app = create_app()
cli = FlaskGroup(app)

@cli.command()
def init_db():
    """Initialise la base de données"""
    click.echo("🗄️  Création des tables...")
    db.create_all()
    click.echo("✅ Tables créées avec succès !")

@cli.command()
def create_admin():
    """Crée un utilisateur administrateur"""
    click.echo("🔧 Création de l'utilisateur administrateur...")
    
    # Vérifier si un admin existe déjà
    admin = Agent.query.filter_by(is_admin=True).first()
    if admin:
        click.echo(f"✅ Administrateur existant: {admin.get_full_name()}")
        return
    
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
    
    click.echo(f"✅ Administrateur créé: {admin.get_full_name()}")
    click.echo("📧 Email: admin@immopilot.com")
    click.echo("🔑 Mot de passe: admin123")
    click.echo("⚠️  Changez ce mot de passe après la première connexion !")

@cli.command()
def seed_data():
    """Crée des données d'exemple"""
    click.echo("📊 Création des données d'exemple...")
    
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
    
    db.session.commit()
    click.echo("✅ Données d'exemple créées avec succès !")

@cli.command()
def check_config():
    """Vérifie la configuration de l'application"""
    click.echo("🔍 Vérification de la configuration...")
    
    # Vérifier les variables d'environnement
    required_vars = ['SECRET_KEY', 'MYSQL_HOST', 'MYSQL_USER', 'MYSQL_DATABASE']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        click.echo(f"❌ Variables manquantes: {', '.join(missing_vars)}")
        click.echo("📝 Créez un fichier .env basé sur env.example")
    else:
        click.echo("✅ Configuration OK")
    
    # Vérifier la connexion à la base de données
    try:
        db.engine.execute("SELECT 1")
        click.echo("✅ Connexion à la base de données OK")
    except Exception as e:
        click.echo(f"❌ Erreur de connexion à la base de données: {e}")

@cli.command()
def reset_db():
    """Réinitialise complètement la base de données"""
    if click.confirm("⚠️  Cette action supprimera toutes les données. Continuer ?"):
        click.echo("🗑️  Suppression de toutes les tables...")
        db.drop_all()
        click.echo("✅ Tables supprimées")
        
        click.echo("🗄️  Recréation des tables...")
        db.create_all()
        click.echo("✅ Tables recréées")
        
        click.echo("🔧 Création de l'administrateur...")
        create_admin()
        
        if click.confirm("Voulez-vous créer des données d'exemple ?"):
            seed_data()

if __name__ == '__main__':
    cli() 