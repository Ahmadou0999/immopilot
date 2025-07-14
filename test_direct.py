#!/usr/bin/env python3
"""
Test direct de l'application Flask
"""

import os
import sys

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_direct():
    """Test direct de l'application"""
    print("🧪 Test direct de l'application Flask...")
    
    # Créer l'application
    app = create_app()
    
    with app.test_client() as client:
        # Test de la page d'accueil
        try:
            response = client.get('/')
            print(f"Page d'accueil: {response.status_code}")
            if response.status_code == 200:
                print("✅ Page d'accueil accessible")
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(f"Contenu: {response.data[:200]}...")
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        # Test de la page de recherche
        try:
            response = client.get('/search')
            print(f"Page de recherche: {response.status_code}")
            if response.status_code == 200:
                print("✅ Page de recherche accessible")
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(f"Contenu: {response.data[:200]}...")
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        # Test de la page de connexion
        try:
            response = client.get('/auth/login')
            print(f"Page de connexion: {response.status_code}")
            if response.status_code == 200:
                print("✅ Page de connexion accessible")
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(f"Contenu: {response.data[:200]}...")
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_direct() 