#!/bin/bash
# Script de déploiement pour Vercel

echo "🚀 Préparation du déploiement Vercel..."

# Ajouter tous les fichiers
git add .

# Créer un commit
echo "📝 Création du commit..."
git commit -m "Configuration pour déploiement Vercel - $(date '+%Y-%m-%d %H:%M:%S')"

# Pousser vers la branche main
echo "📤 Poussée vers GitHub..."
git push origin main

echo "✅ Déploiement préparé ! Maintenant :"
echo "1. Allez sur vercel.com"
echo "2. Connectez votre repository GitHub"
echo "3. Déployez !"
echo ""
echo "🔗 Votre repository : https://github.com/FabyyNuur/flaskProject"
