#!/usr/bin/env python3
"""
Script de débogage pour identifier les erreurs dans l'application
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Agent, Bien, Client, Contrat, DemandeVisite
from app.models.bien import TypeBien, TypeTransaction

def debug_application():
    """Débogage de l'application"""
    print("🔍 Débogage de l'application ImmoPilot...")
    
    # Créer l'application
    app = create_app()
    
    with app.app_context():
        print("\n1️⃣ Vérification de la base de données...")
        
        # Vérifier les tables
        try:
            agent_count = Agent.query.count()
            print(f"✅ Agents: {agent_count}")
        except Exception as e:
            print(f"❌ Erreur agents: {e}")
        
        try:
            bien_count = Bien.query.count()
            print(f"✅ Biens: {bien_count}")
        except Exception as e:
            print(f"❌ Erreur biens: {e}")
        
        try:
            client_count = Client.query.count()
            print(f"✅ Clients: {client_count}")
        except Exception as e:
            print(f"❌ Erreur clients: {e}")
        
        print("\n2️⃣ Test des services...")
        
        # Test du service des biens
        try:
            from app.services.bien_service import BienService
            biens_disponibles = BienService.get_biens_disponibles()
            print(f"✅ Service biens: {len(biens_disponibles)} biens disponibles")
            
            # Test avec pagination
            biens_pages = BienService.get_all_biens(page=1, per_page=6)
            print(f"✅ Pagination biens: {biens_pages.total} biens au total")
            
        except Exception as e:
            print(f"❌ Erreur service biens: {e}")
            import traceback
            traceback.print_exc()
        
        # Test du service d'authentification
        try:
            from app.services.auth_service import AuthService
            print("✅ Service auth: OK")
        except Exception as e:
            print(f"❌ Erreur service auth: {e}")
        
        print("\n3️⃣ Test des modèles...")
        
        # Test des propriétés du modèle Bien
        try:
            if bien_count > 0:
                bien = Bien.query.first()
                print(f"✅ Premier bien: {bien.titre}")
                print(f"   Prix: {bien.prix}")
                print(f"   Type transaction: {bien.type_transaction.value}")
                print(f"   Type bien: {bien.type_bien.value}")
            else:
                print("ℹ️  Aucun bien dans la base de données")
        except Exception as e:
            print(f"❌ Erreur modèle bien: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n4️⃣ Test des routes...")
        
        # Test des routes avec le client de test
        with app.test_client() as client:
            try:
                response = client.get('/')
                print(f"✅ Route /: {response.status_code}")
            except Exception as e:
                print(f"❌ Erreur route /: {e}")
            
            try:
                response = client.get('/search')
                print(f"✅ Route /search: {response.status_code}")
            except Exception as e:
                print(f"❌ Erreur route /search: {e}")
            
            try:
                response = client.get('/auth/login')
                print(f"✅ Route /auth/login: {response.status_code}")
            except Exception as e:
                print(f"❌ Erreur route /auth/login: {e}")
        
        print("\n🎉 Débogage terminé!")

if __name__ == "__main__":
    try:
        debug_application()
    except Exception as e:
        print(f"❌ Erreur lors du débogage: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 