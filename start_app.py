#!/usr/bin/env python3
"""
Script de démarrage de l'application ImmoPilot
"""

import os
import sys
import subprocess
import time

def start_application():
    """Démarre l'application ImmoPilot"""
    print("🚀 Démarrage d'ImmoPilot...")
    print("=" * 40)
    
    # Vérifier que l'environnement virtuel est activé
    if not os.path.exists('immopilot_env'):
        print("❌ Environnement virtuel non trouvé. Veuillez l'activer d'abord.")
        return
    
    # Vérifier que les dépendances sont installées
    try:
        import flask
        import sqlalchemy
        print("✅ Dépendances vérifiées")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("Veuillez installer les dépendances avec: pip install -r requirements.txt")
        return
    
    # Démarrer l'application
    print("\n🌐 Démarrage du serveur Flask...")
    print("   L'application sera accessible sur: http://localhost:5000")
    print("   Appuyez sur Ctrl+C pour arrêter le serveur")
    print("\n" + "=" * 40)
    
    try:
        # Démarrer Flask en mode développement
        subprocess.run([
            sys.executable, "-m", "flask", "run", "--debug", "--host=0.0.0.0", "--port=5000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Serveur arrêté par l'utilisateur")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors du démarrage: {e}")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    start_application() 