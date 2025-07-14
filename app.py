#!/usr/bin/env python3
"""
ImmoPilot - Application de gestion immobilière
Lancement de l'application Flask
"""

import os
from app import create_app
from app.config import config

# Créer l'application Flask
app = create_app()

if __name__ == '__main__':
    # Configuration du port et de l'hôte
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🚀 Démarrage d'ImmoPilot...")
    print(f"📍 Serveur accessible sur: http://{host}:{port}")
    print(f"🔧 Mode debug: {'Activé' if debug else 'Désactivé'}")
    
    # Lancer l'application
    app.run(host=host, port=port, debug=debug) 