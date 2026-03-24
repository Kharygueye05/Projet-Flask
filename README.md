# EduCRM – Application de gestion scolaire

## Description
EduCRM est une application web développée avec **Flask** permettant de gérer les étudiants, enseignants, cours, avec un système d'authentification complet et un tableau de bord interactif.  
Les données sont stockées dans des fichiers **JSON** (en mémoire) pour faciliter un passage ultérieur à une base de données.

## Membres du groupe et répartition des tâches

| Étudiant | Rôle | Tâches réalisées |
|----------|------|------------------|
| **Étudiant 1** | Authentification & Sécurité | - Blueprint `auth` : login, logout, inscription, profil utilisateur<br>- Décorateur `login_required`<br>- Gestion des sessions et flash messages<br>- Protection des routes des autres modules<br>- Fonctionnalités supplémentaires : inscription, modification de profil, changement de mot de passe |
| **Étudiant 2** | Gestion des étudiants | - Blueprint `students` : liste, ajout, modification, suppression<br>- Recherche d'étudiants<br>- Pagination de la liste<br>- Service avec stockage JSON |
| **Étudiant 3** | Gestion des enseignants | - Blueprint `teachers` : liste, ajout, modification, suppression<br>- Filtrage par spécialité<br>- Recherche<br>- Service avec stockage JSON |
| **Étudiant 4** | Gestion des cours | - Blueprint `courses` : liste, création, suppression<br>- Inscription/désinscription d'étudiants<br>- Planning des cours (généré automatiquement)<br>- Recherche par titre<br>- Collaboration avec les services étudiants et enseignants |
| **Étudiant 5** | Dashboard & UI | - Blueprint `dashboard` : page d'accueil avec statistiques<br>- Graphiques (Chart.js) : étudiants par cours<br>- Affichage des dernières activités<br>- Template `base.html` commun avec Tailwind CSS<br>- Intégration de tous les blueprints et gestion des messages flash |

## Fonctionnalités supplémentaires
- **Inscription** : les utilisateurs peuvent créer leur propre compte.
- **Profil utilisateur** : modification des informations personnelles et du mot de passe.
- **Recherche** : dans les modules étudiants, enseignants et cours.
- **Filtres** : par spécialité pour les enseignants.
- **Pagination** : pour la liste des étudiants.
- **Planning** : affichage d’un planning fictif pour chaque cours.
- **Graphiques** : visualisation du nombre d’étudiants par cours avec Chart.js.
- **Interface moderne** : utilisation de **Tailwind CSS** et **Font Awesome**.

## Installation et exécution

### Prérequis
- Python 3.8 ou supérieur
- Flask (installé via pip)

### Étapes
1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-groupe/edu_crm.git
   cd edu_crm