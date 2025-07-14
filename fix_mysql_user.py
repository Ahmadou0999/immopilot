#!/usr/bin/env python3
"""
Script pour corriger l'authentification MySQL
"""

import os
import pymysql
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def fix_mysql_authentication():
    """Corrige l'authentification MySQL"""
    print("🔧 Correction de l'authentification MySQL...")
    
    # Récupérer les paramètres de connexion
    host = os.getenv('MYSQL_HOST', 'localhost')
    port = int(os.getenv('MYSQL_PORT', 3306))
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', '')
    
    try:
        # Connexion sans spécifier de base de données
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        
        print("✅ Connexion à MySQL réussie!")
        
        with connection.cursor() as cursor:
            # Vérifier l'utilisateur actuel
            cursor.execute("SELECT User, Host, plugin FROM mysql.user WHERE User = %s", (user,))
            users = cursor.fetchall()
            
            if users:
                print(f"👤 Utilisateur trouvé: {user}")
                for user_info in users:
                    print(f"   Host: {user_info[1]}, Plugin: {user_info[2]}")
                    
                    # Changer le plugin d'authentification
                    if user_info[2] != 'mysql_native_password':
                        print(f"🔄 Changement du plugin d'authentification pour {user}@{user_info[1]}...")
                        
                        # Créer la base de données si elle n'existe pas
                        database = os.getenv('MYSQL_DATABASE', 'immopilot_db')
                        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                        print(f"✅ Base de données '{database}' créée ou vérifiée")
                        
                        # Changer le plugin d'authentification
                        if password:
                            cursor.execute(f"ALTER USER '{user}'@'{user_info[1]}' IDENTIFIED WITH mysql_native_password BY '{password}'")
                        else:
                            cursor.execute(f"ALTER USER '{user}'@'{user_info[1]}' IDENTIFIED WITH mysql_native_password")
                        
                        print(f"✅ Plugin d'authentification changé pour {user}@{user_info[1]}")
                    else:
                        print(f"✅ Plugin d'authentification déjà correct pour {user}@{user_info[1]}")
            
            # Appliquer les changements
            cursor.execute("FLUSH PRIVILEGES")
            print("✅ Privilèges mis à jour")
        
        connection.close()
        print("🎉 Correction terminée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        print("\n💡 Solutions alternatives:")
        print("1. Connectez-vous à MySQL en tant qu'administrateur et exécutez:")
        print(f"   ALTER USER '{user}'@'localhost' IDENTIFIED WITH mysql_native_password BY 'votre_mot_de_passe';")
        print("   FLUSH PRIVILEGES;")
        print("2. Ou créez un nouvel utilisateur:")
        print(f"   CREATE USER 'immopilot'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mot_de_passe';")
        print(f"   GRANT ALL PRIVILEGES ON immopilot_db.* TO 'immopilot'@'localhost';")
        print("   FLUSH PRIVILEGES;")
        return False

if __name__ == "__main__":
    fix_mysql_authentication() 