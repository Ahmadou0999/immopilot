#!/usr/bin/env python3
"""
Script de test de connexion à la base de données
"""

import os
import pymysql
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_connection():
    """Test de connexion à MySQL"""
    print("🔍 Test de connexion à MySQL...")
    
    # Récupérer la DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        print(f"   DATABASE_URL: {database_url}")
        
        try:
            # Test de connexion avec SQLAlchemy
            from sqlalchemy import create_engine
            engine = create_engine(database_url)
            connection = engine.raw_connection()
            
            print("✅ Connexion réussie avec SQLAlchemy!")
            
            # Test de requête simple
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"   Version MySQL: {version[0]}")
            
            connection.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur de connexion SQLAlchemy: {e}")
    
    # Fallback vers PyMySQL direct
    host = os.getenv('MYSQL_HOST', 'localhost')
    port = int(os.getenv('MYSQL_PORT', 3306))
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', '')
    database = os.getenv('MYSQL_DATABASE', 'immopilot_db')
    
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   User: {user}")
    print(f"   Database: {database}")
    
    try:
        # Test de connexion directe
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        print("✅ Connexion réussie!")
        
        # Test de requête simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"   Version MySQL: {version[0]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

if __name__ == "__main__":
    test_connection() 