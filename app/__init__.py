from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()
mail = Mail()
# Initialisation de Flask-Admin (ne pas utiliser le nom 'admin' pour éviter le conflit)
admin = Admin(name='flaskadmin', template_mode='bootstrap4', url='/flaskadmin')

def create_app(config_class=None):
    """Factory pattern pour créer l'application Flask"""
    app = Flask(__name__)
    
    # Configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object('app.config.Config')
    
    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    
    # Configuration du login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'
    
    # Initialisation de Flask-Admin
    admin.init_app(app)
    
    # Import et enregistrement des blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    from app.blueprints.biens import biens_bp
    from app.blueprints.clients import clients_bp
    from app.blueprints.contrats import contrats_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(biens_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(contrats_bp)
    app.register_blueprint(admin_bp, name='admin_bp')
    
    # Configuration des vues admin
    from app.models import Agent, Bien, Client, Contrat
    from app.admin_views import BienAdminView, DemandeVisiteAdminView
    
    admin.add_view(ModelView(Agent, db.session, name='Agents'))
    admin.add_view(BienAdminView(Bien, db.session, name='Biens'))
    admin.add_view(ModelView(Client, db.session, name='Clients'))
    admin.add_view(ModelView(Contrat, db.session, name='Contrats'))
    admin.add_view(DemandeVisiteAdminView(name='Demandes de visite', endpoint='demandevisiteadmin'))
    
    # Création des tables si elles n'existent pas (optionnel)
    # with app.app_context():
    #     db.create_all()
    
    return app 