from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.services.auth_service import AuthService
from app.services.bien_service import BienService
from app.services.client_service import ClientService
from app.services.contrat_service import ContratService
from app.services.visite_service import VisiteService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Décorateur pour vérifier les droits admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès non autorisé. Droits administrateur requis.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Dashboard administrateur"""
    # Statistiques complètes
    stats_biens = BienService.get_statistics()
    stats_clients = ClientService.get_statistics()
    stats_contrats = ContratService.get_statistics()
    stats_visites = VisiteService.get_statistics()
    stats_agents = AuthService.get_agents_statistics()
    
    # Demandes en attente
    demandes_en_attente = VisiteService.get_demandes_en_attente()
    
    # Visites du jour
    visites_du_jour = VisiteService.get_demandes_du_jour()
    
    # Demandes en retard
    demandes_retardees = VisiteService.get_demandes_retardees()
    
    return render_template('admin/dashboard.html',
                         stats_biens=stats_biens,
                         stats_clients=stats_clients,
                         stats_contrats=stats_contrats,
                         stats_visites=stats_visites,
                         stats_agents=stats_agents,
                         demandes_en_attente=demandes_en_attente,
                         visites_du_jour=visites_du_jour,
                         demandes_retardees=demandes_retardees,
                         title='Administration')

@admin_bp.route('/agents')
@login_required
@admin_required
def agents():
    """Gestion des agents"""
    import datetime
    agents = AuthService.get_all_agents()
    today_date = datetime.datetime.now().date()
    agents_connectes_aujourdhui = [
        a for a in agents if a.derniere_connexion and a.derniere_connexion.date() == today_date
    ]
    return render_template(
        'admin/agents.html',
        agents=agents,
        agents_connectes_aujourdhui=agents_connectes_aujourdhui,
        today_date=today_date,
        title='Gestion des agents'
    )

@admin_bp.route('/agents/<int:agent_id>/activer', methods=['POST'])
@login_required
@admin_required
def activer_agent(agent_id):
    """Activer un agent"""
    success, message = AuthService.activate_user(agent_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('admin_bp.agents'))

@admin_bp.route('/agents/<int:agent_id>/desactiver', methods=['POST'])
@login_required
@admin_required
def desactiver_agent(agent_id):
    """Désactiver un agent"""
    success, message = AuthService.deactivate_user(agent_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('admin_bp.agents'))

@admin_bp.route('/agents/<int:agent_id>/promouvoir-admin', methods=['POST'])
@login_required
@admin_required
def promouvoir_admin(agent_id):
    """Promouvoir un agent en admin"""
    from app import db
    from app.models.agent import Agent
    
    agent = Agent.query.get(agent_id)
    if agent:
        agent.is_admin = True
        db.session.commit()
        flash(f'Agent "{agent.get_full_name()}" promu administrateur !', 'success')
    else:
        flash('Agent non trouvé.', 'danger')
    
    return redirect(url_for('admin_bp.agents'))

@admin_bp.route('/agents/<int:agent_id>/retirer-admin', methods=['POST'])
@login_required
@admin_required
def retirer_admin(agent_id):
    """Retirer les droits admin d'un agent"""
    from app import db
    from app.models.agent import Agent
    
    agent = Agent.query.get(agent_id)
    if agent and agent.id != current_user.id:  # Empêcher de se retirer soi-même
        agent.is_admin = False
        db.session.commit()
        flash(f'Droits administrateur retirés à "{agent.get_full_name()}" !', 'success')
    else:
        flash('Action non autorisée.', 'danger')
    
    return redirect(url_for('admin_bp.agents'))

@admin_bp.route('/visites')
@login_required
@admin_required
def visites():
    """Gestion des visites"""
    page = request.args.get('page', 1, type=int)
    statut = request.args.get('statut', '')
    
    filters = {}
    if statut:
        filters['statut'] = statut
    
    demandes = VisiteService.get_all_demandes(page=page, filters=filters)
    
    return render_template('admin/visites.html', demandes=demandes, title='Gestion des visites')

@admin_bp.route('/visites/<int:demande_id>/confirmer', methods=['POST'])
@login_required
@admin_required
def confirmer_visite(demande_id):
    """Confirmer une demande de visite"""
    from app.services.visite_service import VisiteService
    
    try:
        duree = request.form.get('duree', 60, type=int)
        if duree < 15 or duree > 180:
            flash('La durée doit être comprise entre 15 et 180 minutes.', 'danger')
            return redirect(url_for('admin_bp.visites'))
        
        VisiteService.confirmer_demande(demande_id, current_user.id, duree_estimee=duree)
        flash('Visite confirmée avec succès !', 'success')
    except Exception as e:
        flash(f'Erreur lors de la confirmation : {str(e)}', 'danger')
    
    return redirect(url_for('admin_bp.visites'))

@admin_bp.route('/visites/<int:demande_id>/annuler', methods=['POST'])
@login_required
@admin_required
def annuler_visite(demande_id):
    """Annuler une demande de visite"""
    from app.services.visite_service import VisiteService
    
    try:
        VisiteService.annuler_demande(demande_id)
        flash('Visite annulée avec succès !', 'success')
    except Exception as e:
        flash(f'Erreur lors de l\'annulation : {str(e)}', 'danger')
    
    return redirect(url_for('admin_bp.visites'))

@admin_bp.route('/visites/<int:demande_id>/terminer', methods=['POST'])
@login_required
@admin_required
def terminer_visite(demande_id):
    """Terminer une visite"""
    from app.services.visite_service import VisiteService
    
    try:
        VisiteService.terminer_demande(demande_id)
        flash('Visite marquée comme terminée !', 'success')
    except Exception as e:
        flash(f'Erreur lors de la finalisation : {str(e)}', 'danger')
    
    return redirect(url_for('admin_bp.visites'))

@admin_bp.route('/rapports')
@login_required
@admin_required
def rapports():
    """Page des rapports"""
    return render_template('admin/rapports.html', title='Rapports')

@admin_bp.route('/api/statistiques-globales')
@login_required
@admin_required
def api_statistiques_globales():
    """API pour les statistiques globales"""
    stats = {
        'biens': BienService.get_statistics(),
        'clients': ClientService.get_statistics(),
        'contrats': ContratService.get_statistics(),
        'visites': VisiteService.get_statistics(),
        'agents': AuthService.get_agents_statistics()
    }
    return jsonify(stats)

@admin_bp.route('/api/visites-semaine')
@login_required
@admin_required
def api_visites_semaine():
    """API pour les visites de la semaine"""
    from app.services.visite_service import VisiteService
    
    visites = VisiteService.get_demandes_de_la_semaine()
    return jsonify([{
        'id': v.id,
        'nom_contact': v.nom_contact,
        'date': v.get_date_display(),
        'heure': v.get_heure_display(),
        'bien_titre': v.bien.titre if v.bien else '',
        'statut': v.statut.value,
        'agent': v.agent.get_full_name() if v.agent else 'Non assigné'
    } for v in visites])

@admin_bp.route('/api/demandes-retardees')
@login_required
@admin_required
def api_demandes_retardees():
    """API pour les demandes en retard"""
    from app.services.visite_service import VisiteService
    
    demandes = VisiteService.get_demandes_retardees()
    return jsonify([{
        'id': d.id,
        'nom_contact': d.nom_contact,
        'date': d.get_date_display(),
        'heure': d.get_heure_display(),
        'bien_titre': d.bien.titre if d.bien else '',
        'telephone': d.telephone_contact
    } for d in demandes]) 