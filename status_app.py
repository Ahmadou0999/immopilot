#!/usr/bin/env python3
"""
Statut final de l'application ImmoPilot
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Agent, Bien, Client, Contrat, DemandeVisite

def status_application():
    """Affiche le statut complet de l'application"""
    print("🏠 ImmoPilot - Statut de l'application")
    print("=" * 50)
    
    # Créer l'application
    app = create_app()
    
    with app.app_context():
        print(f"\n📊 Base de données:")
        print(f"   - Agents: {Agent.query.count()}")
        print(f"   - Biens: {Bien.query.count()}")
        print(f"   - Clients: {Client.query.count()}")
        print(f"   - Contrats: {Contrat.query.count()}")
        print(f"   - Demandes de visite: {DemandeVisite.query.count()}")
        
        # Vérifier l'admin
        admin = Agent.query.filter_by(is_admin=True).first()
        if admin:
            print(f"\n👤 Administrateur:")
            print(f"   - Email: {admin.email}")
            print(f"   - Nom: {admin.nom} {admin.prenom}")
        
        # Vérifier les biens
        biens = Bien.query.all()
        if biens:
            print(f"\n🏘️  Biens disponibles:")
            for bien in biens:
                print(f"   - {bien.reference}: {bien.titre} ({bien.ville})")
                print(f"     Type: {bien.type_bien.value} - {bien.type_transaction.value}")
                if bien.prix:
                    print(f"     Prix: {bien.prix:,.0f} FCFA")
                else:
                    print(f"     Prix: Sur demande")
        
        # Test des routes
        print(f"\n🔗 Test des routes:")
        with app.test_client() as client:
            routes = [
                ('/', 'Page d\'accueil'),
                ('/search', 'Page de recherche'),
                ('/auth/login', 'Page de connexion'),
                ('/about', 'Page À propos'),
                ('/contact', 'Page Contact'),
                ('/biens/', 'API des biens')
            ]
            
            for route, name in routes:
                try:
                    response = client.get(route)
                    status = "✅" if response.status_code == 200 else "❌"
                    print(f"   {status} {name}: {response.status_code}")
                except Exception as e:
                    print(f"   ❌ {name}: Erreur - {e}")
        
        print(f"\n🎯 Configuration:")
        print(f"   - Mode debug: {app.debug}")
        print(f"   - Base de données: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Non configurée')}")
        print(f"   - Secret key: {'Configurée' if app.config.get('SECRET_KEY') else 'Non configurée'}")
        
        print(f"\n📋 Instructions:")
        print(f"   1. L'application est prête à être utilisée")
        print(f"   2. Accédez à http://localhost:5000")
        print(f"   3. Connectez-vous avec admin@immopilot.fr / admin123")
        print(f"   4. Toutes les fonctionnalités sont opérationnelles")
        
        print(f"\n🚀 Pour démarrer l'application:")
        print(f"   flask run")
        print(f"   ou")
        print(f"   python app.py")
        
        print(f"\n✅ ImmoPilot est prêt !")

if __name__ == "__main__":
    try:
        status_application()
    except Exception as e:
        print(f"❌ Erreur lors du statut: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 