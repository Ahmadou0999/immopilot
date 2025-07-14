import re
from wtforms.validators import ValidationError

def validate_phone(form, field):
    """Valide un numéro de téléphone français"""
    if field.data:
        phone = re.sub(r'[^\d+]', '', str(field.data))
        
        # Format français
        if phone.startswith('+33'):
            phone = phone[3:]
        
        # Vérifier la longueur
        if len(phone) != 10:
            raise ValidationError('Le numéro de téléphone doit contenir 10 chiffres')
        
        # Vérifier qu'il commence par 0
        if not phone.startswith('0'):
            raise ValidationError('Le numéro de téléphone doit commencer par 0')

def validate_postal_code(form, field):
    """Valide un code postal français"""
    if field.data:
        postal_code = str(field.data).strip()
        
        # Vérifier le format (5 chiffres)
        if not re.match(r'^\d{5}$', postal_code):
            raise ValidationError('Le code postal doit contenir 5 chiffres')
        
        # Vérifier la plage (01000-98890)
        code = int(postal_code)
        if code < 1000 or code > 98890:
            raise ValidationError('Code postal invalide')

def validate_price(form, field):
    """Valide un prix"""
    if field.data is not None:
        try:
            price = float(field.data)
            if price < 0:
                raise ValidationError('Le prix ne peut pas être négatif')
        except (ValueError, TypeError):
            raise ValidationError('Prix invalide')

def validate_surface(form, field):
    """Valide une surface"""
    if field.data is not None:
        try:
            surface = float(field.data)
            if surface <= 0:
                raise ValidationError('La surface doit être positive')
            if surface > 10000:  # 10 000 m² max
                raise ValidationError('La surface semble trop importante')
        except (ValueError, TypeError):
            raise ValidationError('Surface invalide')

def validate_email_domain(form, field):
    """Valide le domaine d'un email"""
    if field.data:
        email = field.data.lower()
        domain = email.split('@')[-1] if '@' in email else ''
        
        # Liste des domaines autorisés (optionnel)
        allowed_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        
        if domain in allowed_domains:
            raise ValidationError('Veuillez utiliser une adresse email professionnelle')

def validate_password_strength(form, field):
    """Valide la force d'un mot de passe"""
    if field.data:
        password = field.data
        
        # Vérifications de sécurité
        if len(password) < 8:
            raise ValidationError('Le mot de passe doit contenir au moins 8 caractères')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Le mot de passe doit contenir au moins une majuscule')
        
        if not re.search(r'[a-z]', password):
            raise ValidationError('Le mot de passe doit contenir au moins une minuscule')
        
        if not re.search(r'\d', password):
            raise ValidationError('Le mot de passe doit contenir au moins un chiffre')

def validate_future_date(form, field):
    """Valide qu'une date est dans le futur"""
    from datetime import date
    
    if field.data:
        if field.data <= date.today():
            raise ValidationError('La date doit être dans le futur')

def validate_past_date(form, field):
    """Valide qu'une date est dans le passé"""
    from datetime import date
    
    if field.data:
        if field.data >= date.today():
            raise ValidationError('La date doit être dans le passé') 