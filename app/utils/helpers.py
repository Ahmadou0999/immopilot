from datetime import datetime, date
import re

def format_price(amount, currency='FCFA'):
    """Formate un montant en prix"""
    if amount is None:
        return "Prix sur demande"
    
    try:
        amount = float(amount)
        return f"{amount:,.0f}{currency}"
    except (ValueError, TypeError):
        return "Prix sur demande"

def format_date(date_obj, format_str='%d/%m/%Y'):
    """Formate une date"""
    if date_obj is None:
        return "Non renseigné"
    
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        except ValueError:
            return "Date invalide"
    
    try:
        return date_obj.strftime(format_str)
    except AttributeError:
        return "Date invalide"

def format_datetime(datetime_obj, format_str='%d/%m/%Y %H:%M'):
    """Formate une date et heure"""
    if datetime_obj is None:
        return "Non renseigné"
    
    try:
        return datetime_obj.strftime(format_str)
    except AttributeError:
        return "Date invalide"

def format_phone(phone):
    """Formate un numéro de téléphone"""
    if not phone:
        return "Non renseigné"
    
    # Nettoyer le numéro
    phone = re.sub(r'[^\d+]', '', str(phone))
    
    # Format français
    if phone.startswith('+33'):
        phone = phone[3:]
        if len(phone) == 9:
            return f"+33 {phone[:1]} {phone[1:3]} {phone[3:5]} {phone[5:7]} {phone[7:9]}"
    
    # Format international
    if phone.startswith('+'):
        return phone
    
    # Format local
    if len(phone) == 10:
        return f"{phone[:2]} {phone[2:4]} {phone[4:6]} {phone[6:8]} {phone[8:10]}"
    
    return phone

def format_surface(surface, unit='m²'):
    """Formate une surface"""
    if surface is None:
        return "Non renseigné"
    
    try:
        surface = float(surface)
        return f"{surface:,.0f} {unit}"
    except (ValueError, TypeError):
        return "Surface invalide"

def format_address(address, city, postal_code):
    """Formate une adresse complète"""
    parts = []
    if address:
        parts.append(address)
    if postal_code and city:
        parts.append(f"{postal_code} {city}")
    elif city:
        parts.append(city)
    
    return ", ".join(parts) if parts else "Adresse non renseignée"

def truncate_text(text, max_length=100, suffix='...'):
    """Tronque un texte"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def get_status_badge_class(status):
    """Retourne la classe CSS pour un badge de statut"""
    status_classes = {
        'disponible': 'badge-success',
        'vendu': 'badge-danger',
        'loué': 'badge-warning',
        'en_cours': 'badge-info',
        'signe': 'badge-success',
        'annule': 'badge-danger',
        'termine': 'badge-secondary',
        'en_attente': 'badge-warning',
        'confirmee': 'badge-info',
        'terminee': 'badge-success'
    }
    return status_classes.get(status, 'badge-secondary')

def get_type_bien_label(type_bien):
    """Retourne le label d'un type de bien"""
    labels = {
        'appartement': 'Appartement',
        'maison': 'Maison',
        'terrain': 'Terrain',
        'commercial': 'Local commercial',
        'bureaux': 'Bureaux',
        'local_industriel': 'Local industriel'
    }
    return labels.get(type_bien, type_bien.title())

def get_type_transaction_label(type_transaction):
    """Retourne le label d'un type de transaction"""
    labels = {
        'vente': 'Vente',
        'location': 'Location'
    }
    return labels.get(type_transaction, type_transaction.title()) 