# 📚 Documentation API - InvestAfrik

Cette documentation décrit tous les endpoints API disponibles dans la plateforme InvestAfrik.

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification. Incluez le token dans l'en-tête Authorization :

```
Authorization: Bearer <votre_token_jwt>
```

## 📋 Endpoints Disponibles

### Authentication (`/api/auth/`)

#### POST `/api/auth/register/`
Inscription d'un nouvel utilisateur.

**Paramètres :**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "motdepasse123",
  "password_confirm": "motdepasse123",
  "first_name": "Prénom",
  "last_name": "Nom",
  "phone_number": "+237123456789",
  "user_type": "porteur", // ou "investisseur"
  "country": "CM",
  "bio": "Description optionnelle"
}
```

**Réponse :**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "Prénom",
    "last_name": "Nom",
    "user_type": "porteur"
  },
  "tokens": {
    "refresh": "refresh_token",
    "access": "access_token"
  }
}
```

#### POST `/api/auth/login/`
Connexion utilisateur.

**Paramètres :**
```json
{
  "email": "user@example.com",
  "password": "motdepasse123"
}
```

#### POST `/api/auth/logout/`
Déconnexion (blacklist du refresh token).

**Paramètres :**
```json
{
  "refresh": "refresh_token"
}
```

#### GET `/api/auth/me/`
Récupérer le profil de l'utilisateur connecté.

**Réponse :**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "Prénom",
  "last_name": "Nom",
  "user_type": "porteur",
  "country": "CM",
  "profile_picture": "url_image",
  "bio": "Description",
  "profile": {
    "company": "Entreprise",
    "job_title": "Poste"
  }
}
```

### Projets (`/api/projects/`)

#### GET `/api/projects/`
Liste tous les projets avec pagination et filtres.

**Paramètres de requête :**
- `category` : Filtrer par catégorie
- `status` : Filtrer par statut (active, successful, failed)
- `country` : Filtrer par pays
- `search` : Recherche textuelle
- `ordering` : Tri (-created_at, goal_amount, end_date)
- `page` : Numéro de page

**Réponse :**
```json
{
  "count": 50,
  "next": "url_page_suivante",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "title": "Titre du projet",
      "slug": "titre-du-projet",
      "short_description": "Description courte",
      "owner": {
        "id": "uuid",
        "first_name": "Prénom",
        "last_name": "Nom"
      },
      "category": {
        "id": 1,
        "name": "Agriculture & Agrobusiness",
        "slug": "agriculture-agrobusiness"
      },
      "goal_amount": "5000000.00",
      "current_amount": "1250000.00",
      "funding_percentage": 25.0,
      "days_remaining": 45,
      "investor_count": 12,
      "featured_image": "url_image",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### POST `/api/projects/`
Créer un nouveau projet (porteurs uniquement).

**Paramètres :**
```json
{
  "title": "Titre du projet",
  "short_description": "Description courte",
  "full_description": "<p>Description complète HTML</p>",
  "category": 1,
  "goal_amount": "5000000.00",
  "country": "CM",
  "start_date": "2024-01-15",
  "end_date": "2024-04-15",
  "budget_breakdown": {
    "equipement": 3000000,
    "marketing": 1000000,
    "operations": 1000000
  }
}
```

#### GET `/api/projects/{id}/`
Détails d'un projet spécifique.

#### PUT/PATCH `/api/projects/{id}/`
Modifier un projet (propriétaire uniquement).

#### POST `/api/projects/{id}/invest/`
Investir dans un projet.

#### POST `/api/projects/{id}/save/`
Sauvegarder un projet en favoris.

#### DELETE `/api/projects/{id}/save/`
Retirer un projet des favoris.

### Catégories (`/api/categories/`)

#### GET `/api/categories/`
Liste toutes les catégories.

**Réponse :**
```json
[
  {
    "id": 1,
    "name": "Agriculture & Agrobusiness",
    "slug": "agriculture-agrobusiness",
    "description": "Projets agricoles, élevage, transformation agricole",
    "icon_class": "fas fa-seedling",
    "color_hex": "#4CAF50",
    "project_count": 25,
    "total_funded_amount": "150000000.00"
  }
]
```

#### GET `/api/categories/{slug}/projects/`
Projets d'une catégorie spécifique.

### Investissements (`/api/investments/`)

#### GET `/api/investments/my-investments/`
Liste des investissements de l'utilisateur connecté.

#### POST `/api/investments/`
Créer un nouvel investissement.

**Paramètres :**
```json
{
  "project": "project_uuid",
  "amount": "100000.00",
  "message": "Message optionnel pour le porteur",
  "payment_method": "mobile_money"
}
```

### Messagerie (`/api/messaging/`)

#### GET `/api/messaging/conversations/`
Liste des conversations de l'utilisateur.

#### POST `/api/messaging/conversations/`
Créer une nouvelle conversation.

#### GET `/api/messaging/conversations/{id}/messages/`
Messages d'une conversation.

#### POST `/api/messaging/conversations/{id}/send_message/`
Envoyer un message.

**Paramètres :**
```json
{
  "content": "Contenu du message"
}
```

### Notifications (`/api/notifications/`)

#### GET `/api/notifications/`
Liste des notifications de l'utilisateur.

#### POST `/api/notifications/{id}/mark_read/`
Marquer une notification comme lue.

#### POST `/api/notifications/mark-all-read/`
Marquer toutes les notifications comme lues.

## 🔧 Codes d'Erreur

- `400 Bad Request` : Données invalides
- `401 Unauthorized` : Token manquant ou invalide
- `403 Forbidden` : Permissions insuffisantes
- `404 Not Found` : Ressource introuvable
- `500 Internal Server Error` : Erreur serveur

## 📝 Exemples d'Utilisation

### JavaScript (Fetch API)

```javascript
// Connexion
const response = await fetch('/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const data = await response.json();
localStorage.setItem('access_token', data.tokens.access);

// Récupérer les projets
const projectsResponse = await fetch('/api/projects/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});

const projects = await projectsResponse.json();
```

### Python (Requests)

```python
import requests

# Connexion
login_data = {
    'email': 'user@example.com',
    'password': 'password123'
}

response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
tokens = response.json()['tokens']

# Récupérer les projets
headers = {'Authorization': f'Bearer {tokens["access"]}'}
projects_response = requests.get('http://localhost:8000/api/projects/', headers=headers)
projects = projects_response.json()
```

### cURL

```bash
# Connexion
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Récupérer les projets
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🚀 WebSocket (Temps Réel)

### Chat en Temps Réel

```javascript
const conversationId = 'uuid-conversation';
const socket = new WebSocket(`ws://localhost:8000/ws/chat/${conversationId}/`);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'chat_message') {
        // Afficher le nouveau message
        displayMessage(data.message);
    }
};

// Envoyer un message
socket.send(JSON.stringify({
    'type': 'chat_message',
    'message': 'Bonjour!'
}));
```

### Notifications en Temps Réel

```javascript
const notificationSocket = new WebSocket('ws://localhost:8000/ws/notifications/');

notificationSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'notification') {
        // Afficher la notification
        showNotification(data.notification);
    }
};
```