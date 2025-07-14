from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth_forms import LoginForm, RegisterForm, ChangePasswordForm
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        agent = AuthService.authenticate_user(form.email.data, form.password.data)
        
        if agent:
            AuthService.login_user(agent, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
            flash('Connexion réussie !', 'success')
            return redirect(next_page)
        else:
            flash('Email ou mot de passe incorrect.', 'danger')
    
    return render_template('auth/login.html', form=form, title='Connexion')

@auth_bp.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    AuthService.logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Page d'inscription (réservée aux admins)"""
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        agent, message = AuthService.register_agent({
            'nom': form.nom.data,
            'prenom': form.prenom.data,
            'email': form.email.data,
            'telephone': form.telephone.data,
            'password': form.password.data,
            'is_admin': False
        })
        
        if agent:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
    
    return render_template('auth/register.html', form=form, title='Inscription')

@auth_bp.route('/profile')
@login_required
def profile():
    """Page de profil de l'utilisateur"""
    return render_template('auth/profile.html', title='Mon Profil')

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Changement de mot de passe"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        success, message = AuthService.change_password(
            current_user.id,
            form.current_password.data,
            form.new_password.data
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash(message, 'danger')
    
    return render_template('auth/change_password.html', form=form, title='Changer le mot de passe') 