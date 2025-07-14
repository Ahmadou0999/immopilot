from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SelectField, DecimalField, 
                    IntegerField, DateField, BooleanField, SubmitField)
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email
from app.models.bien import TypeBien, TypeTransaction

class BienForm(FlaskForm):
    """Formulaire pour ajouter/modifier un bien"""
    reference = StringField('Référence', validators=[
        DataRequired(message='La référence est requise'),
        Length(max=50, message='La référence ne peut pas dépasser 50 caractères')
    ])
    titre = StringField('Titre', validators=[
        DataRequired(message='Le titre est requis'),
        Length(max=200, message='Le titre ne peut pas dépasser 200 caractères')
    ])
    description = TextAreaField('Description')
    type_bien = SelectField('Type de bien', choices=[
        (TypeBien.APPARTEMENT.value, 'Appartement'),
        (TypeBien.MAISON.value, 'Maison'),
        (TypeBien.TERRAIN.value, 'Terrain'),
        (TypeBien.COMMERCIAL.value, 'Local commercial'),
        (TypeBien.BUREAUX.value, 'Bureaux'),
        (TypeBien.LOCAL_INDUSTRIEL.value, 'Local industriel')
    ], validators=[DataRequired(message='Le type de bien est requis')])
    
    type_transaction = SelectField('Type de transaction', choices=[
        (TypeTransaction.VENTE.value, 'Vente'),
        (TypeTransaction.LOCATION.value, 'Location')
    ], validators=[DataRequired(message='Le type de transaction est requis')])
    
    # Localisation
    adresse = StringField('Adresse', validators=[
        DataRequired(message='L\'adresse est requise'),
        Length(max=200, message='L\'adresse ne peut pas dépasser 200 caractères')
    ])
    ville = StringField('Ville', validators=[
        DataRequired(message='La ville est requise'),
        Length(max=100, message='La ville ne peut pas dépasser 100 caractères')
    ])
    code_postal = StringField('Code postal', validators=[
        DataRequired(message='Le code postal est requis'),
        Length(max=10, message='Le code postal ne peut pas dépasser 10 caractères')
    ])
    quartier = StringField('Quartier', validators=[
        Length(max=100, message='Le quartier ne peut pas dépasser 100 caractères')
    ])
    
    # Caractéristiques
    surface_habitable = DecimalField('Surface habitable (m²)', validators=[
        Optional(),
        NumberRange(min=0, message='La surface doit être positive')
    ])
    surface_terrain = DecimalField('Surface du terrain (m²)', validators=[
        Optional(),
        NumberRange(min=0, message='La surface doit être positive')
    ])
    nombre_pieces = IntegerField('Nombre de pièces', validators=[
        Optional(),
        NumberRange(min=1, message='Le nombre de pièces doit être positif')
    ])
    nombre_chambres = IntegerField('Nombre de chambres', validators=[
        Optional(),
        NumberRange(min=0, message='Le nombre de chambres doit être positif')
    ])
    nombre_salles_bain = IntegerField('Nombre de salles de bain', validators=[
        Optional(),
        NumberRange(min=0, message='Le nombre de salles de bain doit être positif')
    ])
    nombre_etages = IntegerField('Nombre d\'étages', validators=[
        Optional(),
        NumberRange(min=0, message='Le nombre d\'étages doit être positif')
    ])
    etage = IntegerField('Étage', validators=[
        Optional(),
        NumberRange(min=0, message='L\'étage doit être positif')
    ])
    annee_construction = IntegerField('Année de construction', validators=[
        Optional(),
        NumberRange(min=1800, max=2024, message='L\'année doit être entre 1800 et 2024')
    ])
    
    # Énergie
    classe_energie = SelectField('Classe énergétique', choices=[
        ('', 'Non renseigné'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G')
    ])
    emission_ges = SelectField('Émission GES', choices=[
        ('', 'Non renseigné'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G')
    ])
    
    # Prix
    prix_vente = DecimalField('Prix de vente (FCFA)', validators=[
        Optional(),
        NumberRange(min=0, message='Le prix doit être positif')
    ])
    prix_location = DecimalField('Prix de location (FCFA/mois)', validators=[
        Optional(),
        NumberRange(min=0, message='Le prix doit être positif')
    ])
    charges = DecimalField('Charges (FCFA)', validators=[
        Optional(),
        NumberRange(min=0, message='Les charges doivent être positives')
    ])
    taxe_fonciere = DecimalField('Taxe foncière (FCFA)', validators=[
        Optional(),
        NumberRange(min=0, message='La taxe foncière doit être positive')
    ])
    
    # État et disponibilité
    etat = SelectField('État', choices=[
        ('', 'Non renseigné'),
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('à rénover', 'À rénover')
    ])
    disponible = BooleanField('Disponible')
    date_disponibilite = DateField('Date de disponibilité')
    
    # Informations supplémentaires
    equipements = TextAreaField('Équipements')
    points_forts = TextAreaField('Points forts')
    points_faibles = TextAreaField('Points faibles')
    notes_agent = TextAreaField('Notes agent')
    
    submit = SubmitField('Enregistrer')

class BienSearchForm(FlaskForm):
    """Formulaire de recherche de biens"""
    type_bien = SelectField('Type de bien', choices=[
        ('', 'Tous les types'),
        (TypeBien.APPARTEMENT.value, 'Appartement'),
        (TypeBien.MAISON.value, 'Maison'),
        (TypeBien.TERRAIN.value, 'Terrain'),
        (TypeBien.COMMERCIAL.value, 'Local commercial'),
        (TypeBien.BUREAUX.value, 'Bureaux'),
        (TypeBien.LOCAL_INDUSTRIEL.value, 'Local industriel')
    ])
    
    type_transaction = SelectField('Type de transaction', choices=[
        ('', 'Tous'),
        (TypeTransaction.VENTE.value, 'Vente'),
        (TypeTransaction.LOCATION.value, 'Location')
    ])
    
    ville = StringField('Ville')
    code_postal = StringField('Code postal')
    prix_min = DecimalField('Prix minimum (FCFA)', validators=[Optional()])
    prix_max = DecimalField('Prix maximum (FCFA)', validators=[Optional()])
    surface_min = DecimalField('Surface minimum (m²)', validators=[Optional()])
    nombre_pieces_min = IntegerField('Nombre de pièces minimum', validators=[Optional()])
    
    submit = SubmitField('Rechercher') 