from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SelectField, DecimalField, 
                    BooleanField, SubmitField, DateField)
from wtforms.validators import DataRequired, Length, Email, Optional, NumberRange

class ClientForm(FlaskForm):
    """Formulaire pour ajouter/modifier un client"""
    nom = StringField('Nom', validators=[
        DataRequired(message='Le nom est requis'),
        Length(max=100, message='Le nom ne peut pas dépasser 100 caractères')
    ])
    prenom = StringField('Prénom', validators=[
        DataRequired(message='Le prénom est requis'),
        Length(max=100, message='Le prénom ne peut pas dépasser 100 caractères')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='L\'email est requis'),
        Email(message='Format d\'email invalide'),
        Length(max=120, message='L\'email ne peut pas dépasser 120 caractères')
    ])
    telephone = StringField('Téléphone', validators=[
        Length(max=20, message='Le téléphone ne peut pas dépasser 20 caractères')
    ])
    date_naissance = DateField('Date de naissance', validators=[
        Optional()
    ])
    profession = StringField('Profession', validators=[
        Length(max=100, message='La profession ne peut pas dépasser 100 caractères')
    ])
    adresse = TextAreaField('Adresse')
    ville = StringField('Ville', validators=[
        Length(max=100, message='La ville ne peut pas dépasser 100 caractères')
    ])
    code_postal = StringField('Code postal', validators=[
        Length(max=10, message='Le code postal ne peut pas dépasser 10 caractères')
    ])
    pays = StringField('Pays', validators=[
        Length(max=100, message='Le pays ne peut pas dépasser 100 caractères')
    ])
    
    # Budget et recherche
    budget_min = DecimalField('Budget minimum (FCFA)', validators=[
        Optional(),
        NumberRange(min=0, message='Le budget doit être positif')
    ])
    budget_max = DecimalField('Budget maximum (FCFA)', validators=[
        Optional(),
        NumberRange(min=0, message='Le budget doit être positif')
    ])
    preferences = TextAreaField('Préférences')
    type_recherche = SelectField('Type de recherche', choices=[
        ('', 'Non renseigné'),
        ('vente', 'Achat'),
        ('location', 'Location'),
        ('les_deux', 'Les deux')
    ], validators=[Optional()])
    
    notes = TextAreaField('Notes')
    is_prospect = BooleanField('Prospect')
    
    submit = SubmitField('Enregistrer')

class ClientSearchForm(FlaskForm):
    """Formulaire de recherche de clients"""
    nom = StringField('Nom')
    prenom = StringField('Prénom')
    email = StringField('Email')
    ville = StringField('Ville')
    type_recherche = SelectField('Type de recherche', choices=[
        ('', 'Tous'),
        ('vente', 'Achat'),
        ('location', 'Location'),
        ('les_deux', 'Les deux')
    ])
    is_prospect = SelectField('Statut', choices=[
        ('', 'Tous'),
        ('1', 'Prospects'),
        ('0', 'Clients')
    ])
    
    submit = SubmitField('Rechercher') 