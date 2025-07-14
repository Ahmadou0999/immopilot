#!/usr/bin/env python3
"""
Test spécifique de la page de détail des biens
"""

import os
import sys

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_bien_detail():
    """Test de la page de détail des biens"""
    print("🧪 Test de la page de détail des biens...")
    
    # Créer l'application
    app = create_app()
    
    with app.test_client() as client:
        # Test de la page de détail d'un bien (nécessite une connexion)
        try:
            response = client.get('/biens/1')
            print(f"Page détail bien 1: {response.status_code}")
            if response.status_code == 302:  # Redirection vers login
                print("✅ Redirection vers login (normal)")
            elif response.status_code == 200:
                print("✅ Page détail bien accessible")
            else:
                print(f"❌ Erreur: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        # Test de la page de détail d'un bien inexistant
        try:
            response = client.get('/biens/999')
            print(f"Page détail bien inexistant: {response.status_code}")
            if response.status_code == 404:
                print("✅ Erreur 404 correcte pour bien inexistant")
            else:
                print(f"⚠️  Statut inattendu: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_bien_detail() 