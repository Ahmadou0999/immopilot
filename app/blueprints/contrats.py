from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.forms.contrat_forms import ContratForm
from app.services.contrat_service import ContratService
from app.services.client_service import ClientService
from app.services.bien_service import BienService
from app import csrf

contrats_bp = Blueprint('contrats', __name__, url_prefix='/contrats')

@contrats_bp.route('/')
@login_required
def index():
    """Liste des contrats"""
    page = request.args.get('page', 1, type=int)
    type_contrat = request.args.get('type', '')
    statut = request.args.get('statut', '')
    
    filters = {}
    if type_contrat:
        filters['type_contrat'] = type_contrat
    if statut:
        filters['statut'] = statut
    
    contrats = ContratService.get_all_contrats(page=page, filters=filters)
    
    return render_template('contrats/index.html', contrats=contrats, title='Contrats')

@contrats_bp.route('/<int:contrat_id>')
@login_required
def detail(contrat_id):
    """Détail d'un contrat"""
    contrat = ContratService.get_contrat_by_id(contrat_id)
    
    return render_template('contrats/detail.html', 
                         contrat=contrat,
                         title=f'Contrat {contrat.numero}')

@contrats_bp.route('/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    """Ajouter un nouveau contrat"""
    form = ContratForm()
    
    # Récupérer les listes pour les select
    clients = ClientService.get_clients()
    biens = BienService.get_biens_disponibles()
    
    if form.validate_on_submit():
        data = {
            'numero': form.numero.data,
            'type_contrat': form.type_contrat.data,
            'montant': form.montant.data,
            'client_id': request.form.get('client_id'),
            'bien_id': request.form.get('bien_id'),
            'frais_agence': form.frais_agence.data,
            'charges': form.charges.data,
            'caution': form.caution.data,
            'date_entree': form.date_entree.data,
            'date_sortie': form.date_sortie.data,
            'date_fin_bail': form.date_fin_bail.data,
            'duree_bail': form.duree_bail.data,
            'conditions_particulieres': form.conditions_particulieres.data,
            'notes': form.notes.data
        }
        
        contrat = ContratService.create_contrat(data, current_user.id)
        flash(f'Contrat "{contrat.numero}" créé avec succès !', 'success')
        return redirect(url_for('contrats.detail', contrat_id=contrat.id))
    
    return render_template('contrats/form.html', 
                         form=form, 
                         clients=clients,
                         biens=biens,
                         title='Créer un contrat')

@contrats_bp.route('/<int:contrat_id>/modifier', methods=['GET', 'POST'])
@login_required
def modifier(contrat_id):
    """Modifier un contrat existant"""
    contrat = ContratService.get_contrat_by_id(contrat_id)
    
    # Vérifier que l'agent peut modifier ce contrat
    if contrat.agent_id != current_user.id and not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à modifier ce contrat.', 'danger')
        return redirect(url_for('contrats.detail', contrat_id=contrat.id))
    
    form = ContratForm(obj=contrat)
    
    # Récupérer les listes pour les select
    clients = ClientService.get_clients()
    biens = BienService.get_biens_disponibles()
    
    if form.validate_on_submit():
        data = {
            'numero': form.numero.data,
            'type_contrat': form.type_contrat.data,
            'montant': form.montant.data,
            'frais_agence': form.frais_agence.data,
            'charges': form.charges.data,
            'caution': form.caution.data,
            'date_entree': form.date_entree.data,
            'date_sortie': form.date_sortie.data,
            'date_fin_bail': form.date_fin_bail.data,
            'duree_bail': form.duree_bail.data,
            'conditions_particulieres': form.conditions_particulieres.data,
            'notes': form.notes.data
        }
        
        ContratService.update_contrat(contrat_id, data)
        flash(f'Contrat "{contrat.numero}" modifié avec succès !', 'success')
        return redirect(url_for('contrats.detail', contrat_id=contrat.id))
    
    return render_template('contrats/form.html', 
                         form=form, 
                         contrat=contrat,
                         clients=clients,
                         biens=biens,
                         title='Modifier le contrat')

@contrats_bp.route('/<int:contrat_id>/supprimer', methods=['POST'])
@login_required
def supprimer(contrat_id):
    """Supprimer un contrat"""
    contrat = ContratService.get_contrat_by_id(contrat_id)
    
    # Vérifier que l'agent peut supprimer ce contrat
    if contrat.agent_id != current_user.id and not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à supprimer ce contrat.', 'danger')
        return redirect(url_for('contrats.detail', contrat_id=contrat.id))
    
    numero = contrat.numero
    ContratService.delete_contrat(contrat_id)
    flash(f'Contrat "{numero}" supprimé avec succès !', 'success')
    return redirect(url_for('contrats.index'))

@contrats_bp.route('/<int:contrat_id>/signer', methods=['POST'])
@login_required
def signer(contrat_id):
    """Signer un contrat"""
    contrat = ContratService.get_contrat_by_id(contrat_id)
    
    # Vérifier que l'agent peut signer ce contrat
    if contrat.agent_id != current_user.id and not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à signer ce contrat.', 'danger')
        return redirect(url_for('contrats.detail', contrat_id=contrat.id))
    
    ContratService.signer_contrat(contrat_id)
    flash(f'Contrat "{contrat.numero}" signé avec succès !', 'success')
    return redirect(url_for('contrats.detail', contrat_id=contrat.id))

@contrats_bp.route('/<int:contrat_id>/annuler', methods=['POST'])
@login_required
def annuler(contrat_id):
    """Annuler un contrat"""
    contrat = ContratService.get_contrat_by_id(contrat_id)
    
    # Vérifier que l'agent peut annuler ce contrat
    if contrat.agent_id != current_user.id and not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à annuler ce contrat.', 'danger')
        return redirect(url_for('contrats.detail', contrat_id=contrat.id))
    
    ContratService.annuler_contrat(contrat_id)
    flash(f'Contrat "{contrat.numero}" annulé avec succès !', 'success')
    return redirect(url_for('contrats.detail', contrat_id=contrat.id))

@contrats_bp.route('/<int:contrat_id>/terminer', methods=['POST'])
@login_required
def terminer(contrat_id):
    """Terminer un contrat"""
    contrat = ContratService.get_contrat_by_id(contrat_id)
    
    # Vérifier que l'agent peut terminer ce contrat
    if contrat.agent_id != current_user.id and not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à terminer ce contrat.', 'danger')
        return redirect(url_for('contrats.detail', contrat_id=contrat.id))
    
    ContratService.terminer_contrat(contrat_id)
    flash(f'Contrat "{contrat.numero}" terminé avec succès !', 'success')
    return redirect(url_for('contrats.detail', contrat_id=contrat.id))

@contrats_bp.route('/mes-contrats')
@login_required
def mes_contrats():
    """Liste des contrats de l'agent connecté"""
    page = request.args.get('page', 1, type=int)
    contrats = ContratService.get_contrats_by_agent(current_user.id, page=page)
    
    return render_template('contrats/mes_contrats.html', contrats=contrats, title='Mes contrats')

@contrats_bp.route('/actifs')
@login_required
def contrats_actifs():
    """Liste des contrats actifs"""
    contrats = ContratService.get_contrats_actifs()
    return render_template('contrats/contrats_actifs.html', contrats=contrats, title='Contrats actifs')

@contrats_bp.route('/api/statistiques')
@login_required
def api_statistiques():
    """API pour les statistiques des contrats"""
    stats = ContratService.get_statistics()
    par_type = ContratService.get_contrats_par_type()
    par_statut = ContratService.get_contrats_par_statut()
    
    return jsonify({
        'general': stats,
        'par_type': par_type,
        'par_statut': par_statut
    }) 