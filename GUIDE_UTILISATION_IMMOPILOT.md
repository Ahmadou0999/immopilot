# 🏠 GUIDE D'UTILISATION COMPLET - IMMOPILOT

## 📋 Table des matières
1. [Présentation de l'application](#présentation)
2. [Rôles et permissions](#rôles)
3. [Guide d'utilisation par rôle](#guide-par-rôle)
4. [Cas pratique complet](#cas-pratique)
5. [Fonctionnalités avancées](#fonctionnalités-avancées)
6. [Dépannage](#dépannage)

---

## 🎯 Présentation de l'application {#présentation}

**ImmoPilot** est une application web de gestion immobilière complète permettant aux agences immobilières de gérer leurs biens, clients, contrats et visites. L'application offre une interface moderne et intuitive pour optimiser le workflow des agents immobiliers.

### 🏗️ Architecture de l'application
- **Framework** : Flask (Python)
- **Base de données** : MySQL avec SQLAlchemy
- **Interface** : Bootstrap 4 avec templates Jinja2
- **Authentification** : Flask-Login avec gestion des rôles
- **Administration** : Flask-Admin intégré

### 📊 Modules principaux
- **Gestion des biens** : Création, modification, recherche de biens immobiliers
- **Gestion des clients** : Base de données clients et prospects
- **Gestion des contrats** : Contrats de vente et location
- **Gestion des visites** : Planification et suivi des visites
- **Administration** : Gestion des agents et statistiques

---

## 👥 Rôles et permissions {#rôles}

### 🔐 Agent Immobilier (Rôle standard)
**Permissions :**
- ✅ Connexion à l'application
- ✅ Gestion de ses propres biens
- ✅ Gestion de ses clients
- ✅ Création et suivi de contrats
- ✅ Gestion des demandes de visite
- ✅ Accès au tableau de bord personnel
- ✅ Modification de son profil

**Limitations :**
- ❌ Pas d'accès à l'administration
- ❌ Pas de gestion des autres agents
- ❌ Pas d'accès aux statistiques globales

### 🛡️ Administrateur
**Permissions :**
- ✅ Toutes les permissions d'un agent
- ✅ Gestion complète des agents (création, activation, promotion)
- ✅ Accès aux statistiques globales
- ✅ Gestion de toutes les visites
- ✅ Accès au dashboard administrateur
- ✅ Génération de rapports
- ✅ Configuration système

**Fonctionnalités exclusives :**
- 🔧 Panel d'administration complet
- 📊 Statistiques détaillées
- 👥 Gestion des équipes
- 📈 Rapports de performance

---

## 📖 Guide d'utilisation par rôle {#guide-par-rôle}

### 🏠 Agent Immobilier

#### 1. **Connexion et premier accès**
```
URL : http://localhost:5000/auth/login
```
- Saisir votre email et mot de passe
- Cocher "Se souvenir de moi" si nécessaire
- Cliquer sur "Se connecter"

#### 2. **Tableau de bord personnel**
**Accès :** `/dashboard`

**Informations affichées :**
- 📊 Statistiques personnelles (biens, clients, contrats)
- 📅 Visites du jour
- ⏳ Demandes de visite en attente
- 🏠 Vos biens récents
- 📋 Vos contrats récents

#### 3. **Gestion des biens**

**Ajouter un nouveau bien :**
1. Aller dans "Biens" → "Ajouter un bien"
2. Remplir les informations obligatoires :
   - Référence unique
   - Titre du bien
   - Type de bien (appartement, maison, etc.)
   - Type de transaction (vente/location)
   - Adresse complète
3. Compléter les caractéristiques :
   - Surface habitable
   - Nombre de pièces
   - Prix
   - Équipements
4. Ajouter des photos (URLs)
5. Cliquer sur "Enregistrer"

**Modifier un bien :**
1. Aller dans "Biens" → Liste des biens
2. Cliquer sur le bien à modifier
3. Cliquer sur "Modifier"
4. Apporter les modifications
5. Sauvegarder

**Marquer un bien comme vendu/loué :**
1. Aller dans le détail du bien
2. Cliquer sur "Marquer comme vendu/loué"
3. Le bien devient indisponible automatiquement

#### 4. **Gestion des clients**

**Ajouter un nouveau client :**
1. Aller dans "Clients" → "Ajouter un client"
2. Remplir les informations :
   - Nom et prénom
   - Email (unique)
   - Téléphone
   - Adresse
   - Budget (min/max)
   - Type de recherche
3. Sauvegarder

**Suivre un prospect :**
1. Dans la liste des clients, identifier les prospects
2. Ajouter des notes sur les interactions
3. Mettre à jour les préférences
4. Convertir en client actif quand nécessaire

#### 5. **Gestion des contrats**

**Créer un contrat :**
1. Aller dans "Contrats" → "Nouveau contrat"
2. Sélectionner le client
3. Sélectionner le bien
4. Remplir les informations financières :
   - Montant
   - Frais d'agence
   - Charges (si location)
5. Définir les dates importantes
6. Ajouter des conditions particulières
7. Sauvegarder

**Suivre l'état d'un contrat :**
- **En cours** : Contrat en négociation
- **Signé** : Contrat finalisé
- **Annulé** : Contrat abandonné
- **Terminé** : Contrat clos

#### 6. **Gestion des visites**

**Planifier une visite :**
1. Aller dans "Visites" → "Nouvelle visite"
2. Sélectionner le bien
3. Choisir la date et l'heure
4. Ajouter les informations du visiteur
5. Confirmer la visite

**Suivre les demandes de visite :**
1. Consulter les demandes en attente
2. Confirmer ou proposer d'autres créneaux
3. Ajouter des notes après la visite
4. Marquer comme terminée

### 🛡️ Administrateur

#### 1. **Accès au panel d'administration**
**URL :** `/admin` ou `/flaskadmin`

#### 2. **Dashboard administrateur**
**Accès :** `/admin/dashboard`

**Fonctionnalités :**
- 📊 Statistiques globales de l'agence
- 👥 État des agents (connectés aujourd'hui)
- 📅 Visites du jour (toutes agences)
- ⚠️ Demandes en retard
- 📈 Performance globale

#### 3. **Gestion des agents**

**Créer un nouvel agent :**
1. Aller dans "Administration" → "Agents"
2. Cliquer sur "Ajouter un agent"
3. Remplir les informations :
   - Nom et prénom
   - Email (unique)
   - Téléphone
   - Mot de passe temporaire
4. L'agent recevra un email d'activation

**Gérer les droits :**
- **Activer/Désactiver** : Contrôler l'accès
- **Promouvoir admin** : Donner les droits administrateur
- **Retirer admin** : Retirer les droits administrateur

**Surveiller l'activité :**
- Voir les dernières connexions
- Consulter les statistiques par agent
- Identifier les agents inactifs

#### 4. **Gestion globale des visites**

**Accès :** `/admin/visites`

**Fonctionnalités :**
- Voir toutes les demandes de visite
- Filtrer par statut
- Réassigner des visites
- Gérer les conflits d'horaires
- Générer des rapports de visite

#### 5. **Rapports et statistiques**

**Types de rapports disponibles :**
- 📊 Performance des agents
- 🏠 Biens les plus visités
- 💰 Chiffre d'affaires
- 📅 Taux de conversion des visites
- 👥 Évolution de la clientèle

---

## 🎯 Cas pratique complet : De A à Z {#cas-pratique}

### 📖 Scénario : Vente d'un appartement à Paris

**Contexte :** Marie Dupont, agent immobilier chez ImmoPilot, doit gérer la vente d'un appartement 3 pièces dans le 16ème arrondissement de Paris.

---

### **Étape 1 : Création du bien** 🏠

**Marie se connecte à l'application :**
```
URL : http://localhost:5000/auth/login
Email : marie.dupont@immopilot.fr
Mot de passe : ********
```

**Elle ajoute le nouveau bien :**
1. **Navigation :** Dashboard → Biens → "Ajouter un bien"
2. **Informations de base :**
   - Référence : `APP-16-2024-001`
   - Titre : "Appartement 3 pièces - 16ème arrondissement"
   - Type : Appartement
   - Transaction : Vente
   - Adresse : 45 Avenue Victor Hugo
   - Ville : Paris
   - Code postal : 75016

3. **Caractéristiques :**
   - Surface habitable : 85 m²
   - Surface terrain : 0 m²
   - Nombre de pièces : 3
   - Nombre de chambres : 2
   - Nombre de salles de bain : 1
   - Étage : 4ème
   - Année de construction : 1985

4. **Énergie :**
   - Classe énergétique : C
   - Émission GES : D

5. **Prix :**
   - Prix de vente : 850 000 €
   - Taxe foncière : 3 200 €/an

6. **État et disponibilité :**
   - État : Excellent
   - Disponible : Oui
   - Date de disponibilité : Immédiat

7. **Informations supplémentaires :**
   - Équipements : "Cuisine équipée, cave, parking"
   - Points forts : "Vue dégagée, calme, proche transports"
   - Notes agent : "Bien entretenu, propriétaire motivé"

8. **Images :** Ajout des URLs des photos

**Résultat :** Le bien est créé et visible dans le catalogue.

---

### **Étape 2 : Gestion des demandes de visite** 📅

**Une demande de visite arrive via le site web :**

**Informations reçues :**
- Nom : Jean Martin
- Téléphone : 06.12.34.56.78
- Email : jean.martin@email.com
- Date souhaitée : 15/01/2024
- Heure souhaitée : 14:00
- Commentaires : "Intéressé par l'appartement, budget 800k-900k"

**Marie traite la demande :**
1. **Navigation :** Dashboard → Demandes en attente
2. **Action :** Cliquer sur "Confirmer la visite"
3. **Détails :**
   - Durée estimée : 45 minutes
   - Notes : "Client sérieux, budget compatible"

**Résultat :** La visite est confirmée et planifiée.

---

### **Étape 3 : Création du client** 👤

**Après la visite, Marie crée le profil client :**

1. **Navigation :** Clients → "Ajouter un client"
2. **Informations :**
   - Nom : Martin
   - Prénom : Jean
   - Email : jean.martin@email.com
   - Téléphone : 06.12.34.56.78
   - Adresse : 12 Rue de la Paix, 75001 Paris
   - Budget min : 800 000 €
   - Budget max : 900 000 €
   - Type de recherche : Vente
   - Notes : "Intéressé par l'appartement Victor Hugo, visite positive"

3. **Statut :** Prospect (pas encore client actif)

**Résultat :** Le client est ajouté à la base de données.

---

### **Étape 4 : Négociation et suivi** 💬

**Marie ajoute des notes de suivi :**
1. **Navigation :** Clients → Jean Martin → "Modifier"
2. **Notes ajoutées :**
   - "15/01/2024 : Visite effectuée, client très intéressé"
   - "16/01/2024 : Appel de suivi, client demande des documents"
   - "18/01/2024 : Envoi du diagnostic énergétique"
   - "20/01/2024 : Client propose 820 000 €"

**Mise à jour du bien :**
1. **Navigation :** Biens → APP-16-2024-001 → "Modifier"
2. **Notes agent :** "Négociation en cours avec M. Martin, offre à 820k"

---

### **Étape 5 : Création du contrat** 📋

**Le client accepte le prix de 830 000 € :**

1. **Navigation :** Contrats → "Nouveau contrat"
2. **Informations du contrat :**
   - Numéro : `CONTRAT-2024-001`
   - Type : Vente
   - Client : Jean Martin
   - Bien : APP-16-2024-001
   - Montant : 830 000 €
   - Frais d'agence : 24 900 € (3%)
   - Date de signature prévue : 15/02/2024
   - Date d'entrée : 01/04/2024

3. **Conditions particulières :**
   - "Vente sous réserve de financement"
   - "Acte de vente chez le notaire"

**Résultat :** Le contrat est créé avec le statut "En cours".

---

### **Étape 6 : Finalisation de la vente** ✅

**Le contrat est signé :**

1. **Navigation :** Contrats → CONTRAT-2024-001 → "Modifier"
2. **Actions :**
   - Cliquer sur "Marquer comme signé"
   - Date de signature : 15/02/2024
   - Statut : Signé

**Mise à jour automatique :**
- Le bien devient indisponible
- Le client passe de "Prospect" à "Client actif"
- Les statistiques sont mises à jour

---

### **Étape 7 : Suivi post-vente** 📊

**Marie finalise le dossier :**

1. **Navigation :** Contrats → CONTRAT-2024-001
2. **Actions :**
   - Ajouter des notes : "Acte signé, dossier clos"
   - Marquer comme "Terminé" après l'entrée dans les lieux

**Résultat :** Le dossier est complètement finalisé.

---

## 🚀 Fonctionnalités avancées {#fonctionnalités-avancées}

### 📊 Tableau de bord intelligent
- **Statistiques en temps réel**
- **Alertes automatiques** (visites en retard, contrats à signer)
- **Graphiques de performance**
- **Notifications push**

### 🔍 Recherche avancée
- **Filtres multiples** (prix, surface, localisation)
- **Recherche géolocalisée**
- **Sauvegarde de recherches favorites**
- **Alertes automatiques** pour nouveaux biens

### 📱 Interface responsive
- **Compatible mobile** et tablette
- **Application web progressive** (PWA)
- **Synchronisation hors ligne**

### 📧 Communication intégrée
- **Emails automatiques** (confirmations, rappels)
- **SMS de rappel** pour les visites
- **Notifications push** dans le navigateur

### 📈 Rapports et analytics
- **Rapports de performance** par agent
- **Analyse de la clientèle**
- **Prévisions de vente**
- **Export PDF/Excel**

---

## 🔧 Dépannage {#dépannage}

### Problèmes de connexion
**Symptôme :** Impossible de se connecter
**Solutions :**
1. Vérifier l'email et le mot de passe
2. Contacter l'administrateur si le compte est désactivé
3. Utiliser "Mot de passe oublié" si disponible

### Problèmes de performance
**Symptôme :** Application lente
**Solutions :**
1. Vider le cache du navigateur
2. Fermer les onglets inutiles
3. Vérifier la connexion internet

### Erreurs de sauvegarde
**Symptôme :** Impossible de sauvegarder
**Solutions :**
1. Vérifier que tous les champs obligatoires sont remplis
2. Vérifier la connexion à la base de données
3. Contacter le support technique

### Problèmes d'affichage
**Symptôme :** Interface déformée
**Solutions :**
1. Actualiser la page (F5)
2. Vérifier la résolution d'écran
3. Utiliser un navigateur récent (Chrome, Firefox, Safari)

---

## 📞 Support et contact

### 🆘 Support technique
- **Email :** support@immopilot.fr
- **Téléphone :** 01 23 45 67 89
- **Horaires :** Lundi-Vendredi 9h-18h

### 📚 Documentation
- **Guide utilisateur :** Disponible dans l'application
- **FAQ :** Section Aide dans le menu
- **Tutoriels vidéo :** Chaîne YouTube ImmoPilot

### 🔄 Mises à jour
- **Version actuelle :** 1.0.0
- **Dernière mise à jour :** Janvier 2024
- **Prochaines fonctionnalités :** Application mobile native

---

## 📝 Notes importantes

### 🔐 Sécurité
- **Changement de mot de passe** : Obligatoire tous les 90 jours
- **Déconnexion automatique** : Après 30 minutes d'inactivité
- **Sauvegarde automatique** : Toutes les 5 minutes

### 💾 Sauvegarde des données
- **Sauvegarde automatique** quotidienne
- **Rétention** : 7 ans pour les contrats, 3 ans pour les visites
- **Export** : Disponible sur demande

### 📋 Conformité RGPD
- **Consentement** obligatoire pour les données personnelles
- **Droit à l'oubli** : Demande via le support
- **Portabilité** : Export des données personnelles

---

*Ce guide est régulièrement mis à jour. Dernière version : Janvier 2024* 