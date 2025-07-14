from app.forms.auth_forms import LoginForm, RegisterForm
from app.forms.bien_forms import BienForm, BienSearchForm
from app.forms.client_forms import ClientForm, ClientSearchForm
from app.forms.contrat_forms import ContratForm
from app.forms.visite_forms import DemandeVisiteForm

__all__ = [
    'LoginForm', 'RegisterForm',
    'BienForm', 'BienSearchForm',
    'ClientForm', 'ClientSearchForm',
    'ContratForm',
    'DemandeVisiteForm'
] 