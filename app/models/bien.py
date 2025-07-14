from app import db
from datetime import datetime
from sqlalchemy import Numeric
import enum

class TypeBien(enum.Enum):
    APPARTEMENT = "appartement"
    MAISON = "maison"
    TERRAIN = "terrain"
    COMMERCIAL = "commercial"
    BUREAUX = "bureaux"
    LOCAL_INDUSTRIEL = "local_industriel"

class TypeTransaction(enum.Enum):
    VENTE = "vente"
    LOCATION = "location"

class Bien(db.Model):
    """Modèle pour les biens immobiliers"""
    __tablename__ = 'biens'
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True, nullable=False)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type_bien = db.Column(db.Enum(TypeBien), nullable=False)
    type_transaction = db.Column(db.Enum(TypeTransaction), nullable=False)
    
    # Localisation
    adresse = db.Column(db.String(200), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    code_postal = db.Column(db.String(10), nullable=False)
    quartier = db.Column(db.String(100))
    
    # Caractéristiques
    surface_habitable = db.Column(db.Float)  # m²
    surface_terrain = db.Column(db.Float)    # m²
    nombre_pieces = db.Column(db.Integer)
    nombre_chambres = db.Column(db.Integer)
    nombre_salles_bain = db.Column(db.Integer)
    nombre_etages = db.Column(db.Integer)
    etage = db.Column(db.Integer)
    annee_construction = db.Column(db.Integer)
    
    # Énergie
    classe_energie = db.Column(db.String(2))  # A, B, C, D, E, F, G
    emission_ges = db.Column(db.String(2))    # A, B, C, D, E, F, G
    
    # Prix
    prix_vente = db.Column(Numeric(10, 2))
    prix_location = db.Column(Numeric(10, 2))
    charges = db.Column(Numeric(8, 2))
    taxe_fonciere = db.Column(Numeric(8, 2))
    
    # État et disponibilité
    etat = db.Column(db.String(50))  # 'excellent', 'bon', 'moyen', 'à rénover'
    disponible = db.Column(db.Boolean, default=True)
    date_disponibilite = db.Column(db.Date)
    
    # Informations supplémentaires
    equipements = db.Column(db.Text)  # JSON ou texte libre
    points_forts = db.Column(db.Text)
    points_faibles = db.Column(db.Text)
    notes_agent = db.Column(db.Text)
    
    # Images
    images = db.Column(db.Text)  # JSON array of image URLs
    
    # Métadonnées
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    contrats = db.relationship('Contrat', backref='bien', lazy='dynamic', cascade='all, delete-orphan')
    demandes_visite = db.relationship('DemandeVisite', backref='bien', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, reference, titre, type_bien, type_transaction, adresse, ville, 
                 code_postal, agent_id, **kwargs):
        self.reference = reference
        self.titre = titre
        self.type_bien = type_bien
        self.type_transaction = type_transaction
        self.adresse = adresse
        self.ville = ville
        self.code_postal = code_postal
        self.agent_id = agent_id
        
        # Attributs optionnels
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_full_address(self):
        """Retourne l'adresse complète"""
        parts = [self.adresse]
        if self.quartier:
            parts.append(f"Quartier {self.quartier}")
        parts.append(f"{self.code_postal} {self.ville}")
        return ", ".join(parts)
    
    @property
    def prix(self):
        """Propriété pour accéder au prix selon le type de transaction"""
        if self.type_transaction == TypeTransaction.VENTE:
            return self.prix_vente
        else:
            return self.prix_location
    
    def get_price_display(self):
        """Retourne le prix formaté selon le type de transaction"""
        if self.type_transaction == TypeTransaction.VENTE:
            if self.prix_vente:
                return f"{self.prix_vente:,.0f} FCFA"
        else:  # location
            if self.prix_location:
                return f"{self.prix_location:,.0f} FCFA/mois"
        return "Prix sur demande"
    
    def get_surface_display(self):
        """Retourne la surface formatée"""
        if self.surface_habitable:
            return f"{self.surface_habitable} m²"
        return "Surface non renseignée"
    
    def get_rooms_display(self):
        """Retourne le nombre de pièces formaté"""
        if self.nombre_pieces:
            return f"{self.nombre_pieces} pièces"
        return "Non renseigné"
    
    def is_available(self):
        """Vérifie si le bien est disponible"""
        return self.disponible and (not self.date_disponibilite or 
                                   self.date_disponibilite <= datetime.now().date())
    
    def get_status_badge(self):
        """Retourne le badge de statut pour l'affichage"""
        if not self.disponible:
            return "Vendu/Loué"
        elif self.date_disponibilite and self.date_disponibilite > datetime.now().date():
            return "Disponible bientôt"
        else:
            return "Disponible"
    
    def get_images_list(self):
        """Retourne la liste des images"""
        if self.images:
            import json
            try:
                return json.loads(self.images)
            except:
                return []
        return []
    
    def add_image(self, image_url):
        """Ajoute une image à la liste"""
        images = self.get_images_list()
        images.append(image_url)
        import json
        self.images = json.dumps(images)
    
    def __repr__(self):
        return f'<Bien {self.reference}: {self.titre}>' 