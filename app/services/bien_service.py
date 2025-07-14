from app import db
from app.models.bien import Bien, TypeBien, TypeTransaction
from app.models.agent import Agent
from sqlalchemy import and_, or_
from datetime import datetime
import uuid

class BienService:
    """Service pour la gestion des biens immobiliers"""
    
    @staticmethod
    def get_all_biens(page=1, per_page=12, filters=None):
        """Récupère tous les biens avec pagination et filtres"""
        query = Bien.query
        
        if filters:
            # Filtres de base
            if filters.get('type_bien'):
                query = query.filter(Bien.type_bien == TypeBien(filters['type_bien']))
            
            if filters.get('type_transaction'):
                query = query.filter(Bien.type_transaction == TypeTransaction(filters['type_transaction']))
            
            if filters.get('ville'):
                query = query.filter(Bien.ville.ilike(f"%{filters['ville']}%"))
            
            if filters.get('code_postal'):
                query = query.filter(Bien.code_postal.ilike(f"%{filters['code_postal']}%"))
            
            # Filtres de prix
            if filters.get('prix_min'):
                if filters.get('type_transaction') == TypeTransaction.VENTE.value:
                    query = query.filter(Bien.prix_vente >= filters['prix_min'])
                else:
                    query = query.filter(Bien.prix_location >= filters['prix_min'])
            
            if filters.get('prix_max'):
                if filters.get('type_transaction') == TypeTransaction.VENTE.value:
                    query = query.filter(Bien.prix_vente <= filters['prix_max'])
                else:
                    query = query.filter(Bien.prix_location <= filters['prix_max'])
            
            # Filtres de surface et pièces
            if filters.get('surface_min'):
                query = query.filter(Bien.surface_habitable >= filters['surface_min'])
            
            if filters.get('nombre_pieces_min'):
                query = query.filter(Bien.nombre_pieces >= filters['nombre_pieces_min'])
            
            # Filtre de disponibilité
            if filters.get('disponible_only', True):
                query = query.filter(Bien.disponible == True)
        
        # Tri par date de création décroissante
        query = query.order_by(Bien.date_creation.desc())
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_bien_by_id(bien_id):
        """Récupère un bien par son ID"""
        return Bien.query.get_or_404(bien_id)
    
    @staticmethod
    def get_bien_by_reference(reference):
        """Récupère un bien par sa référence"""
        return Bien.query.filter_by(reference=reference).first()
    
    @staticmethod
    def create_bien(data, agent_id):
        """Crée un nouveau bien"""
        # Générer une référence unique si non fournie
        if not data.get('reference'):
            data['reference'] = f"REF-{datetime.now().strftime('%Y%m')}-{str(uuid.uuid4())[:8].upper()}"
        
        bien = Bien(
            reference=data['reference'],
            titre=data['titre'],
            type_bien=TypeBien(data['type_bien']),
            type_transaction=TypeTransaction(data['type_transaction']),
            adresse=data['adresse'],
            ville=data['ville'],
            code_postal=data['code_postal'],
            agent_id=agent_id,
            description=data.get('description'),
            quartier=data.get('quartier'),
            surface_habitable=data.get('surface_habitable'),
            surface_terrain=data.get('surface_terrain'),
            nombre_pieces=data.get('nombre_pieces'),
            nombre_chambres=data.get('nombre_chambres'),
            nombre_salles_bain=data.get('nombre_salles_bain'),
            nombre_etages=data.get('nombre_etages'),
            etage=data.get('etage'),
            annee_construction=data.get('annee_construction'),
            classe_energie=data.get('classe_energie'),
            emission_ges=data.get('emission_ges'),
            prix_vente=data.get('prix_vente'),
            prix_location=data.get('prix_location'),
            charges=data.get('charges'),
            taxe_fonciere=data.get('taxe_fonciere'),
            etat=data.get('etat'),
            disponible=data.get('disponible', True),
            date_disponibilite=data.get('date_disponibilite'),
            equipements=data.get('equipements'),
            points_forts=data.get('points_forts'),
            points_faibles=data.get('points_faibles'),
            notes_agent=data.get('notes_agent')
        )
        
        db.session.add(bien)
        db.session.commit()
        return bien
    
    @staticmethod
    def update_bien(bien_id, data):
        """Met à jour un bien existant"""
        bien = BienService.get_bien_by_id(bien_id)
        
        # Mise à jour des champs
        for key, value in data.items():
            if hasattr(bien, key) and value is not None:
                if key in ['type_bien', 'type_transaction']:
                    # Gestion des enums
                    if key == 'type_bien':
                        setattr(bien, key, TypeBien(value))
                    elif key == 'type_transaction':
                        setattr(bien, key, TypeTransaction(value))
                else:
                    setattr(bien, key, value)
        
        bien.date_modification = datetime.utcnow()
        db.session.commit()
        return bien
    
    @staticmethod
    def delete_bien(bien_id):
        """Supprime un bien"""
        bien = BienService.get_bien_by_id(bien_id)
        db.session.delete(bien)
        db.session.commit()
        return True
    
    @staticmethod
    def search_biens(search_term, page=1, per_page=12):
        """Recherche de biens par terme"""
        query = Bien.query.filter(
            or_(
                Bien.titre.ilike(f"%{search_term}%"),
                Bien.description.ilike(f"%{search_term}%"),
                Bien.adresse.ilike(f"%{search_term}%"),
                Bien.ville.ilike(f"%{search_term}%"),
                Bien.reference.ilike(f"%{search_term}%")
            )
        ).filter(Bien.disponible == True)
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_biens_by_agent(agent_id, page=1, per_page=12):
        """Récupère les biens d'un agent"""
        query = Bien.query.filter_by(agent_id=agent_id).order_by(Bien.date_creation.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_biens_disponibles():
        """Récupère tous les biens disponibles"""
        return Bien.query.filter_by(disponible=True).order_by(Bien.date_creation.desc()).all()
    
    @staticmethod
    def get_statistics():
        """Récupère les statistiques des biens"""
        total_biens = Bien.query.count()
        biens_disponibles = Bien.query.filter_by(disponible=True).count()
        biens_vente = Bien.query.filter_by(type_transaction=TypeTransaction.VENTE).count()
        biens_location = Bien.query.filter_by(type_transaction=TypeTransaction.LOCATION).count()
        
        return {
            'total': total_biens,
            'disponibles': biens_disponibles,
            'vente': biens_vente,
            'location': biens_location
        } 