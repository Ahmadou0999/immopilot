#!/usr/bin/env python3
"""
Script d'initialisation de la base de données ImmoPilot
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Agent, Bien, Client, Contrat, DemandeVisite
from app.models.bien import TypeBien, TypeTransaction
from app.models.demande_visite import StatutDemande

def init_database():
    """Initialise la base de données"""
    print("🚀 Initialisation de la base de données ImmoPilot...")
    
    # Créer l'application
    app = create_app()
    
    with app.app_context():
        # Créer toutes les tables
        print("📋 Création des tables...")
        db.create_all()
        print("✅ Tables créées avec succès!")
        
        # Vérifier si un admin existe déjà
        admin = Agent.query.filter_by(is_admin=True).first()
        if not admin:
            print("👤 Création de l'administrateur par défaut...")
            
            # Créer un administrateur par défaut
            admin = Agent(
                nom="Admin",
                prenom="ImmoPilot",
                email="admin@immopilot.fr",
                telephone="0123456789",
                password="admin123",
                is_admin=True
            )
            
            db.session.add(admin)
            db.session.commit()
            print("✅ Administrateur créé avec succès!")
            print("   Email: admin@immopilot.fr")
            print("   Mot de passe: admin123")
        else:
            print("ℹ️  Administrateur déjà existant")
        
        # Créer quelques données de test
        print("📊 Création de données de test...")
        
        # Vérifier s'il y a déjà des biens
        if Bien.query.count() == 0:
            # Créer quelques biens de test
            bien1 = Bien(
                reference="REF-2024-001",
                titre="Appartement T3 moderne",
                description="Bel appartement de 3 pièces dans un quartier calme, proche des transports.",
                type_bien=TypeBien.APPARTEMENT,
                type_transaction=TypeTransaction.VENTE,
                adresse="123 Rue de la Paix",
                ville="Paris",
                code_postal="75001",
                quartier="Centre",
                surface_habitable=65.0,
                nombre_pieces=3,
                nombre_chambres=2,
                nombre_salles_bain=1,
                prix_vente=450000,
                etat="excellent",
                disponible=True,
                agent_id=admin.id
            )
            
            bien2 = Bien(
                reference="REF-2024-002",
                titre="Maison avec jardin",
                description="Maison familiale avec jardin, garage et terrasse.",
                type_bien=TypeBien.MAISON,
                type_transaction=TypeTransaction.LOCATION,
                adresse="456 Avenue des Fleurs",
                ville="Lyon",
                code_postal="69001",
                quartier="Centre-ville",
                surface_habitable=120.0,
                surface_terrain=200.0,
                nombre_pieces=5,
                nombre_chambres=3,
                nombre_salles_bain=2,
                prix_location=1800,
                charges=150,
                etat="bon",
                disponible=True,
                agent_id=admin.id
            )
            
            db.session.add(bien1)
            db.session.add(bien2)
            db.session.commit()
            print("✅ 2 biens de test créés")
        
        # Vérifier s'il y a déjà des clients
        if Client.query.count() == 0:
            # Créer quelques clients de test
            client1 = Client(
                nom="Dupont",
                prenom="Jean",
                email="jean.dupont@email.com",
                telephone="0123456789",
                adresse="789 Rue du Commerce",
                ville="Paris",
                code_postal="75002",
                type_recherche="vente",
                budget_min=300000,
                budget_max=500000
            )
            
            client2 = Client(
                nom="Martin",
                prenom="Marie",
                email="marie.martin@email.com",
                telephone="0987654321",
                adresse="321 Boulevard de la République",
                ville="Lyon",
                code_postal="69002",
                type_recherche="location",
                budget_min=1000,
                budget_max=2000
            )
            
            db.session.add(client1)
            db.session.add(client2)
            db.session.commit()
            print("✅ 2 clients de test créés")
        
        print("🎉 Initialisation terminée avec succès!")
        print("\n📋 Récapitulatif:")
        print(f"   - Agents: {Agent.query.count()}")
        print(f"   - Biens: {Bien.query.count()}")
        print(f"   - Clients: {Client.query.count()}")
        print(f"   - Contrats: {Contrat.query.count()}")
        print(f"   - Demandes de visite: {DemandeVisite.query.count()}")

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        sys.exit(1) 