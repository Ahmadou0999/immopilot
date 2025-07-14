from app import db, bcrypt
from app.models.agent import Agent
from flask_login import login_user, logout_user, current_user
from datetime import datetime

class AuthService:
    """Service pour l'authentification des agents"""
    
    @staticmethod
    def authenticate_user(email, password):
        """Authentifie un utilisateur"""
        agent = Agent.query.filter_by(email=email).first()
        
        if agent and agent.check_password(password):
            if agent.is_active:
                agent.update_last_login()
                return agent
            else:
                return None  # Compte désactivé
        return None
    
    @staticmethod
    def login_user(agent, remember=False):
        """Connecte un utilisateur"""
        login_user(agent, remember=remember)
        agent.update_last_login()
        return True
    
    @staticmethod
    def logout_user():
        """Déconnecte l'utilisateur actuel"""
        logout_user()
        return True
    
    @staticmethod
    def register_agent(data):
        """Enregistre un nouvel agent"""
        # Vérifier si l'email existe déjà
        if Agent.query.filter_by(email=data['email']).first():
            return None, "Cet email est déjà utilisé"
        
        # Créer le nouvel agent
        agent = Agent(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            telephone=data.get('telephone'),
            password=data['password'],
            is_admin=data.get('is_admin', False)
        )
        
        db.session.add(agent)
        db.session.commit()
        
        return agent, "Agent créé avec succès"
    
    @staticmethod
    def change_password(agent_id, current_password, new_password):
        """Change le mot de passe d'un agent"""
        agent = Agent.query.get(agent_id)
        
        if not agent:
            return False, "Agent non trouvé"
        
        if not agent.check_password(current_password):
            return False, "Mot de passe actuel incorrect"
        
        agent.set_password(new_password)
        db.session.commit()
        
        return True, "Mot de passe modifié avec succès"
    
    @staticmethod
    def reset_password_request(email):
        """Demande de réinitialisation de mot de passe"""
        agent = Agent.query.filter_by(email=email).first()
        
        if not agent:
            return False, "Aucun compte trouvé avec cet email"
        
        # Ici, vous pourriez générer un token et envoyer un email
        # Pour l'instant, on retourne juste un succès
        return True, "Email de réinitialisation envoyé"
    
    @staticmethod
    def get_user_by_id(user_id):
        """Récupère un utilisateur par son ID"""
        return Agent.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        """Récupère un utilisateur par son email"""
        return Agent.query.filter_by(email=email).first()
    
    @staticmethod
    def update_user_profile(user_id, data):
        """Met à jour le profil d'un utilisateur"""
        agent = Agent.query.get(user_id)
        
        if not agent:
            return None, "Agent non trouvé"
        
        # Mise à jour des champs autorisés
        allowed_fields = ['nom', 'prenom', 'telephone']
        for field in allowed_fields:
            if field in data and data[field]:
                setattr(agent, field, data[field])
        
        db.session.commit()
        return agent, "Profil mis à jour avec succès"
    
    @staticmethod
    def deactivate_user(user_id):
        """Désactive un utilisateur"""
        agent = Agent.query.get(user_id)
        
        if not agent:
            return False, "Agent non trouvé"
        
        agent.is_active = False
        db.session.commit()
        
        return True, "Agent désactivé avec succès"
    
    @staticmethod
    def activate_user(user_id):
        """Active un utilisateur"""
        agent = Agent.query.get(user_id)
        
        if not agent:
            return False, "Agent non trouvé"
        
        agent.is_active = True
        db.session.commit()
        
        return True, "Agent activé avec succès"
    
    @staticmethod
    def get_all_agents():
        """Récupère tous les agents"""
        return Agent.query.order_by(Agent.date_creation.desc()).all()
    
    @staticmethod
    def get_active_agents():
        """Récupère tous les agents actifs"""
        return Agent.query.filter_by(is_active=True).order_by(Agent.nom.asc()).all()
    
    @staticmethod
    def get_agents_statistics():
        """Récupère les statistiques des agents"""
        total_agents = Agent.query.count()
        active_agents = Agent.query.filter_by(is_active=True).count()
        admin_agents = Agent.query.filter_by(is_admin=True).count()
        
        return {
            'total': total_agents,
            'actifs': active_agents,
            'admins': admin_agents
        } 