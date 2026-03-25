# EduCRM – Application de gestion scolaire

## Description

EduCRM est une application web développée avec Flask permettant de gérer les étudiants, enseignants, cours, avec un système d'authentification complet et un tableau de bord interactif.
Les données sont stockées dans des fichiers JSON afin de simuler une base de données et faciliter une évolution future vers une base relationnelle.

## Objectif

Ce projet vise à mettre en place une application de gestion scolaire modulaire en respectant une architecture professionnelle basée sur les Blueprints et la séparation des responsabilités (routes, services, templates). Il simule le fonctionnement réel d’un système académique.

---

## Équipe et rôles

| Étudiant                  | Module    | Responsabilités                                                        |
| ------------------------- | --------- | ---------------------------------------------------------------------- |
| Dieynaba Ba               | AUTH      | Login, Logout, Register, gestion des sessions, sécurisation des routes |
| Ndeye Oumy Ndoye          | STUDENTS  | CRUD étudiants, recherche, pagination, validation                      |
| Ndeye Yacine Ba           | TEACHERS  | CRUD enseignants, filtrage, recherche                                  |
| Marie Diagne              | COURSES   | Création des routes, intégration des cours, inscription                |
| Mame Khary Gueye          | COURSES   | Gestion du planning, logique métier, relations                         |
| Hadja Oumou Koultoumi Bah | DASHBOARD | Interface utilisateur, tableau de bord, statistiques                   |

---

## Architecture

```
app/
├── auth/              # Authentification
├── students/          # Étudiants
├── teachers/          # Enseignants
├── courses/           # Cours
├── dashboard/         # Accueil
├── announcements/     # Bonus: Annonces
├── classes/           # Bonus: Classes
├── rooms/             # Bonus: Salles
├── data/              # Stockage JSON
├── templates/         # Templates HTML
└── static/            # Fichiers CSS/JS
```

---

## Installation

```bash
# 1. Cloner le projet
git clone https://github.com/Kharygueye05/Projet-Flask.git
cd edu.crm-main

# 2. Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate

# 3. Installer les dépendances
pip install flask

# 4. Lancer l'application
python run.py
```

Accès : [http://localhost:5000](http://localhost:5000)

---

## Fonctionnalités principales

| Module    | Fonctionnalités                                   |
| --------- | ------------------------------------------------- |
| AUTH      | Authentification, sessions, protection des routes |
| STUDENTS  | Gestion des étudiants, recherche, pagination      |
| TEACHERS  | Gestion des enseignants, filtrage                 |
| COURSES   | Gestion des cours, relations, inscriptions        |
| DASHBOARD | Tableau de bord, statistiques, navigation         |
| BONUS     | Classes, salles, annonces                         |

---

## Fonctionnalités supplémentaires

L’application a été enrichie avec plusieurs fonctionnalités au-delà du cahier de base :

* Inscription : les utilisateurs peuvent créer leur propre compte
* Profil utilisateur : modification des informations personnelles et du mot de passe
* Recherche : dans les modules étudiants, enseignants et cours
* Filtres : par spécialité pour les enseignants
* Pagination : pour la liste des étudiants
* Planning : affichage d’un planning fictif pour chaque cours
* Graphiques : visualisation du nombre d’étudiants par cours avec Chart.js
* Interface moderne : utilisation de Tailwind CSS et Font Awesome

---

## Structure des données

Les données sont stockées dans le dossier app/data/ :

* users.json : comptes utilisateurs
* students.json : étudiants
* teachers.json : enseignants
* courses.json : cours
* classes.json : classes
* rooms.json : salles
* announcements.json : annonces
* sessions.json : planning

---

## Routes principales

AUTH

* POST /auth/login
* POST /auth/logout
* POST /auth/register
* GET /auth/profile

STUDENTS

* GET /students/
* POST /students/create
* POST /students/edit/<id>
* POST /students/delete/<id>

TEACHERS

* GET /teachers/
* POST /teachers/create
* POST /teachers/edit/<id>
* POST /teachers/delete/<id>
* GET /teachers/search

COURSES

* GET /courses/
* POST /courses/create
* POST /courses/edit/<id>
* GET /courses/schedule
* POST /courses/assign

DASHBOARD

* GET /
* GET /dashboard

---

## Choix techniques

* Utilisation du pattern Application Factory pour une meilleure organisation
* Séparation claire entre routes, services et templates
* Utilisation des Blueprints pour modulariser l’application
* Stockage JSON pour simplifier le développement

---

## Phases de développement

| Phase | Contenu                                                    |
| ----- | ---------------------------------------------------------- |
| 1     | Application Factory, Blueprints, configuration             |
| 2     | AUTH, STUDENTS, TEACHERS, COURSES, DASHBOARD               |
| 3     | ANNOUNCEMENTS, CLASSES, ROOMS                              |
| 4     | Interface utilisateur (Tailwind CSS), navigation, messages |
| 5     | Tests, validation, documentation                           |

---

## Conclusion

Ce projet propose une architecture modulaire et évolutive. Il met en œuvre les bonnes pratiques de développement avec Flask et intègre des fonctionnalités permettant de simuler un système de gestion scolaire réaliste.
