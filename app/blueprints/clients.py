from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.forms.client_forms import ClientForm, ClientSearchForm
from app.services.client_service import ClientService
from app import csrf

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
@login_required
def index():
    """Liste des clients"""
    page = request.args.get('page', 1, type=int)
    form = ClientSearchForm()
    
    # Récupérer les filtres depuis l'URL
    filters = {}
    if form.nom.data:
        filters['nom'] = form.nom.data
    if form.prenom.data:
        filters['prenom'] = form.prenom.data
    if form.email.data:
        filters['email'] = form.email.data
    if form.ville.data:
        filters['ville'] = form.ville.data
    if form.type_recherche.data:
        filters['type_recherche'] = form.type_recherche.data
    if form.is_prospect.data:
        filters['is_prospect'] = form.is_prospect.data == '1'
    
    clients = ClientService.get_all_clients(page=page, filters=filters)
    
    return render_template('clients/index.html', clients=clients, form=form, title='Clients')

@clients_bp.route('/<int:client_id>')
@login_required
def detail(client_id):
    """Détail d'un client"""
    client = ClientService.get_client_by_id(client_id)
    
    # Récupérer les demandes de visite du client
    from app.services.visite_service import VisiteService
    demandes_visite = VisiteService.get_demandes_by_client(client_id, page=1, per_page=10)
    
    # Récupérer les contrats du client
    from app.services.contrat_service import ContratService
    contrats = ContratService.get_contrats_by_client(client_id, page=1, per_page=10)
    
    return render_template('clients/detail.html', 
                         client=client, 
                         demandes_visite=demandes_visite,
                         contrats=contrats,
                         title=f'Client - {client.get_full_name()}')

@clients_bp.route('/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    """Ajouter un nouveau client"""
    form = ClientForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            data = {
                'nom': form.nom.data,
                'prenom': form.prenom.data,
                'email': form.email.data,
                'telephone': form.telephone.data,
                'date_naissance': form.date_naissance.data,
                'profession': form.profession.data,
                'adresse': form.adresse.data,
                'ville': form.ville.data,
                'code_postal': form.code_postal.data,
                'pays': form.pays.data,
                'budget_min': form.budget_min.data,
                'budget_max': form.budget_max.data,
                'preferences': form.preferences.data,
                'type_recherche': form.type_recherche.data,
                'notes': form.notes.data,
                'is_prospect': form.is_prospect.data
            }
            
            try:
                client = ClientService.create_client(data)
                flash(f'Client "{client.get_full_name()}" ajouté avec succès !', 'success')
                return redirect(url_for('clients.detail', client_id=client.id))
            except Exception as e:
                flash(f'Erreur lors de la création du client: {str(e)}', 'danger')
        else:
            # Afficher les erreurs de validation
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Erreur dans {field}: {error}', 'danger')
    
    return render_template('clients/form.html', form=form, title='Ajouter un client')

@clients_bp.route('/<int:client_id>/modifier', methods=['GET', 'POST'])
@login_required
def modifier(client_id):
    """Modifier un client existant"""
    client = ClientService.get_client_by_id(client_id)
    form = ClientForm(obj=client)
    
    if form.validate_on_submit():
        data = {
            'nom': form.nom.data,
            'prenom': form.prenom.data,
            'email': form.email.data,
            'telephone': form.telephone.data,
            'date_naissance': form.date_naissance.data,
            'profession': form.profession.data,
            'adresse': form.adresse.data,
            'ville': form.ville.data,
            'code_postal': form.code_postal.data,
            'pays': form.pays.data,
            'budget_min': form.budget_min.data,
            'budget_max': form.budget_max.data,
            'preferences': form.preferences.data,
            'type_recherche': form.type_recherche.data,
            'notes': form.notes.data,
            'is_prospect': form.is_prospect.data
        }
        
        ClientService.update_client(client_id, data)
        flash(f'Client "{client.get_full_name()}" modifié avec succès !', 'success')
        return redirect(url_for('clients.detail', client_id=client.id))
    
    return render_template('clients/form.html', form=form, client=client, title='Modifier le client')

@clients_bp.route('/<int:client_id>/supprimer', methods=['POST'])
@login_required
@csrf.exempt
def supprimer(client_id):
    """Supprimer un client"""
    try:
        client = ClientService.get_client_by_id(client_id)
        nom = client.get_full_name()
        
        # Vérifier s'il y a des relations qui empêchent la suppression
        if client.contrats.count() > 0:
            flash(f'Impossible de supprimer le client "{nom}" car il a des contrats associés.', 'danger')
            return redirect(url_for('clients.detail', client_id=client_id))
        
        if client.demandes_visite.count() > 0:
            flash(f'Impossible de supprimer le client "{nom}" car il a des demandes de visite associées.', 'danger')
            return redirect(url_for('clients.detail', client_id=client_id))
        
        ClientService.delete_client(client_id)
        flash(f'Client "{nom}" supprimé avec succès !', 'success')
        return redirect(url_for('clients.index'))
        
    except Exception as e:
        flash(f'Erreur lors de la suppression du client: {str(e)}', 'danger')
        return redirect(url_for('clients.detail', client_id=client_id))

@clients_bp.route('/<int:client_id>/convertir-client', methods=['POST'])
@login_required
def convertir_client(client_id):
    """Convertir un prospect en client"""
    client = ClientService.convert_prospect_to_client(client_id)
    flash(f'Prospect "{client.get_full_name()}" converti en client !', 'success')
    return redirect(url_for('clients.detail', client_id=client.id))

@clients_bp.route('/prospects')
@login_required
def prospects():
    """Liste des prospects"""
    prospects = ClientService.get_prospects()
    return render_template('clients/prospects.html', prospects=prospects, title='Prospects')

@clients_bp.route('/clients-actifs')
@login_required
def clients_actifs():
    """Liste des clients actifs"""
    clients = ClientService.get_clients()
    return render_template('clients/clients_actifs.html', clients=clients, title='Clients actifs')

@clients_bp.route('/<int:client_id>/demande-visite/<int:bien_id>', methods=['GET', 'POST'])
def demande_visite(client_id, bien_id):
    """Demande de visite pour un client spécifique"""
    from app.forms.visite_forms import DemandeVisiteForm
    from app.services.visite_service import VisiteService
    from app.services.bien_service import BienService
    
    # Validation des paramètres
    if bien_id <= 0:
        flash('Bien invalide.', 'danger')
        return redirect(url_for('clients.detail', client_id=client_id))
    
    try:
        client = ClientService.get_client_by_id(client_id)
        bien = BienService.get_bien_by_id(bien_id)
        
        if not bien:
            flash('Bien non trouvé.', 'danger')
            return redirect(url_for('clients.detail', client_id=client_id))
            
    except Exception as e:
        flash('Erreur lors de la récupération des données.', 'danger')
        return redirect(url_for('clients.detail', client_id=client_id))
    
    form = DemandeVisiteForm()
    
    if form.validate_on_submit():
        data = {
            'date_souhaitee': form.date_souhaitee.data,
            'heure_souhaitee': form.heure_souhaitee.data,
            'nom_contact': form.nom_contact.data,
            'telephone_contact': form.telephone_contact.data,
            'bien_id': bien_id,
            'email_contact': form.email_contact.data,
            'nombre_personnes': form.nombre_personnes.data,
            'commentaires': form.commentaires.data,
            'motivation': form.motivation.data,
            'client_id': client_id
        }
        
        demande = VisiteService.create_demande(data)
        flash('Demande de visite envoyée avec succès !', 'success')
        return redirect(url_for('clients.detail', client_id=client.id))
    
    return render_template('clients/demande_visite.html', 
                         form=form, 
                         client=client, 
                         bien=bien,
                         title='Demande de visite')

@clients_bp.route('/api/search')
@login_required
def api_search():
    """API de recherche AJAX"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        clients = ClientService.search_clients(query, page=page)
    else:
        clients = ClientService.get_all_clients(page=page)
    
    return jsonify({
        'clients': [{
            'id': c.id,
            'nom': c.nom,
            'prenom': c.prenom,
            'email': c.email,
            'telephone': c.telephone,
            'ville': c.ville,
            'type_recherche': c.type_recherche,
            'is_prospect': c.is_prospect
        } for c in clients.items],
        'total': clients.total,
        'pages': clients.pages,
        'current_page': clients.page
    }) 