from app import db
from app.models.contrat import Contrat, TypeContrat, StatutContrat
from app.models.client import Client
from app.models.bien import Bien
from app.models.agent import Agent
from datetime import datetime
import uuid

class ContratService:
    """Service pour la gestion des contrats"""
    
    @staticmethod
    def get_all_contrats(page=1, per_page=20, filters=None):
        """Récupère tous les contrats avec pagination et filtres"""
        query = Contrat.query
        
        if filters:
            if filters.get('type_contrat'):
                query = query.filter(Contrat.type_contrat == TypeContrat(filters['type_contrat']))
            
            if filters.get('statut'):
                query = query.filter(Contrat.statut == StatutContrat(filters['statut']))
            
            if filters.get('client_id'):
                query = query.filter(Contrat.client_id == filters['client_id'])
            
            if filters.get('bien_id'):
                query = query.filter(Contrat.bien_id == filters['bien_id'])
            
            if filters.get('agent_id'):
                query = query.filter(Contrat.agent_id == filters['agent_id'])
        
        # Tri par date de création décroissante
        query = query.order_by(Contrat.date_creation.desc())
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_contrat_by_id(contrat_id):
        """Récupère un contrat par son ID"""
        return Contrat.query.get_or_404(contrat_id)
    
    @staticmethod
    def get_contrat_by_numero(numero):
        """Récupère un contrat par son numéro"""
        return Contrat.query.filter_by(numero=numero).first()
    
    @staticmethod
    def create_contrat(data, agent_id):
        """Crée un nouveau contrat"""
        # Générer un numéro unique si non fourni
        if not data.get('numero'):
            data['numero'] = f"CON-{datetime.now().strftime('%Y%m')}-{str(uuid.uuid4())[:8].upper()}"
        
        contrat = Contrat(
            numero=data['numero'],
            type_contrat=TypeContrat(data['type_contrat']),
            montant=data['montant'],
            client_id=data['client_id'],
            bien_id=data['bien_id'],
            agent_id=agent_id,
            frais_agence=data.get('frais_agence'),
            charges=data.get('charges'),
            caution=data.get('caution'),
            date_entree=data.get('date_entree'),
            date_sortie=data.get('date_sortie'),
            date_fin_bail=data.get('date_fin_bail'),
            duree_bail=data.get('duree_bail'),
            conditions_particulieres=data.get('conditions_particulieres'),
            notes=data.get('notes')
        )
        
        db.session.add(contrat)
        db.session.commit()
        return contrat
    
    @staticmethod
    def update_contrat(contrat_id, data):
        """Met à jour un contrat existant"""
        contrat = ContratService.get_contrat_by_id(contrat_id)
        
        # Mise à jour des champs
        for key, value in data.items():
            if hasattr(contrat, key) and value is not None:
                if key in ['type_contrat', 'statut']:
                    # Gestion des enums
                    if key == 'type_contrat':
                        setattr(contrat, key, TypeContrat(value))
                    elif key == 'statut':
                        setattr(contrat, key, StatutContrat(value))
                else:
                    setattr(contrat, key, value)
        
        db.session.commit()
        return contrat
    
    @staticmethod
    def delete_contrat(contrat_id):
        """Supprime un contrat"""
        contrat = ContratService.get_contrat_by_id(contrat_id)
        db.session.delete(contrat)
        db.session.commit()
        return True
    
    @staticmethod
    def signer_contrat(contrat_id):
        """Marque un contrat comme signé"""
        contrat = ContratService.get_contrat_by_id(contrat_id)
        contrat.signer()
        return contrat
    
    @staticmethod
    def annuler_contrat(contrat_id):
        """Annule un contrat"""
        contrat = ContratService.get_contrat_by_id(contrat_id)
        contrat.annuler()
        return contrat
    
    @staticmethod
    def terminer_contrat(contrat_id):
        """Termine un contrat"""
        contrat = ContratService.get_contrat_by_id(contrat_id)
        contrat.terminer()
        return contrat
    
    @staticmethod
    def get_contrats_by_client(client_id, page=1, per_page=20):
        """Récupère les contrats d'un client"""
        query = Contrat.query.filter_by(client_id=client_id).order_by(Contrat.date_creation.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_contrats_by_bien(bien_id, page=1, per_page=20):
        """Récupère les contrats d'un bien"""
        query = Contrat.query.filter_by(bien_id=bien_id).order_by(Contrat.date_creation.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_contrats_by_agent(agent_id, page=1, per_page=20):
        """Récupère les contrats d'un agent"""
        query = Contrat.query.filter_by(agent_id=agent_id).order_by(Contrat.date_creation.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_contrats_actifs():
        """Récupère tous les contrats actifs"""
        return Contrat.query.filter(
            Contrat.statut.in_([StatutContrat.EN_COURS, StatutContrat.SIGNE])
        ).order_by(Contrat.date_creation.desc()).all()
    
    @staticmethod
    def get_contrats_par_type():
        """Récupère les contrats groupés par type"""
        ventes = Contrat.query.filter_by(type_contrat=TypeContrat.VENTE).count()
        locations = Contrat.query.filter_by(type_contrat=TypeContrat.LOCATION).count()
        
        return {
            'ventes': ventes,
            'locations': locations
        }
    
    @staticmethod
    def get_contrats_par_statut():
        """Récupère les contrats groupés par statut"""
        en_cours = Contrat.query.filter_by(statut=StatutContrat.EN_COURS).count()
        signes = Contrat.query.filter_by(statut=StatutContrat.SIGNE).count()
        annules = Contrat.query.filter_by(statut=StatutContrat.ANNULE).count()
        termines = Contrat.query.filter_by(statut=StatutContrat.TERMINE).count()
        
        return {
            'en_cours': en_cours,
            'signes': signes,
            'annules': annules,
            'termines': termines
        }
    
    @staticmethod
    def get_statistics():
        """Récupère les statistiques des contrats"""
        total_contrats = Contrat.query.count()
        contrats_actifs = Contrat.query.filter(
            Contrat.statut.in_([StatutContrat.EN_COURS, StatutContrat.SIGNE])
        ).count()
        
        # Montant total des contrats signés
        montant_total = db.session.query(db.func.sum(Contrat.montant)).filter(
            Contrat.statut == StatutContrat.SIGNE
        ).scalar() or 0
        
        return {
            'total': total_contrats,
            'actifs': contrats_actifs,
            'montant_total': float(montant_total)
        } 