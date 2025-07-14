from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SelectField, DateField, 
                    TimeField, IntegerField, SubmitField)
from wtforms.validators import DataRequired, Length, Email, Optional, NumberRange, ValidationError
from datetime import date

class DemandeVisiteForm(FlaskForm):
    """Formulaire pour demander une visite"""
    nom_contact = StringField('Nom complet', validators=[
        DataRequired(message='Le nom est requis'),
        Length(max=100, message='Le nom ne peut pas dépasser 100 caractères')
    ])
    telephone_contact = StringField('Téléphone', validators=[
        DataRequired(message='Le téléphone est requis'),
        Length(max=20, message='Le téléphone ne peut pas dépasser 20 caractères')
    ])
    email_contact = StringField('Email', validators=[
        Optional(),
        Email(message='Format d\'email invalide'),
        Length(max=120, message='L\'email ne peut pas dépasser 120 caractères')
    ])
    
    date_souhaitee = DateField('Date souhaitée', validators=[
        DataRequired(message='La date est requise')
    ])
    heure_souhaitee = TimeField('Heure souhaitée', validators=[
        DataRequired(message='L\'heure est requise')
    ])
    
    nombre_personnes = IntegerField('Nombre de personnes', validators=[
        Optional(),
        NumberRange(min=1, max=10, message='Le nombre de personnes doit être entre 1 et 10')
    ])
    motivation = SelectField('Motivation', choices=[
        ('', 'Sélectionnez une motivation'),
        ('achat', 'Achat'),
        ('location', 'Location'),
        ('curiosite', 'Curiosité'),
        ('investissement', 'Investissement')
    ], validators=[DataRequired(message='La motivation est requise')])
    
    commentaires = TextAreaField('Commentaires ou questions')
    
    submit = SubmitField('Demander une visite')
    
    def validate_date_souhaitee(self, field):
        """Vérifie que la date n'est pas dans le passé"""
        if field.data and field.data < date.today():
            raise ValidationError('La date ne peut pas être dans le passé.') 