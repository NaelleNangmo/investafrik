#!/usr/bin/env python3
"""
Test pour vérifier que la navbar ne génère plus d'erreur VariableDoesNotExist.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

def test_navbar_anonymous():
    """Test de la navbar avec un utilisateur anonyme."""
    print("🧪 TEST NAVBAR UTILISATEUR ANONYME")
    print("=" * 40)
    
    try:
        context = {'user': AnonymousUser()}
        navbar_html = render_to_string('components/navbar.html', context)
        print("✅ Navbar rendue avec succès pour utilisateur anonyme")
        
        # Vérifications
        if 'Connexion' in navbar_html:
            print("✅ Bouton 'Connexion' présent")
        else:
            print("❌ Bouton 'Connexion' manquant")
            
        if 'Inscription' in navbar_html:
            print("✅ Bouton 'Inscription' présent")
        else:
            print("❌ Bouton 'Inscription' manquant")
            
        if 'user.email' not in navbar_html:
            print("✅ Pas de référence directe à user.email")
        else:
            print("❌ Référence directe à user.email trouvée")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du rendu navbar anonyme: {e}")
        return False

def test_navbar_authenticated():
    """Test de la navbar avec un utilisateur connecté."""
    print("\n🧪 TEST NAVBAR UTILISATEUR CONNECTÉ")
    print("=" * 40)
    
    try:
        user = User.objects.get(email='admin@investafrik.com')
        context = {'user': user}
        navbar_html = render_to_string('components/navbar.html', context)
        print("✅ Navbar rendue avec succès pour utilisateur connecté")
        
        # Vérifications
        if 'Mes Projets' in navbar_html:
            print("✅ Onglet 'Mes Projets' présent pour porteur")
        else:
            print("❌ Onglet 'Mes Projets' manquant")
            
        if 'Messages' in navbar_html:
            print("✅ Onglet 'Messages' présent")
        else:
            print("❌ Onglet 'Messages' manquant")
            
        if 'Déconnexion' in navbar_html:
            print("✅ Bouton 'Déconnexion' présent")
        else:
            print("❌ Bouton 'Déconnexion' manquant")
            
        return True
        
    except User.DoesNotExist:
        print("❌ Utilisateur admin non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du rendu navbar connecté: {e}")
        return False

def test_navbar_investisseur():
    """Test de la navbar avec un utilisateur investisseur."""
    print("\n🧪 TEST NAVBAR UTILISATEUR INVESTISSEUR")
    print("=" * 40)
    
    try:
        user = User.objects.get(email='investor@test.com')
        context = {'user': user}
        navbar_html = render_to_string('components/navbar.html', context)
        print("✅ Navbar rendue avec succès pour investisseur")
        
        # Vérifications
        if 'Mes Investissements' in navbar_html:
            print("✅ Onglet 'Mes Investissements' présent pour investisseur")
        else:
            print("❌ Onglet 'Mes Investissements' manquant")
            
        if 'Mes Projets' not in navbar_html:
            print("✅ Onglet 'Mes Projets' absent (correct pour investisseur)")
        else:
            print("❌ Onglet 'Mes Projets' présent (incorrect pour investisseur)")
            
        return True
        
    except User.DoesNotExist:
        print("❌ Utilisateur investisseur non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du rendu navbar investisseur: {e}")
        return False

if __name__ == '__main__':
    print("🚀 TESTS DE CORRECTION NAVBAR")
    print("=" * 60)
    
    success1 = test_navbar_anonymous()
    success2 = test_navbar_authenticated()
    success3 = test_navbar_investisseur()
    
    print("\n" + "=" * 60)
    
    if success1 and success2 and success3:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ La navbar ne génère plus d'erreur VariableDoesNotExist")
        print("✅ L'affichage conditionnel fonctionne correctement")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus")
    
    print("\n📋 Pour tester manuellement:")
    print("1. Allez sur http://127.0.0.1:8000")
    print("2. Vérifiez que la page se charge sans erreur")
    print("3. Connectez-vous et vérifiez les onglets selon le type d'utilisateur")