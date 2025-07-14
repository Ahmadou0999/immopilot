from app import db
from datetime import datetime
import enum

class StatutDemande(enum.Enum):
    EN_ATTENTE = "en_attente"
    CONFIRMEE = "confirmee"
    ANNULEE = "annulee"
    TERMINEE = "terminee"

class DemandeVisite(db.Model):
    """Modèle pour les demandes de visite"""
    __tablename__ = 'demandes_visite'
    
    id = db.Column(db.Integer, primary_key=True)
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_souhaitee = db.Column(db.Date, nullable=False)
    heure_souhaitee = db.Column(db.Time, nullable=False)
    statut = db.Column(db.Enum(StatutDemande), default=StatutDemande.EN_ATTENTE)
    
    # Informations de contact
    nom_contact = db.Column(db.String(100), nullable=False)
    telephone_contact = db.Column(db.String(20), nullable=False)
    email_contact = db.Column(db.String(120))
    
    # Détails de la demande
    nombre_personnes = db.Column(db.Integer, default=1)
    commentaires = db.Column(db.Text)
    motivation = db.Column(db.String(100))  # 'achat', 'location', 'curiosite'
    
    # Planification
    date_confirmee = db.Column(db.DateTime)
    duree_estimee = db.Column(db.Integer)  # en minutes
    notes_agent = db.Column(db.Text)
    
    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    bien_id = db.Column(db.Integer, db.ForeignKey('biens.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))
    
    def __init__(self, date_souhaitee, heure_souhaitee, nom_contact, telephone_contact, 
                 bien_id, email_contact=None, nombre_personnes=None, motivation=None, 
                 commentaires=None, **kwargs):
        self.date_souhaitee = date_souhaitee
        self.heure_souhaitee = heure_souhaitee
        self.nom_contact = nom_contact
        self.telephone_contact = telephone_contact
        self.bien_id = bien_id
        self.email_contact = email_contact
        self.nombre_personnes = nombre_personnes
        self.motivation = motivation
        self.commentaires = commentaires
        
        # Attributs optionnels
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def confirmer(self, agent_id, date_confirmee=None, duree_estimee=60):
        """Confirme la demande de visite"""
        self.statut = StatutDemande.CONFIRMEE
        self.agent_id = agent_id
        self.date_confirmee = date_confirmee or datetime.utcnow()
        self.duree_estimee = duree_estimee
    
    def annuler(self):
        """Annule la demande de visite"""
        self.statut = StatutDemande.ANNULEE
    
    def terminer(self):
        """Marque la visite comme terminée"""
        self.statut = StatutDemande.TERMINEE
    
    def get_datetime_souhaitee(self):
        """Retourne la date et heure souhaitées combinées"""
        from datetime import datetime
        return datetime.combine(self.date_souhaitee, self.heure_souhaitee)
    
    def get_heure_display(self):
        """Retourne l'heure formatée"""
        return self.heure_souhaitee.strftime("%H:%M")
    
    def get_date_display(self):
        """Retourne la date formatée"""
        return self.date_souhaitee.strftime("%d/%m/%Y")
    
    def get_status_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        status_classes = {
            StatutDemande.EN_ATTENTE: "badge-warning",
            StatutDemande.CONFIRMEE: "badge-info",
            StatutDemande.ANNULEE: "badge-danger",
            StatutDemande.TERMINEE: "badge-success"
        }
        return status_classes.get(self.statut, "badge-secondary")
    
    def is_past_due(self):
        """Vérifie si la date souhaitée est dépassée"""
        return self.date_souhaitee < datetime.now().date()
    
    def can_be_confirmed(self):
        """Vérifie si la demande peut être confirmée"""
        return (self.statut == StatutDemande.EN_ATTENTE and 
                not self.is_past_due())
    
    def __repr__(self):
        return f'<DemandeVisite {self.id}: {self.nom_contact} - {self.get_date_display()}>' 