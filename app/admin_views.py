from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.models.bien import Bien
from app.models.demande_visite import DemandeVisite, StatutDemande
from app import db
from datetime import datetime

class BienAdminView(ModelView):
    """Vue personnalisée pour l'administration des biens"""
    
    column_list = ['reference', 'titre', 'type_bien', 'type_transaction', 'ville', 'prix_vente', 'prix_location', 'disponible', 'actions']
    column_searchable_list = ['reference', 'titre', 'ville', 'adresse']
    column_filters = ['type_bien', 'type_transaction', 'disponible', 'ville']
    column_editable_list = ['disponible']
    
    def _format_prix(self, context, model, name):
        """Formate l'affichage du prix"""
        if model.type_transaction.value == 'vente' and model.prix_vente:
            return f"{model.prix_vente:,.0f} FCFA"
        elif model.type_transaction.value == 'location' and model.prix_location:
            return f"{model.prix_location:,.0f} FCFA/mois"
        return "Prix sur demande"
    
    def _format_actions(self, context, model, name):
        """Formate les actions pour chaque ligne"""
        return f'''
        <a href="{url_for('main.demande_visite_form', bien_id=model.id)}" class="btn btn-sm btn-success" title="Demander une visite">
            <i class="fas fa-calendar-plus"></i>
        </a>
        <a href="{url_for('biens.detail', bien_id=model.id)}" class="btn btn-sm btn-info" title="Voir détails">
            <i class="fas fa-eye"></i>
        </a>
        '''
    
    column_formatters = {
        'prix_vente': _format_prix,
        'prix_location': _format_prix,
        'actions': _format_actions
    }
    
    def scaffold_list_columns(self):
        """Ajoute des colonnes personnalisées"""
        columns = super().scaffold_list_columns()
        # Ajouter la colonne actions
        columns['actions'] = self._format_actions
        return columns
    
    def get_list(self, page, sort_field, sort_desc, search, filters, page_size=None):
        """Personnalise la liste avec des actions supplémentaires"""
        result = super().get_list(page, sort_field, sort_desc, search, filters, page_size)
        return result

class DemandeVisiteAdminView(BaseView):
    """Vue pour gérer les demandes de visite depuis l'admin"""
    
    @expose('/')
    @login_required
    def index(self):
        """Liste des demandes de visite"""
        from app.services.visite_service import VisiteService
        
        page = request.args.get('page', 1, type=int)
        statut = request.args.get('statut', '')
        
        filters = {}
        if statut:
            filters['statut'] = statut
        
        demandes = VisiteService.get_all_demandes(page=page, filters=filters)
        
        return self.render('admin/demandes_visite.html', demandes=demandes)
    
    @expose('/<int:demande_id>/confirmer', methods=['POST'])
    @login_required
    def confirmer(self, demande_id):
        """Confirmer une demande de visite"""
        from app.services.visite_service import VisiteService
        
        duree = request.form.get('duree', 60, type=int)
        VisiteService.confirmer_demande(demande_id, current_user.id, duree_estimee=duree)
        flash('Visite confirmée avec succès !', 'success')
        return redirect(url_for('demandevisiteadmin.index'))
    
    @expose('/<int:demande_id>/annuler', methods=['POST'])
    @login_required
    def annuler(self, demande_id):
        """Annuler une demande de visite"""
        from app.services.visite_service import VisiteService
        
        VisiteService.annuler_demande(demande_id)
        flash('Visite annulée avec succès !', 'success')
        return redirect(url_for('demandevisiteadmin.index')) 