# 📖 Guide d'Installation - InvestAfrik

Ce guide vous accompagne étape par étape pour installer et configurer InvestAfrik sur votre machine de développement.

## 🔧 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.11+** - [Télécharger Python](https://www.python.org/downloads/)
- **PostgreSQL 15+** - [Télécharger PostgreSQL](https://www.postgresql.org/download/)
- **Node.js 18+** - [Télécharger Node.js](https://nodejs.org/)
- **Git** - [Télécharger Git](https://git-scm.com/)

## 📥 Étape 1 : Cloner le Repository

```bash
git clone https://github.com/votre-username/investafrik.git
cd investafrik
```

## 🐍 Étape 2 : Environnement Python

### Créer l'environnement virtuel
```bash
python -m venv venv
```

### Activer l'environnement virtuel
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Installer les dépendances Python
```bash
pip install -r requirements.txt
```

## 🗄️ Étape 3 : Configuration PostgreSQL

### Créer la base de données
```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base de données
CREATE DATABASE invest_afbd;

# Créer un utilisateur (optionnel)
CREATE USER investafrik WITH PASSWORD 'noutong1';
GRANT ALL PRIVILEGES ON DATABASE invest_afbd TO investafrik;

# Quitter psql
\q
```

## ⚙️ Étape 4 : Variables d'Environnement

### Copier le fichier d'exemple
```bash
cp .env.example .env
```

### Éditer le fichier .env
```bash
# Ouvrir avec votre éditeur préféré
nano .env
# ou
code .env
```

### Configuration minimale requise
```env
SECRET_KEY=votre-clé-secrète-très-longue-et-complexe
DEBUG=True
DB_NAME=invest_afbd
DB_USER=postgres
DB_PASSWORD=noutong1
DB_HOST=localhost
DB_PORT=5432
```

## 🎨 Étape 5 : Tailwind CSS

### Installer les dépendances Node.js
```bash
npm install
```

### Compiler Tailwind CSS
```bash
# Pour le développement (avec watch)
npm run build

# Pour la production (minifié)
npm run build-prod
```

## 🔄 Étape 6 : Migrations Django

### Créer et appliquer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📊 Étape 7 : Données de Test

### Charger les données de test
```bash
python manage.py seed_data
```

### Créer un superutilisateur
```bash
python manage.py createsuperuser
```

## 🚀 Étape 8 : Lancement

### Démarrer le serveur de développement
```bash
python manage.py runserver
```

### Accéder à l'application
- **Frontend** : [http://localhost:8000](http://localhost:8000)
- **Admin** : [http://localhost:8000/admin](http://localhost:8000/admin)
- **API** : [http://localhost:8000/api](http://localhost:8000/api)

## ✅ Vérification de l'Installation

1. Accédez à la page d'accueil
2. Créez un compte utilisateur
3. Connectez-vous à l'admin Django
4. Vérifiez que les catégories sont chargées
5. Testez la création d'un projet

## 🔧 Dépannage

### Erreur de base de données
```bash
# Vérifier que PostgreSQL est démarré
sudo service postgresql start  # Linux
brew services start postgresql  # Mac

# Vérifier la connexion
psql -U postgres -d invest_afbd
```

### Erreur Tailwind CSS
```bash
# Réinstaller les dépendances
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Erreur de migrations
```bash
# Reset des migrations (ATTENTION : perte de données)
python manage.py migrate --fake-initial
python manage.py migrate
```

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs Django
2. Consultez la documentation
3. Ouvrez une issue sur GitHub