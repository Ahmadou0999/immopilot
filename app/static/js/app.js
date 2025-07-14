/**
 * ImmoPilot - Main JavaScript File
 * Gestion des interactions AJAX et UI
 */

// Configuration globale
const APP_CONFIG = {
    apiBaseUrl: '/api',
    csrfToken: document.querySelector('meta[name="csrf-token"]')?.getAttribute('content'),
    debug: false
};

// Utilitaires
const Utils = {
    // Afficher une notification
    showNotification: function(message, type = 'info', duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-header">
                <strong class="me-auto">ImmoPilot</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">${message}</div>
        `;
        
        const container = document.querySelector('.toast-container') || this.createToastContainer();
        container.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        setTimeout(() => {
            bsToast.hide();
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },
    
    // Créer le conteneur de notifications
    createToastContainer: function() {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    },
    
    // Formater un prix
    formatPrice: function(price, currency = '€') {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: currency
        }).format(price);
    },
    
    // Formater une date
    formatDate: function(date) {
        return new Intl.DateTimeFormat('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    // Valider un email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Gestionnaire AJAX
const AjaxManager = {
    // Requête GET
    get: function(url, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;
        
        return fetch(fullUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(this.handleResponse);
    },
    
    // Requête POST
    post: function(url, data = {}) {
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': APP_CONFIG.csrfToken
            },
            body: JSON.stringify(data)
        }).then(this.handleResponse);
    },
    
    // Requête PUT
    put: function(url, data = {}) {
        return fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': APP_CONFIG.csrfToken
            },
            body: JSON.stringify(data)
        }).then(this.handleResponse);
    },
    
    // Requête DELETE
    delete: function(url) {
        return fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': APP_CONFIG.csrfToken
            }
        }).then(this.handleResponse);
    },
    
    // Gestion de la réponse
    handleResponse: function(response) {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }
};

// API des biens
const BiensAPI = {
    // Rechercher des biens
    search: function(query, filters = {}) {
        return AjaxManager.get(`${APP_CONFIG.apiBaseUrl}/biens/search`, {
            q: query,
            ...filters
        });
    },
    
    // Obtenir les statistiques
    getStats: function() {
        return AjaxManager.get(`${APP_CONFIG.apiBaseUrl}/biens/stats`);
    },
    
    // Obtenir un bien par ID
    getById: function(id) {
        return AjaxManager.get(`${APP_CONFIG.apiBaseUrl}/biens/${id}`);
    },
    
    // Créer un bien
    create: function(data) {
        return AjaxManager.post(`${APP_CONFIG.apiBaseUrl}/biens`, data);
    },
    
    // Mettre à jour un bien
    update: function(id, data) {
        return AjaxManager.put(`${APP_CONFIG.apiBaseUrl}/biens/${id}`, data);
    },
    
    // Supprimer un bien
    delete: function(id) {
        return AjaxManager.delete(`${APP_CONFIG.apiBaseUrl}/biens/${id}`);
    }
};

// API des clients
const ClientsAPI = {
    // Rechercher des clients
    search: function(query) {
        return AjaxManager.get(`${APP_CONFIG.apiBaseUrl}/clients/search`, { q: query });
    },
    
    // Créer une demande de visite
    createVisite: function(data) {
        return AjaxManager.post(`${APP_CONFIG.apiBaseUrl}/clients/visite`, data);
    },
    
    // Obtenir les visites
    getVisites: function(filters = {}) {
        return AjaxManager.get(`${APP_CONFIG.apiBaseUrl}/clients/visites`, filters);
    }
};

// API des contrats
const ContratsAPI = {
    // Obtenir les contrats
    getAll: function(filters = {}) {
        return AjaxManager.get(`${APP_CONFIG.apiBaseUrl}/contrats`, filters);
    },
    
    // Créer un contrat
    create: function(data) {
        return AjaxManager.post(`${APP_CONFIG.apiBaseUrl}/contrats`, data);
    }
};

// Gestionnaire de recherche
const SearchManager = {
    init: function() {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            const debouncedSearch = Utils.debounce(this.performSearch.bind(this), 300);
            searchInput.addEventListener('input', debouncedSearch);
        }
    },
    
    performSearch: function(event) {
        const query = event.target.value.trim();
        const resultsContainer = document.getElementById('searchResults');
        
        if (query.length < 2) {
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
            return;
        }
        
        BiensAPI.search(query)
            .then(data => {
                this.displayResults(data.biens, resultsContainer);
            })
            .catch(error => {
                console.error('Erreur de recherche:', error);
                Utils.showNotification('Erreur lors de la recherche', 'error');
            });
    },
    
    displayResults: function(biens, container) {
        if (biens.length === 0) {
            container.innerHTML = '<div class="p-3 text-muted">Aucun résultat trouvé</div>';
        } else {
            const html = biens.map(bien => `
                <div class="search-result-item p-2 border-bottom">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${bien.titre}</strong>
                            <br>
                            <small class="text-muted">${bien.reference} - ${bien.ville}</small>
                        </div>
                        <div class="text-end">
                            <div class="text-primary">${bien.prix}</div>
                            <a href="/biens/${bien.id}" class="btn btn-sm btn-outline-primary">
                                Voir
                            </a>
                        </div>
                    </div>
                </div>
            `).join('');
            
            container.innerHTML = html;
        }
        
        container.style.display = 'block';
    }
};

// Gestionnaire de formulaires
const FormManager = {
    init: function() {
        this.initFormValidation();
        this.initAutoSave();
    },
    
    initFormValidation: function() {
        const forms = document.querySelectorAll('form[data-validate]');
        forms.forEach(form => {
            form.addEventListener('submit', this.validateForm.bind(this));
        });
    },
    
    validateForm: function(event) {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading"></span> Envoi...';
        }
        
        // Réactiver le bouton après 5 secondes au cas où
        setTimeout(() => {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Envoyer';
            }
        }, 5000);
    },
    
    initAutoSave: function() {
        const forms = document.querySelectorAll('form[data-autosave]');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            const debouncedSave = Utils.debounce(this.autoSave.bind(this), 1000);
            
            inputs.forEach(input => {
                input.addEventListener('change', debouncedSave);
                input.addEventListener('blur', debouncedSave);
            });
        });
    },
    
    autoSave: function(event) {
        const form = event.target.closest('form');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Sauvegarder dans localStorage
        const formId = form.id || 'autosave-form';
        localStorage.setItem(`autosave-${formId}`, JSON.stringify(data));
        
        Utils.showNotification('Brouillon sauvegardé', 'info', 2000);
    }
};

// Gestionnaire de notifications
const NotificationManager = {
    init: function() {
        // Afficher les notifications Flash
        const flashMessages = document.querySelectorAll('.alert');
        flashMessages.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }
};

// Gestionnaire de pagination
const PaginationManager = {
    init: function() {
        const paginationLinks = document.querySelectorAll('.pagination a');
        paginationLinks.forEach(link => {
            link.addEventListener('click', this.handlePagination.bind(this));
        });
    },
    
    handlePagination: function(event) {
        const link = event.target.closest('a');
        if (!link) return;
        
        event.preventDefault();
        
        const url = new URL(link.href);
        const currentUrl = new URL(window.location);
        
        // Mettre à jour les paramètres de pagination
        url.searchParams.forEach((value, key) => {
            currentUrl.searchParams.set(key, value);
        });
        
        // Charger la nouvelle page
        window.location.href = currentUrl.toString();
    }
};

// Initialisation de l'application
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les gestionnaires
    SearchManager.init();
    FormManager.init();
    NotificationManager.init();
    PaginationManager.init();
    
    // Initialiser les tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialiser les popovers Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Gestionnaire de confirmation de suppression
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(event) {
            const message = this.getAttribute('data-confirm') || 'Êtes-vous sûr de vouloir continuer ?';
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });
    
    // Gestionnaire de copie dans le presse-papiers
    document.querySelectorAll('[data-copy]').forEach(element => {
        element.addEventListener('click', function(event) {
            event.preventDefault();
            const text = this.getAttribute('data-copy');
            navigator.clipboard.writeText(text).then(() => {
                Utils.showNotification('Copié dans le presse-papiers', 'success', 2000);
            });
        });
    });
    
    if (APP_CONFIG.debug) {
        console.log('ImmoPilot initialisé avec succès');
    }
});

// Export pour utilisation globale
window.ImmoPilot = {
    Utils,
    AjaxManager,
    BiensAPI,
    ClientsAPI,
    ContratsAPI,
    SearchManager,
    FormManager,
    NotificationManager,
    PaginationManager
}; 