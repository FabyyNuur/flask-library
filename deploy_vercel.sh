#!/bin/bash
# Script de déploiement automatique vers Vercel

echo "🚀 Déploiement vers Vercel..."

# Vérifications préliminaires
if [ ! -f "vercel.json" ]; then
    echo "❌ Erreur: vercel.json non trouvé"
    exit 1
fi

if [ ! -f "api/index.py" ]; then
    echo "❌ Erreur: api/index.py non trouvé"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Erreur: requirements.txt non trouvé"
    exit 1
fi

echo "✅ Fichiers de configuration trouvés"

# Test de l'application localement
echo "🔍 Test de l'application..."
python debug_vercel.py
if [ $? -ne 0 ]; then
    echo "❌ Erreur: L'application ne fonctionne pas localement"
    exit 1
fi

echo "✅ Application testée avec succès"

# Vérifier si vercel CLI est installé
if ! command -v vercel &> /dev/null; then
    echo "📦 Installation de Vercel CLI..."
    npm install -g vercel
fi

echo "🚀 Déploiement vers Vercel..."
vercel --prod

echo "🎉 Déploiement terminé !"
echo ""
echo "📝 N'oubliez pas de :"
echo "   1. Configurer les variables d'environnement sur Vercel"
echo "   2. Vérifier les logs avec: vercel logs --follow"
echo "   3. Tester votre application déployée"
