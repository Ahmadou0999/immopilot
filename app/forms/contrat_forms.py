from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SelectField, DecimalField, 
                    DateField, IntegerField, SubmitField)
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.models.contrat import TypeContrat

class ContratForm(FlaskForm):
    """Formulaire pour créer/modifier un contrat"""
    numero = StringField('Numéro de contrat', validators=[
        DataRequired(message='Le numéro de contrat est requis'),
        Length(max=50, message='Le numéro ne peut pas dépasser 50 caractères')
    ])
    type_contrat = SelectField('Type de contrat', choices=[
        (TypeContrat.VENTE.value, 'Vente'),
        (TypeContrat.LOCATION.value, 'Location')
    ], validators=[DataRequired(message='Le type de contrat est requis')])
    
    # Montants
    montant = DecimalField('Montant (FCFA)', validators=[
        DataRequired(message='Le montant est requis'),
        NumberRange(min=0, message='Le montant doit être positif')
    ])
    frais_agence = DecimalField('Frais d\'agence (FCFA)', validators=[
        Optional(),
        NumberRange(min=0, message='Les frais doivent être positifs')
    ])
    charges = DecimalField('Charges (FCFA)', validators=[
        Optional(),
        NumberRange(min=0, message='Les charges doivent être positives')
    ])
    caution = DecimalField('Caution (FCFA)', validators=[
        Optional(),
        NumberRange(min=0, message='La caution doit être positive')
    ])
    
    # Dates
    date_entree = DateField('Date d\'entrée dans les lieux', validators=[
        Optional()
    ])
    date_sortie = DateField('Date de sortie', validators=[
        Optional()
    ])
    date_fin_bail = DateField('Date de fin de bail', validators=[
        Optional()
    ])
    
    # Durée (pour locations)
    duree_bail = IntegerField('Durée du bail (mois)', validators=[
        Optional(),
        NumberRange(min=1, message='La durée doit être d\'au moins 1 mois')
    ])
    
    # Conditions
    conditions_particulieres = TextAreaField('Conditions particulières')
    notes = TextAreaField('Notes')
    
    submit = SubmitField('Enregistrer') 