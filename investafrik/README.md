# 🚀 InvestAfrik - Plateforme de Crowdfunding Africaine

[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4+-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Description

InvestAfrik est une plateforme de crowdfunding moderne dédiée aux projets africains. Elle permet la mise en relation directe entre porteurs de projets et investisseurs, facilitant le financement participatif avec une interface intuitive et sécurisée.

## ✨ Fonctionnalités Principales

- 🔐 **Authentification complète** - Inscription, connexion, gestion de profils
- 📊 **Gestion de projets** - Création, édition, suivi des projets par catégories
- 💰 **Système d'investissement** - Investissements sécurisés avec suivi en temps réel
- 💬 **Messagerie privée** - Chat temps réel entre porteurs et investisseurs
- 🔔 **Notifications** - Système de notifications push et email
- 📱 **Interface responsive** - Design moderne avec Tailwind CSS
- 🌍 **Contexte africain** - Adapté aux pays et devises africaines (FCFA)

## 🛠️ Technologies Utilisées

- **Backend**: Django 5.0+, Django REST Framework
- **Base de données**: PostgreSQL
- **Frontend**: Tailwind CSS, Alpine.js
- **Temps réel**: Django Channels + WebSocket
- **Authentification**: JWT avec Django Simple JWT
- **Cache**: Redis
- **Task Queue**: Celery

## 🚀 Installation Rapide

```bash
# Cloner le repository
git clone https://github.com/NAELLENANGMO/investafrik.git
cd investafrik

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données PostgreSQL
createdb invest_afbd

# Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# Effectuer les migrations
python manage.py migrate

# Charger les données de test
python manage.py seed_data

# Créer un superutilisateur
python manage.py createsuperuser

# Installer et compiler Tailwind CSS
npm install
npm run build

# Lancer le serveur de développement
python manage.py runserver
```

Accédez à l'application sur [http://localhost:8000](http://localhost:8000)

## 🔑 Comptes de Test

L'application est livrée avec des comptes de test pré-configurés :

### 👑 Administrateur
- **Email**: `admin@investafrik.com`
- **Mot de passe**: `admin123`
- **Accès**: Interface d'administration complète

### 🚀 Porteurs de Projets
- **Email**: `amina.diallo@example.com` | **Mot de passe**: `password123`
- **Email**: `kwame.asante@example.com` | **Mot de passe**: `password123`
- **Email**: `fatou.ba@example.com` | **Mot de passe**: `password123`
- **Email**: `ibrahim.kone@example.com` | **Mot de passe**: `password123`
- **Email**: `aisha.traore@example.com` | **Mot de passe**: `password123`

### 💰 Investisseurs
- **Email**: `jean.dupont@example.com` | **Mot de passe**: `password123`
- **Email**: `marie.martin@example.com` | **Mot de passe**: `password123`
- **Email**: `pierre.bernard@example.com` | **Mot de passe**: `password123`
- **Email**: `sophie.dubois@example.com` | **Mot de passe**: `password123`
- **Email**: `michel.laurent@example.com` | **Mot de passe**: `password123`

### 🎯 Accès Rapide
- **Site web**: http://127.0.0.1:8000
- **Administration**: http://127.0.0.1:8000/admin
- **API**: http://127.0.0.1:8000/api
- **Documentation API**: http://127.0.0.1:8000/api/docs

## 📚 Documentation

- [Guide d'installation détaillé](docs/SETUP_GUIDE.md)
- [Documentation API](docs/API_DOCUMENTATION.md)
- [Guide utilisateur](docs/USER_GUIDE.md)
- [Guide de déploiement](docs/DEPLOYMENT_GUIDE.md)

## 🏗️ Structure du Projet

```
investafrik/
├── apps/                   # Applications Django
│   ├── accounts/          # Gestion des utilisateurs
│   ├── projects/          # Gestion des projets
│   ├── investments/       # Gestion des investissements
│   ├── messaging/         # Système de chat
│   ├── categories/        # Catégories de projets
│   └── notifications/     # Système de notifications
├── templates/             # Templates HTML
├── static/               # Fichiers statiques
├── media/                # Fichiers uploadés
└── docs/                 # Documentation
```