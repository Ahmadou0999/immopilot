#!/usr/bin/env python3
"""
Test simple de l'application
"""

import requests
import time

def test_simple():
    """Test simple des pages principales"""
    print("🧪 Test simple de l'application...")
    
    base_url = "http://localhost:5000"
    
    # Attendre un peu que le serveur soit prêt
    time.sleep(2)
    
    # Test de la page d'accueil
    try:
        response = requests.get(base_url, timeout=10)
        print(f"Page d'accueil: {response.status_code}")
        if response.status_code == 200:
            print("✅ Page d'accueil accessible")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test de la page de recherche
    try:
        response = requests.get(f"{base_url}/search", timeout=10)
        print(f"Page de recherche: {response.status_code}")
        if response.status_code == 200:
            print("✅ Page de recherche accessible")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test de la page de connexion
    try:
        response = requests.get(f"{base_url}/auth/login", timeout=10)
        print(f"Page de connexion: {response.status_code}")
        if response.status_code == 200:
            print("✅ Page de connexion accessible")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_simple() 