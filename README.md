# 🏢 ImmoPilot - Gestion Immobilière Intelligente

**ImmoPilot** est une application web complète destinée à la gestion intelligente d'une agence immobilière, permettant aux agents immobiliers de gérer les biens, clients, ventes et locations avec une interface moderne et intuitive.

## 🎯 Fonctionnalités

### 👤 Agents Immobiliers
- **Gestion des biens** : Ajouter, modifier, supprimer des biens immobiliers
- **Gestion des clients** : Suivre les prospects et clients
- **Contrats** : Créer et gérer les contrats de vente et location
- **Visites** : Planifier et gérer les demandes de visite
- **Dashboard** : Tableau de bord avec statistiques en temps réel

### 🏠 Clients
- **Recherche de biens** : Interface de recherche avancée
- **Demandes de visite** : Formulaire de demande de visite
- **Consultation** : Détails complets des biens disponibles

### 🔧 Fonctionnalités Techniques
- **Interface responsive** : Compatible mobile et desktop
- **Recherche AJAX** : Recherche en temps réel
- **Pagination dynamique** : Navigation fluide
- **Notifications** : Système de notifications intégré
- **Sécurité** : Authentification et autorisation

## 🚀 Installation

### Prérequis
- Python 3.8+
- MySQL 8.0+
- WSL (Windows Subsystem for Linux) - recommandé

### 1. Cloner le projet
```bash
git clone <repository-url>
cd immopilot
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de la base de données
```bash
# Créer la base de données MySQL
mysql -u root -p
CREATE DATABASE immopilot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configuration des variables d'environnement
```bash
# Copier le fichier d'exemple
cp env.example .env

# Modifier le fichier .env avec vos paramètres
nano .env
```

### 6. Initialiser la base de données
```bash
# Créer les tables
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Créer un utilisateur admin
flask create-admin
```

### 7. Lancer l'application
```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 📁 Structure du projet

```
immopilot/
├── app/
│   ├── __init__.py              # Initialisation Flask
│   ├── config.py                # Configuration
│   ├── models/                  # Modèles de données
│   │   ├── agent.py
│   │   ├── bien.py
│   │   ├── client.py
│   │   ├── contrat.py
│   │   └── demande_visite.py
│   ├── services/                # Logique métier
│   │   ├── auth_service.py
│   │   ├── bien_service.py
│   │   ├── client_service.py
│   │   ├── contrat_service.py
│   │   └── visite_service.py
│   ├── forms/                   # Formulaires Flask-WTF
│   │   ├── auth_forms.py
│   │   ├── bien_forms.py
│   │   ├── client_forms.py
│   │   ├── contrat_forms.py
│   │   └── visite_forms.py
│   ├── blueprints/              # Routes organisées
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── biens.py
│   │   ├── clients.py
│   │   ├── contrats.py
│   │   └── admin.py
│   ├── templates/               # Templates HTML
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── main/
│   │   ├── biens/
│   │   ├── clients/
│   │   ├── contrats/
│   │   └── admin/
│   └── static/                  # Assets statiques
│       ├── css/
│       ├── js/
│       └── img/
├── migrations/                  # Migrations de base de données
├── tests/                       # Tests unitaires
├── app.py                       # Point d'entrée
├── requirements.txt             # Dépendances
├── env.example                  # Variables d'environnement
└── README.md                    # Documentation
```

## 🗄️ Modèles de données

### Agent
- Informations personnelles (nom, prénom, email, téléphone)
- Authentification (mot de passe hashé)
- Rôles (agent, administrateur)
- Relations avec biens et contrats

### Bien
- Caractéristiques (type, surface, pièces, etc.)
- Localisation (adresse, ville, code postal)
- Prix (vente/location)
- État et disponibilité
- Relations avec agent et contrats

### Client
- Informations personnelles
- Budget et type de recherche
- Statut (prospect/client)
- Relations avec contrats et visites

### Contrat
- Type (vente/location)
- Montants et conditions
- Dates importantes
- Statut (en cours, signé, annulé, terminé)

### DemandeVisite
- Planification (date, heure)
- Informations de contact
- Statut (en attente, confirmée, annulée, terminée)

## 🔐 Sécurité

- **Authentification** : Flask-Login avec sessions sécurisées
- **Hachage des mots de passe** : Flask-Bcrypt
- **Protection CSRF** : Flask-WTF
- **Validation des formulaires** : WTForms
- **Autorisation** : Décorateurs pour les rôles

## 🎨 Interface utilisateur

- **Framework CSS** : Bootstrap 5
- **Thème admin** : AdminLTE 3
- **JavaScript** : Vanilla JS + AJAX
- **Responsive** : Mobile-first design
- **Notifications** : Toastr pour les messages

## 📊 API Endpoints

### Public
- `GET /` - Page d'accueil
- `GET /biens` - Liste des biens
- `GET /biens/<id>` - Détail d'un bien
- `GET /search` - Recherche de biens

### Authentifiés
- `GET /dashboard` - Tableau de bord
- `POST /biens/ajouter` - Ajouter un bien
- `PUT /biens/<id>/modifier` - Modifier un bien
- `GET /clients` - Liste des clients
- `POST /contrats/ajouter` - Créer un contrat

### Administrateurs
- `GET /admin` - Dashboard admin
- `GET /admin/agents` - Gestion des agents
- `GET /admin/visites` - Gestion des visites

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_models.py
```

## 🚀 Déploiement

### Production avec Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Variables d'environnement de production
```bash
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
DATABASE_URL=mysql+pymysql://user:pass@host:port/db
```

## 🔧 Commandes utiles

```bash
# Créer un utilisateur admin
flask create-admin

# Réinitialiser la base de données
flask db downgrade base
flask db upgrade

# Générer des données de test
flask seed-data

# Vérifier la configuration
flask check-config
```

## 📝 Logs

Les logs sont configurés pour différents niveaux :
- **DEBUG** : Développement
- **INFO** : Production
- **ERROR** : Erreurs critiques

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation
- Contacter l'équipe de développement

## 🔄 Mises à jour

### Version 1.0.0
- ✅ Gestion complète des biens
- ✅ Système d'authentification
- ✅ Gestion des clients et contrats
- ✅ Interface responsive
- ✅ API REST

### Prochaines versions
- 📅 Système de notifications push
- 📅 Intégration SMS/Email
- 📅 Module de comptabilité
- 📅 Application mobile
- 📅 Intégration cartographique

---

**ImmoPilot** - Simplifiez votre gestion immobilière ! 🏠✨ 