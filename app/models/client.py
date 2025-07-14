from app import db
from datetime import datetime
from sqlalchemy import Numeric

class Client(db.Model):
    """Modèle pour les clients"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20))
    date_naissance = db.Column(db.Date)
    profession = db.Column(db.String(100))
    adresse = db.Column(db.Text)
    ville = db.Column(db.String(100))
    code_postal = db.Column(db.String(10))
    pays = db.Column(db.String(100), default='France')
    budget_min = db.Column(Numeric(10, 2))
    budget_max = db.Column(Numeric(10, 2))
    preferences = db.Column(db.Text)
    type_recherche = db.Column(db.String(20))  # 'vente', 'location', 'les_deux'
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)
    is_prospect = db.Column(db.Boolean, default=True)
    
    # Relations
    contrats = db.relationship('Contrat', backref='client', lazy='dynamic', cascade='all, delete-orphan')
    demandes_visite = db.relationship('DemandeVisite', backref='client', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, nom, prenom, email, telephone=None, date_naissance=None, profession=None, 
                 adresse=None, ville=None, code_postal=None, pays=None, budget_min=None, 
                 budget_max=None, preferences=None, type_recherche=None, notes=None, is_prospect=True):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.date_naissance = date_naissance
        self.profession = profession
        self.adresse = adresse
        self.ville = ville
        self.code_postal = code_postal
        self.pays = pays
        self.budget_min = budget_min
        self.budget_max = budget_max
        self.preferences = preferences
        self.type_recherche = type_recherche
        self.notes = notes
        self.is_prospect = is_prospect
    
    @property
    def est_actif(self):
        """Retourne True si le client est actif (pas un prospect)"""
        return not self.is_prospect
    
    def get_full_name(self):
        """Retourne le nom complet"""
        return f"{self.prenom} {self.nom}"
    
    def get_full_address(self):
        """Retourne l'adresse complète"""
        parts = []
        if self.adresse:
            parts.append(self.adresse)
        if self.code_postal and self.ville:
            parts.append(f"{self.code_postal} {self.ville}")
        elif self.ville:
            parts.append(self.ville)
        if self.pays and self.pays != 'France':
            parts.append(self.pays)
        return ", ".join(parts) if parts else "Non renseignée"
    
    def get_budget_range(self):
        """Retourne la fourchette de budget"""
        if self.budget_min and self.budget_max:
            return f"{self.budget_min:,.0f} FCFA - {self.budget_max:,.0f} FCFA"
        elif self.budget_min:
            return f"À partir de {self.budget_min:,.0f} FCFA"
        elif self.budget_max:
            return f"Jusqu'à {self.budget_max:,.0f} FCFA"
        return "Non renseigné"
    
    def __repr__(self):
        return f'<Client {self.get_full_name()}>' 