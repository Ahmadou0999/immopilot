from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.forms.bien_forms import BienForm, BienSearchForm
from app.services.bien_service import BienService
from app.services.client_service import ClientService
from app import csrf

biens_bp = Blueprint('biens', __name__, url_prefix='/biens')

@biens_bp.route('/')
def index():
    """Liste des biens disponibles"""
    page = request.args.get('page', 1, type=int)
    form = BienSearchForm()
    
    # Récupérer les filtres depuis l'URL
    filters = {}
    if form.type_bien.data:
        filters['type_bien'] = form.type_bien.data
    if form.type_transaction.data:
        filters['type_transaction'] = form.type_transaction.data
    if form.ville.data:
        filters['ville'] = form.ville.data
    if form.code_postal.data:
        filters['code_postal'] = form.code_postal.data
    if form.prix_min.data:
        filters['prix_min'] = form.prix_min.data
    if form.prix_max.data:
        filters['prix_max'] = form.prix_max.data
    if form.surface_min.data:
        filters['surface_min'] = form.surface_min.data
    if form.nombre_pieces_min.data:
        filters['nombre_pieces_min'] = form.nombre_pieces_min.data
    
    biens = BienService.get_all_biens(page=page, filters=filters)
    
    return render_template('biens/index.html', biens=biens, form=form, title='Nos biens')

@biens_bp.route('/<int:bien_id>')
def detail(bien_id):
    """Détail d'un bien"""
    bien = BienService.get_bien_by_id(bien_id)
    
    # Récupérer les demandes de visite pour ce bien
    from app.services.visite_service import VisiteService
    demandes_visite = VisiteService.get_demandes_by_bien(bien_id, page=1, per_page=5)
    
    # Récupérer les contrats pour ce bien
    from app.services.contrat_service import ContratService
    contrats = ContratService.get_contrats_by_bien(bien_id, page=1, per_page=5)
    
    return render_template('biens/detail.html', 
                         bien=bien, 
                         demandes_visite=demandes_visite,
                         contrats=contrats,
                         title=bien.titre)

@biens_bp.route('/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    """Ajouter un nouveau bien"""
    form = BienForm()
    
    if form.validate_on_submit():
        data = {
            'reference': form.reference.data,
            'titre': form.titre.data,
            'description': form.description.data,
            'type_bien': form.type_bien.data,
            'type_transaction': form.type_transaction.data,
            'adresse': form.adresse.data,
            'ville': form.ville.data,
            'code_postal': form.code_postal.data,
            'quartier': form.quartier.data,
            'surface_habitable': form.surface_habitable.data,
            'surface_terrain': form.surface_terrain.data,
            'nombre_pieces': form.nombre_pieces.data,
            'nombre_chambres': form.nombre_chambres.data,
            'nombre_salles_bain': form.nombre_salles_bain.data,
            'nombre_etages': form.nombre_etages.data,
            'etage': form.etage.data,
            'annee_construction': form.annee_construction.data,
            'classe_energie': form.classe_energie.data,
            'emission_ges': form.emission_ges.data,
            'prix_vente': form.prix_vente.data,
            'prix_location': form.prix_location.data,
            'charges': form.charges.data,
            'taxe_fonciere': form.taxe_fonciere.data,
            'etat': form.etat.data,
            'disponible': form.disponible.data,
            'date_disponibilite': form.date_disponibilite.data,
            'equipements': form.equipements.data,
            'points_forts': form.points_forts.data,
            'points_faibles': form.points_faibles.data,
            'notes_agent': form.notes_agent.data
        }
        
        bien = BienService.create_bien(data, current_user.id)
        flash(f'Bien "{bien.titre}" ajouté avec succès !', 'success')
        return redirect(url_for('biens.detail', bien_id=bien.id))
    
    return render_template('biens/form.html', form=form, title='Ajouter un bien')

@biens_bp.route('/<int:bien_id>/modifier', methods=['GET', 'POST'])
@login_required
def modifier(bien_id):
    """Modifier un bien existant"""
    bien = BienService.get_bien_by_id(bien_id)
    
    # Vérifier que l'agent peut modifier ce bien
    if bien.agent_id != current_user.id and not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à modifier ce bien.', 'danger')
        return redirect(url_for('biens.detail', bien_id=bien.id))
    
    form = BienForm(obj=bien)
    
    if form.validate_on_submit():
        data = {
            'reference': form.reference.data,
            'titre': form.titre.data,
            'description': form.description.data,
            'type_bien': form.type_bien.data,
            'type_transaction': form.type_transaction.data,
            'adresse': form.adresse.data,
            'ville': form.ville.data,
            'code_postal': form.code_postal.data,
            'quartier': form.quartier.data,
            'surface_habitable': form.surface_habitable.data,
            'surface_terrain': form.surface_terrain.data,
            'nombre_pieces': form.nombre_pieces.data,
            'nombre_chambres': form.nombre_chambres.data,
            'nombre_salles_bain': form.nombre_salles_bain.data,
            'nombre_etages': form.nombre_etages.data,
            'etage': form.etage.data,
            'annee_construction': form.annee_construction.data,
            'classe_energie': form.classe_energie.data,
            'emission_ges': form.emission_ges.data,
            'prix_vente': form.prix_vente.data,
            'prix_location': form.prix_location.data,
            'charges': form.charges.data,
            'taxe_fonciere': form.taxe_fonciere.data,
            'etat': form.etat.data,
            'disponible': form.disponible.data,
            'date_disponibilite': form.date_disponibilite.data,
            'equipements': form.equipements.data,
            'points_forts': form.points_forts.data,
            'points_faibles': form.points_faibles.data,
            'notes_agent': form.notes_agent.data
        }
        
        BienService.update_bien(bien_id, data)
        flash(f'Bien "{bien.titre}" modifié avec succès !', 'success')
        return redirect(url_for('biens.detail', bien_id=bien.id))
    
    return render_template('biens/form.html', form=form, bien=bien, title='Modifier le bien')

@biens_bp.route('/<int:bien_id>/supprimer', methods=['POST'])
@login_required
@csrf.exempt
def supprimer(bien_id):
    """Supprimer un bien"""
    bien = BienService.get_bien_by_id(bien_id)
    
    # Vérifier que l'agent peut supprimer ce bien
    if bien.agent_id != current_user.id and not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à supprimer ce bien.', 'danger')
        return redirect(url_for('biens.detail', bien_id=bien.id))
    
    titre = bien.titre
    BienService.delete_bien(bien_id)
    flash(f'Bien "{titre}" supprimé avec succès !', 'success')
    return redirect(url_for('biens.index'))

@biens_bp.route('/mes-biens')
@login_required
def mes_biens():
    """Liste des biens de l'agent connecté"""
    page = request.args.get('page', 1, type=int)
    biens = BienService.get_biens_by_agent(current_user.id, page=page)
    
    return render_template('biens/mes_biens.html', biens=biens, title='Mes biens')

@biens_bp.route('/api/search')
def api_search():
    """API de recherche AJAX"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        biens = BienService.search_biens(query, page=page)
    else:
        biens = BienService.get_all_biens(page=page)
    
    return jsonify({
        'biens': [{
            'id': b.id,
            'titre': b.titre,
            'reference': b.reference,
            'ville': b.ville,
            'prix': b.get_price_display(),
            'surface': b.get_surface_display(),
            'type_bien': b.type_bien.value,
            'type_transaction': b.type_transaction.value,
            'disponible': b.disponible
        } for b in biens.items],
        'total': biens.total,
        'pages': biens.pages,
        'current_page': biens.page
    }) 