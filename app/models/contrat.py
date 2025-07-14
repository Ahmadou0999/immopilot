from app import db
from datetime import datetime
from sqlalchemy import Numeric
import enum

class TypeContrat(enum.Enum):
    VENTE = "vente"
    LOCATION = "location"

class StatutContrat(enum.Enum):
    EN_COURS = "en_cours"
    SIGNE = "signe"
    ANNULE = "annule"
    TERMINE = "termine"

class Contrat(db.Model):
    """Modèle pour les contrats de vente et location"""
    __tablename__ = 'contrats'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    type_contrat = db.Column(db.Enum(TypeContrat), nullable=False)
    statut = db.Column(db.Enum(StatutContrat), default=StatutContrat.EN_COURS)
    
    # Montants
    montant = db.Column(Numeric(10, 2), nullable=False)
    frais_agence = db.Column(Numeric(8, 2))
    charges = db.Column(Numeric(8, 2))
    caution = db.Column(Numeric(8, 2))  # Pour les locations
    
    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_signature = db.Column(db.DateTime)
    date_entree = db.Column(db.Date)  # Date d'entrée dans les lieux
    date_sortie = db.Column(db.Date)  # Date de sortie (pour locations)
    date_fin_bail = db.Column(db.Date)  # Date de fin de bail
    
    # Durée (pour locations)
    duree_bail = db.Column(db.Integer)  # en mois
    
    # Conditions
    conditions_particulieres = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    bien_id = db.Column(db.Integer, db.ForeignKey('biens.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    
    def __init__(self, numero, type_contrat, montant, client_id, bien_id, agent_id, **kwargs):
        self.numero = numero
        self.type_contrat = type_contrat
        self.montant = montant
        self.client_id = client_id
        self.bien_id = bien_id
        self.agent_id = agent_id
        
        # Attributs optionnels
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def signer(self):
        """Marque le contrat comme signé"""
        self.statut = StatutContrat.SIGNE
        self.date_signature = datetime.utcnow()
        
        # Marquer le bien comme non disponible
        if self.bien:
            self.bien.disponible = False
    
    def annuler(self):
        """Annule le contrat"""
        self.statut = StatutContrat.ANNULE
        
        # Remettre le bien comme disponible
        if self.bien:
            self.bien.disponible = True
    
    def terminer(self):
        """Termine le contrat"""
        self.statut = StatutContrat.TERMINE
        
        # Remettre le bien comme disponible
        if self.bien:
            self.bien.disponible = True
    
    def get_montant_display(self):
        """Retourne le montant formaté"""
        return f"{self.montant:,.0f} FCFA"
    
    def get_duree_display(self):
        """Retourne la durée formatée pour les locations"""
        if self.type_contrat == TypeContrat.LOCATION and self.duree_bail:
            if self.duree_bail == 1:
                return "1 mois"
            elif self.duree_bail < 12:
                return f"{self.duree_bail} mois"
            else:
                annees = self.duree_bail // 12
                mois = self.duree_bail % 12
                if mois == 0:
                    return f"{annees} an{'s' if annees > 1 else ''}"
                else:
                    return f"{annees} an{'s' if annees > 1 else ''} et {mois} mois"
        return "Non renseignée"
    
    def get_status_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        status_classes = {
            StatutContrat.EN_COURS: "badge-warning",
            StatutContrat.SIGNE: "badge-success",
            StatutContrat.ANNULE: "badge-danger",
            StatutContrat.TERMINE: "badge-secondary"
        }
        return status_classes.get(self.statut, "badge-info")
    
    def get_status_display(self):
        """Retourne le statut formaté pour l'affichage"""
        status_display = {
            StatutContrat.EN_COURS: "En cours",
            StatutContrat.SIGNE: "Signé",
            StatutContrat.ANNULE: "Annulé",
            StatutContrat.TERMINE: "Terminé"
        }
        return status_display.get(self.statut, self.statut.value.title())
    
    def get_date_debut_display(self):
        """Retourne la date de début formatée pour l'affichage"""
        if self.date_entree:
            return self.date_entree.strftime('%d/%m/%Y')
        return "Non renseignée"
    
    def get_date_fin_display(self):
        """Retourne la date de fin formatée pour l'affichage"""
        if self.type_contrat == TypeContrat.LOCATION and self.date_fin_bail:
            return self.date_fin_bail.strftime('%d/%m/%Y')
        elif self.type_contrat == TypeContrat.VENTE and self.date_signature:
            return "Vente signée"
        return "Non renseignée"
    
    def is_active(self):
        """Vérifie si le contrat est actif"""
        return self.statut in [StatutContrat.EN_COURS, StatutContrat.SIGNE]
    
    def __repr__(self):
        return f'<Contrat {self.numero}: {self.type_contrat.value}>' 