from app import db
from app.models.demande_visite import DemandeVisite, StatutDemande
from app.models.bien import Bien
from app.models.client import Client
from app.models.agent import Agent
from datetime import datetime, date
from sqlalchemy import and_

class VisiteService:
    """Service pour la gestion des demandes de visite"""
    
    @staticmethod
    def get_all_demandes(page=1, per_page=20, filters=None):
        """Récupère toutes les demandes avec pagination et filtres"""
        query = DemandeVisite.query
        
        if filters:
            if filters.get('statut'):
                query = query.filter(DemandeVisite.statut == StatutDemande(filters['statut']))
            
            if filters.get('bien_id'):
                query = query.filter(DemandeVisite.bien_id == filters['bien_id'])
            
            if filters.get('agent_id'):
                query = query.filter(DemandeVisite.agent_id == filters['agent_id'])
            
            if filters.get('date_debut'):
                query = query.filter(DemandeVisite.date_souhaitee >= filters['date_debut'])
            
            if filters.get('date_fin'):
                query = query.filter(DemandeVisite.date_souhaitee <= filters['date_fin'])
        
        # Tri par date de demande décroissante
        query = query.order_by(DemandeVisite.date_demande.desc())
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_demande_by_id(demande_id):
        """Récupère une demande par son ID"""
        return DemandeVisite.query.get_or_404(demande_id)
    
    @staticmethod
    def create_demande(data):
        """Crée une nouvelle demande de visite"""
        demande = DemandeVisite(
            date_souhaitee=data['date_souhaitee'],
            heure_souhaitee=data['heure_souhaitee'],
            nom_contact=data['nom_contact'],
            telephone_contact=data['telephone_contact'],
            bien_id=data['bien_id'],
            email_contact=data.get('email_contact'),
            nombre_personnes=data.get('nombre_personnes', 1),
            commentaires=data.get('commentaires'),
            motivation=data.get('motivation'),
            client_id=data.get('client_id')
        )
        
        db.session.add(demande)
        db.session.commit()
        return demande
    
    @staticmethod
    def update_demande(demande_id, data):
        """Met à jour une demande existante"""
        demande = VisiteService.get_demande_by_id(demande_id)
        
        # Mise à jour des champs
        for key, value in data.items():
            if hasattr(demande, key) and value is not None:
                if key == 'statut':
                    setattr(demande, key, StatutDemande(value))
                else:
                    setattr(demande, key, value)
        
        db.session.commit()
        return demande
    
    @staticmethod
    def delete_demande(demande_id):
        """Supprime une demande"""
        demande = VisiteService.get_demande_by_id(demande_id)
        db.session.delete(demande)
        db.session.commit()
        return True
    
    @staticmethod
    def confirmer_demande(demande_id, agent_id, date_confirmee=None, duree_estimee=60):
        """Confirme une demande de visite"""
        demande = VisiteService.get_demande_by_id(demande_id)
        demande.confirmer(agent_id, date_confirmee, duree_estimee)
        db.session.commit()
        return demande
    
    @staticmethod
    def annuler_demande(demande_id):
        """Annule une demande de visite"""
        demande = VisiteService.get_demande_by_id(demande_id)
        demande.annuler()
        db.session.commit()
        return demande
    
    @staticmethod
    def terminer_demande(demande_id):
        """Marque une visite comme terminée"""
        demande = VisiteService.get_demande_by_id(demande_id)
        demande.terminer()
        db.session.commit()
        return demande
    
    @staticmethod
    def get_demandes_by_bien(bien_id, page=1, per_page=20):
        """Récupère les demandes d'un bien"""
        query = DemandeVisite.query.filter_by(bien_id=bien_id).order_by(DemandeVisite.date_demande.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_demandes_by_client(client_id, page=1, per_page=20):
        """Récupère les demandes d'un client"""
        query = DemandeVisite.query.filter_by(client_id=client_id).order_by(DemandeVisite.date_demande.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_demandes_by_agent(agent_id, page=1, per_page=20):
        """Récupère les demandes d'un agent"""
        query = DemandeVisite.query.filter_by(agent_id=agent_id).order_by(DemandeVisite.date_demande.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_demandes_en_attente():
        """Récupère toutes les demandes en attente"""
        return DemandeVisite.query.filter_by(statut=StatutDemande.EN_ATTENTE).order_by(DemandeVisite.date_demande.asc()).all()
    
    @staticmethod
    def get_demandes_confirmees():
        """Récupère toutes les demandes confirmées"""
        return DemandeVisite.query.filter_by(statut=StatutDemande.CONFIRMEE).order_by(DemandeVisite.date_souhaitee.asc()).all()
    
    @staticmethod
    def get_demandes_du_jour():
        """Récupère les demandes du jour"""
        today = date.today()
        return DemandeVisite.query.filter(
            and_(
                DemandeVisite.date_souhaitee == today,
                DemandeVisite.statut.in_([StatutDemande.CONFIRMEE, StatutDemande.EN_ATTENTE])
            )
        ).order_by(DemandeVisite.heure_souhaitee.asc()).all()
    
    @staticmethod
    def get_demandes_de_la_semaine():
        """Récupère les demandes de la semaine"""
        today = date.today()
        from datetime import timedelta
        week_end = today + timedelta(days=7)
        
        return DemandeVisite.query.filter(
            and_(
                DemandeVisite.date_souhaitee >= today,
                DemandeVisite.date_souhaitee <= week_end,
                DemandeVisite.statut.in_([StatutDemande.CONFIRMEE, StatutDemande.EN_ATTENTE])
            )
        ).order_by(DemandeVisite.date_souhaitee.asc(), DemandeVisite.heure_souhaitee.asc()).all()
    
    @staticmethod
    def get_demandes_retardees():
        """Récupère les demandes en retard"""
        today = date.today()
        return DemandeVisite.query.filter(
            and_(
                DemandeVisite.date_souhaitee < today,
                DemandeVisite.statut == StatutDemande.EN_ATTENTE
            )
        ).order_by(DemandeVisite.date_souhaitee.asc()).all()
    
    @staticmethod
    def get_statistics():
        """Récupère les statistiques des demandes"""
        total_demandes = DemandeVisite.query.count()
        en_attente = DemandeVisite.query.filter_by(statut=StatutDemande.EN_ATTENTE).count()
        confirmees = DemandeVisite.query.filter_by(statut=StatutDemande.CONFIRMEE).count()
        annulees = DemandeVisite.query.filter_by(statut=StatutDemande.ANNULEE).count()
        terminees = DemandeVisite.query.filter_by(statut=StatutDemande.TERMINEE).count()
        
        # Demandes du jour
        demandes_aujourd_hui = DemandeVisite.query.filter(
            DemandeVisite.date_souhaitee == date.today()
        ).count()
        
        return {
            'total': total_demandes,
            'en_attente': en_attente,
            'confirmees': confirmees,
            'annulees': annulees,
            'terminees': terminees,
            'aujourd_hui': demandes_aujourd_hui
        } 