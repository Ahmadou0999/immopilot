from app import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return Agent.query.get(int(user_id))

class Agent(db.Model, UserMixin):
    """Modèle pour les agents immobiliers"""
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    derniere_connexion = db.Column(db.DateTime)
    
    # Relations
    biens = db.relationship('Bien', backref='agent', lazy='dynamic', cascade='all, delete-orphan')
    contrats = db.relationship('Contrat', backref='agent', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, nom, prenom, email, password, telephone=None, is_admin=False):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.is_admin = is_admin
        self.set_password(password)
    
    def set_password(self, password):
        """Hash le mot de passe"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Retourne le nom complet"""
        return f"{self.prenom} {self.nom}"
    
    def update_last_login(self):
        """Met à jour la dernière connexion"""
        self.derniere_connexion = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Agent {self.get_full_name()}>' 