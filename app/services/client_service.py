from app import db
from app.models.client import Client
from sqlalchemy import or_
from datetime import datetime

class ClientService:
    """Service pour la gestion des clients"""
    
    @staticmethod
    def get_all_clients(page=1, per_page=20, filters=None):
        """Récupère tous les clients avec pagination et filtres"""
        query = Client.query
        
        if filters:
            if filters.get('nom'):
                query = query.filter(Client.nom.ilike(f"%{filters['nom']}%"))
            
            if filters.get('prenom'):
                query = query.filter(Client.prenom.ilike(f"%{filters['prenom']}%"))
            
            if filters.get('email'):
                query = query.filter(Client.email.ilike(f"%{filters['email']}%"))
            
            if filters.get('ville'):
                query = query.filter(Client.ville.ilike(f"%{filters['ville']}%"))
            
            if filters.get('type_recherche'):
                query = query.filter(Client.type_recherche == filters['type_recherche'])
            
            if filters.get('is_prospect') is not None:
                query = query.filter(Client.is_prospect == filters['is_prospect'])
        
        # Tri par date de création décroissante
        query = query.order_by(Client.date_creation.desc())
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_client_by_id(client_id):
        """Récupère un client par son ID"""
        return Client.query.get_or_404(client_id)
    
    @staticmethod
    def get_client_by_email(email):
        """Récupère un client par son email"""
        return Client.query.filter_by(email=email).first()
    
    @staticmethod
    def create_client(data):
        """Crée un nouveau client"""
        client = Client(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            telephone=data.get('telephone'),
            date_naissance=data.get('date_naissance'),
            profession=data.get('profession'),
            adresse=data.get('adresse'),
            ville=data.get('ville'),
            code_postal=data.get('code_postal'),
            pays=data.get('pays', 'France'),
            budget_min=data.get('budget_min'),
            budget_max=data.get('budget_max'),
            preferences=data.get('preferences'),
            type_recherche=data.get('type_recherche'),
            notes=data.get('notes'),
            is_prospect=data.get('is_prospect', True)
        )
        
        db.session.add(client)
        db.session.commit()
        return client
    
    @staticmethod
    def update_client(client_id, data):
        """Met à jour un client existant"""
        client = ClientService.get_client_by_id(client_id)
        
        # Mise à jour des champs
        for key, value in data.items():
            if hasattr(client, key) and value is not None:
                setattr(client, key, value)
        
        db.session.commit()
        return client
    
    @staticmethod
    def delete_client(client_id):
        """Supprime un client"""
        client = ClientService.get_client_by_id(client_id)
        db.session.delete(client)
        db.session.commit()
        return True
    
    @staticmethod
    def search_clients(search_term, page=1, per_page=20):
        """Recherche de clients par terme"""
        query = Client.query.filter(
            or_(
                Client.nom.ilike(f"%{search_term}%"),
                Client.prenom.ilike(f"%{search_term}%"),
                Client.email.ilike(f"%{search_term}%"),
                Client.ville.ilike(f"%{search_term}%")
            )
        )
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_prospects():
        """Récupère tous les prospects"""
        return Client.query.filter_by(is_prospect=True).order_by(Client.date_creation.desc()).all()
    
    @staticmethod
    def get_clients():
        """Récupère tous les clients (non prospects)"""
        return Client.query.filter_by(is_prospect=False).order_by(Client.date_creation.desc()).all()
    
    @staticmethod
    def convert_prospect_to_client(client_id):
        """Convertit un prospect en client"""
        client = ClientService.get_client_by_id(client_id)
        client.is_prospect = False
        db.session.commit()
        return client
    
    @staticmethod
    def get_clients_by_type_recherche(type_recherche):
        """Récupère les clients par type de recherche"""
        return Client.query.filter_by(type_recherche=type_recherche).all()
    
    @staticmethod
    def get_statistics():
        """Récupère les statistiques des clients"""
        total_clients = Client.query.count()
        prospects = Client.query.filter_by(is_prospect=True).count()
        clients = Client.query.filter_by(is_prospect=False).count()
        
        # Par type de recherche
        clients_vente = Client.query.filter_by(type_recherche='vente').count()
        clients_location = Client.query.filter_by(type_recherche='location').count()
        clients_les_deux = Client.query.filter_by(type_recherche='les_deux').count()
        
        return {
            'total': total_clients,
            'prospects': prospects,
            'clients': clients,
            'vente': clients_vente,
            'location': clients_location,
            'les_deux': clients_les_deux
        } 