#!/usr/bin/env python3
"""
Script de démarrage optimisé d'ImmoPilot
"""

import os
import sys
import subprocess
import time

def start_immopilot():
    """Démarre l'application ImmoPilot"""
    print("🏠 ImmoPilot - Gestion d'Agence Immobilière")
    print("=" * 50)
    
    # Vérifier l'environnement
    if not os.path.exists('immopilot_env'):
        print("❌ Environnement virtuel non trouvé.")
        print("   Créez-le avec: python -m venv immopilot_env")
        return
    
    # Vérifier les dépendances
    try:
        import flask
        import sqlalchemy
        print("✅ Dépendances vérifiées")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("   Installez avec: pip install -r requirements.txt")
        return
    
    # Vérifier la base de données
    try:
        from app import create_app, db
        from app.models import Agent, Bien
        
        app = create_app()
        with app.app_context():
            agent_count = Agent.query.count()
            bien_count = Bien.query.count()
            print(f"✅ Base de données connectée")
            print(f"   - Agents: {agent_count}")
            print(f"   - Biens: {bien_count}")
    except Exception as e:
        print(f"❌ Erreur de base de données: {e}")
        return
    
    print("\n🚀 Démarrage du serveur...")
    print("   🌐 URL: http://localhost:5000")
    print("   👤 Admin: admin@immopilot.fr / admin123")
    print("   🛑 Arrêt: Ctrl+C")
    print("\n" + "=" * 50)
    
    try:
        # Démarrer Flask en mode développement
        subprocess.run([
            sys.executable, "-m", "flask", "run", 
            "--debug", "--host=0.0.0.0", "--port=5000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Serveur arrêté par l'utilisateur")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur de démarrage: {e}")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    start_immopilot() 