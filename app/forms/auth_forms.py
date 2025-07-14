from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.agent import Agent

class LoginForm(FlaskForm):
    """Formulaire de connexion"""
    email = StringField('Email', validators=[
        DataRequired(message='L\'email est requis'),
        Email(message='Format d\'email invalide')
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message='Le mot de passe est requis')
    ])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    """Formulaire d'inscription d'agent"""
    nom = StringField('Nom', validators=[
        DataRequired(message='Le nom est requis'),
        Length(min=2, max=100, message='Le nom doit contenir entre 2 et 100 caractères')
    ])
    prenom = StringField('Prénom', validators=[
        DataRequired(message='Le prénom est requis'),
        Length(min=2, max=100, message='Le prénom doit contenir entre 2 et 100 caractères')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='L\'email est requis'),
        Email(message='Format d\'email invalide'),
        Length(max=120, message='L\'email ne peut pas dépasser 120 caractères')
    ])
    telephone = StringField('Téléphone', validators=[
        Length(max=20, message='Le téléphone ne peut pas dépasser 20 caractères')
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message='Le mot de passe est requis'),
        Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères')
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(message='La confirmation du mot de passe est requise'),
        EqualTo('password', message='Les mots de passe doivent être identiques')
    ])
    submit = SubmitField('S\'inscrire')
    
    def validate_email(self, email):
        """Vérifie que l'email n'existe pas déjà"""
        agent = Agent.query.filter_by(email=email.data).first()
        if agent:
            raise ValidationError('Cet email est déjà utilisé.')

class ChangePasswordForm(FlaskForm):
    """Formulaire de changement de mot de passe"""
    current_password = PasswordField('Mot de passe actuel', validators=[
        DataRequired(message='Le mot de passe actuel est requis')
    ])
    new_password = PasswordField('Nouveau mot de passe', validators=[
        DataRequired(message='Le nouveau mot de passe est requis'),
        Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères')
    ])
    confirm_password = PasswordField('Confirmer le nouveau mot de passe', validators=[
        DataRequired(message='La confirmation du mot de passe est requise'),
        EqualTo('new_password', message='Les mots de passe doivent être identiques')
    ])
    submit = SubmitField('Changer le mot de passe') 