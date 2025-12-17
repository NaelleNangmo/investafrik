#!/usr/bin/env python3
"""
Script de diagnostic pour comprendre pourquoi les boutons ne s'affichent pas.
"""
import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

def debug_navbar_rendering():
    """Debug complet du rendu de la navbar."""
    print("🔍 DIAGNOSTIC COMPLET DE LA NAVBAR")
    print("=" * 60)
    
    # Test 1: Rendu avec utilisateur anonyme
    print("1. Test avec utilisateur anonyme...")
    try:
        context = {'user': AnonymousUser()}
        navbar_html = render_to_string('components/navbar.html', context)
        
        print(f"   - Longueur HTML: {len(navbar_html)} caractères")
        print(f"   - Contient 'Connexion': {'Connexion' in navbar_html}")
        print(f"   - Contient 'Inscription': {'Inscription' in navbar_html}")
        print(f"   - Contient 'user-menu': {'user-menu' in navbar_html}")
        print(f"   - Contient 'guest-buttons': {'guest-buttons' in navbar_html}")
        
        # Extraire la partie des boutons
        if 'Connexion' in navbar_html:
            start = navbar_html.find('Connexion') - 100
            end = navbar_html.find('Connexion') + 200
            print(f"   - Contexte autour de 'Connexion':")
            print(f"     {navbar_html[start:end]}")
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: Rendu avec utilisateur connecté
    print("\n2. Test avec utilisateur connecté...")
    try:
        user = User.objects.get(email='admin@investafrik.com')
        context = {'user': user}
        navbar_html = render_to_string('components/navbar.html', context)
        
        print(f"   - Utilisateur: {user.email}")
        print(f"   - Type: {user.user_type}")
        print(f"   - Authentifié: {user.is_authenticated}")
        print(f"   - Contient nom utilisateur: {user.email in navbar_html}")
        print(f"   - Contient 'Mes Projets': {'Mes Projets' in navbar_html}")
        print(f"   - Contient 'Déconnexion': {'Déconnexion' in navbar_html}")
        
    except User.DoesNotExist:
        print("   ❌ Utilisateur admin non trouvé")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Test avec client Django
    print("\n3. Test avec client Django...")
    client = Client()
    
    try:
        response = client.get('/')
        print(f"   - Status code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode()
            print(f"   - Contient 'Connexion': {'Connexion' in content}")
            print(f"   - Contient 'Inscription': {'Inscription' in content}")
            print(f"   - Contient debug info: {'DEBUG NAVBAR' in content}")
            
            # Chercher la section debug
            if 'DEBUG NAVBAR' in content:
                start = content.find('DEBUG NAVBAR')
                end = content.find('</div>', start) + 6
                debug_section = content[start:end]
                print(f"   - Section debug trouvée:")
                print(f"     {debug_section}")
        
    except Exception as e:
        print(f"   ❌ Erreur client: {e}")

def check_template_inheritance():
    """Vérifier l'héritage des templates."""
    print("\n🔍 VÉRIFICATION HÉRITAGE TEMPLATES")
    print("=" * 40)
    
    # Vérifier si base.html inclut la navbar
    try:
        from django.template.loader import get_template
        base_template = get_template('base.html')
        base_source = base_template.source
        
        print(f"   - Template base.html trouvé")
        print(f"   - Contient 'navbar': {'navbar' in base_source}")
        print(f"   - Contient 'components/navbar': {'components/navbar' in base_source}")
        
        # Extraire la ligne d'inclusion
        lines = base_source.split('\n')
        for i, line in enumerate(lines):
            if 'navbar' in line.lower():
                print(f"   - Ligne {i+1}: {line.strip()}")
        
    except Exception as e:
        print(f"   ❌ Erreur template: {e}")

def check_css_classes():
    """Vérifier les classes CSS qui pourraient cacher les éléments."""
    print("\n🔍 VÉRIFICATION CLASSES CSS")
    print("=" * 30)
    
    try:
        context = {'user': AnonymousUser()}
        navbar_html = render_to_string('components/navbar.html', context)
        
        # Chercher les classes hidden
        hidden_count = navbar_html.count('hidden')
        print(f"   - Occurrences de 'hidden': {hidden_count}")
        
        # Chercher les classes md:flex
        md_flex_count = navbar_html.count('md:flex')
        print(f"   - Occurrences de 'md:flex': {md_flex_count}")
        
        # Extraire les divs avec classes importantes
        import re
        div_pattern = r'<div[^>]*class="[^"]*(?:hidden|md:flex|auth|guest)[^"]*"[^>]*>'
        matches = re.findall(div_pattern, navbar_html)
        
        print("   - Divs avec classes importantes:")
        for match in matches:
            print(f"     {match}")
        
    except Exception as e:
        print(f"   ❌ Erreur CSS: {e}")

if __name__ == '__main__':
    debug_navbar_rendering()
    check_template_inheritance()
    check_css_classes()
    
    print("\n" + "=" * 60)
    print("🎯 INSTRUCTIONS POUR CORRIGER:")
    print("1. Vérifiez la console du navigateur pour les erreurs JavaScript")
    print("2. Inspectez l'élément dans le navigateur pour voir les classes CSS")
    print("3. Vérifiez que l'utilisateur est bien anonyme (pas de session résiduelle)")
    print("4. Regardez la section DEBUG dans la navbar pour l'état utilisateur")
    print("5. Testez en navigation privée pour éliminer les problèmes de cache")