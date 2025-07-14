from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.services.bien_service import BienService
from app.services.client_service import ClientService
from app.services.contrat_service import ContratService
from app.services.visite_service import VisiteService
from app.services.auth_service import AuthService
from app import csrf

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Page d'accueil publique"""
    # Récupérer quelques biens récents pour l'affichage
    biens_recents = BienService.get_biens_disponibles()[:6]
    return render_template('main/index.html', biens_recents=biens_recents, title='Accueil')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal de l'agent"""
    # Statistiques générales
    stats_biens = BienService.get_statistics()
    stats_clients = ClientService.get_statistics()
    stats_contrats = ContratService.get_statistics()
    stats_visites = VisiteService.get_statistics()
    stats_agents = AuthService.get_agents_statistics()
    
    # Demandes de visite en attente
    demandes_en_attente = VisiteService.get_demandes_en_attente()
    
    # Visites du jour
    visites_du_jour = VisiteService.get_demandes_du_jour()
    
    # Biens récents de l'agent
    biens_agent = BienService.get_biens_by_agent(current_user.id, page=1, per_page=5)
    
    # Contrats récents de l'agent
    contrats_agent = ContratService.get_contrats_by_agent(current_user.id, page=1, per_page=5)
    
    return render_template('main/dashboard.html',
                         stats_biens=stats_biens,
                         stats_clients=stats_clients,
                         stats_contrats=stats_contrats,
                         stats_visites=stats_visites,
                         stats_agents=stats_agents,
                         demandes_en_attente=demandes_en_attente,
                         visites_du_jour=visites_du_jour,
                         biens_agent=biens_agent,
                         contrats_agent=contrats_agent,
                         title='Tableau de bord')

@main_bp.route('/search')
def search():
    """Page de recherche de biens"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        biens = BienService.search_biens(query, page=page)
    else:
        biens = BienService.get_all_biens(page=page)
    
    return render_template('main/search.html', biens=biens, query=query, title='Recherche')

@main_bp.route('/about')
def about():
    """Page À propos"""
    return render_template('main/about.html', title='À propos')

@main_bp.route('/contact')
def contact():
    """Page Contact"""
    return render_template('main/contact.html', title='Contact')

@main_bp.route('/demande-visite', methods=['POST'])
@csrf.exempt
def demande_visite():
    """Enregistre une demande de visite depuis le formulaire d'un bien"""
    from app.models.demande_visite import DemandeVisite, StatutDemande
    from app import db
    
    try:
        # Récupérer les données du formulaire directement
        bien_id = request.form.get('bien_id')
        nom_contact = request.form.get('nom_contact')
        telephone_contact = request.form.get('telephone_contact')
        email_contact = request.form.get('email_contact')
        date_souhaitee = request.form.get('date_souhaitee')
        heure_souhaitee = request.form.get('heure_souhaitee')
        nombre_personnes = request.form.get('nombre_personnes')
        motivation = request.form.get('motivation')
        commentaires = request.form.get('commentaires')
        
        # Validation des champs obligatoires
        if not bien_id:
            flash('Bien non spécifié.', 'danger')
            return redirect(request.referrer or url_for('main.index'))
        
        if not nom_contact:
            flash('Le nom de contact est obligatoire.', 'danger')
            return redirect(request.referrer or url_for('main.index'))
        
        if not telephone_contact:
            flash('Le téléphone de contact est obligatoire.', 'danger')
            return redirect(request.referrer or url_for('main.index'))
        
        if not date_souhaitee:
            flash('La date souhaitée est obligatoire.', 'danger')
            return redirect(request.referrer or url_for('main.index'))
        
        if not heure_souhaitee:
            flash('L\'heure souhaitée est obligatoire.', 'danger')
            return redirect(request.referrer or url_for('main.index'))
        
        # Convertir les types
        from datetime import datetime, time
        try:
            date_souhaitee = datetime.strptime(date_souhaitee, '%Y-%m-%d').date()
        except ValueError:
            flash('Format de date invalide.', 'danger')
            return redirect(request.referrer or url_for('main.index'))
        
        try:
            heure_souhaitee = datetime.strptime(heure_souhaitee, '%H:%M').time()
        except ValueError:
            flash('Format d\'heure invalide.', 'danger')
            return redirect(request.referrer or url_for('main.index'))
        
        if nombre_personnes:
            try:
                nombre_personnes = int(nombre_personnes)
            except ValueError:
                nombre_personnes = 1
        
        # Créer la demande de visite
        demande = DemandeVisite(
            bien_id=bien_id,
            nom_contact=nom_contact,
            telephone_contact=telephone_contact,
            email_contact=email_contact,
            date_souhaitee=date_souhaitee,
            heure_souhaitee=heure_souhaitee,
            nombre_personnes=nombre_personnes,
            motivation=motivation,
            commentaires=commentaires,
            statut=StatutDemande.EN_ATTENTE
        )
        
        db.session.add(demande)
        db.session.commit()
        flash('Votre demande de visite a bien été enregistrée. Nous vous contacterons rapidement.', 'success')
        return redirect(url_for('biens.detail', bien_id=bien_id))
        
    except Exception as e:
        flash(f'Erreur lors de l\'enregistrement de la demande: {str(e)}', 'danger')
        return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/demande-visite/<int:bien_id>', methods=['GET'])
def demande_visite_form(bien_id):
    """Affiche le formulaire de demande de visite pour un bien spécifique"""
    from app.services.bien_service import BienService
    from app.forms.visite_forms import DemandeVisiteForm
    
    bien = BienService.get_bien_by_id(bien_id)
    form = DemandeVisiteForm()
    
    return render_template('main/demande_visite_form.html', 
                         form=form, 
                         bien=bien,
                         title='Demande de visite')

@main_bp.route('/api/stats')
@login_required
def api_stats():
    """API pour récupérer les statistiques en AJAX"""
    stats = {
        'biens': BienService.get_statistics(),
        'clients': ClientService.get_statistics(),
        'contrats': ContratService.get_statistics(),
        'visites': VisiteService.get_statistics(),
        'agents': AuthService.get_agents_statistics()
    }
    return jsonify(stats)

@main_bp.route('/api/visites-jour')
@login_required
def api_visites_jour():
    """API pour récupérer les visites du jour"""
    visites = VisiteService.get_demandes_du_jour()
    return jsonify([{
        'id': v.id,
        'nom_contact': v.nom_contact,
        'heure': v.get_heure_display(),
        'bien_titre': v.bien.titre if v.bien else '',
        'statut': v.statut.value
    } for v in visites])

@main_bp.route('/api/demandes-attente')
@login_required
def api_demandes_attente():
    """API pour récupérer les demandes en attente"""
    demandes = VisiteService.get_demandes_en_attente()
    return jsonify([{
        'id': d.id,
        'nom_contact': d.nom_contact,
        'date': d.get_date_display(),
        'heure': d.get_heure_display(),
        'bien_titre': d.bien.titre if d.bien else '',
        'telephone': d.telephone_contact
    } for d in demandes]) 