#!/bin/bash
# Script pour configurer les variables d'environnement Vercel avec Supabase

echo "🔧 Configuration Vercel avec Supabase..."
echo ""

# Demander les informations Supabase
echo "📝 Informations nécessaires de votre projet Supabase :"
echo "   (Disponibles dans Settings → Database de votre projet)"
echo ""

read -p "🔑 SECRET_KEY (ou appuyez sur Entrée pour utiliser la valeur par défaut): " SECRET_KEY
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY="NurulHalbiii-Supabase-Production-2025-SecureBooksStore"
fi

read -p "🐘 DATABASE_URL (postgresql://...): " DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL obligatoire pour Supabase !"
    exit 1
fi

read -p "🌐 SUPABASE_URL (https://xxx.supabase.co): " SUPABASE_URL
read -p "🗝️  SUPABASE_ANON_KEY: " SUPABASE_ANON_KEY

echo ""
echo "🚀 Configuration des variables sur Vercel..."

# Vérifier si vercel CLI est installé
if ! command -v vercel &> /dev/null; then
    echo "📦 Installation de Vercel CLI..."
    npm install -g vercel
fi

# Configurer les variables
echo "📋 Ajout des variables d'environnement..."

vercel env add SECRET_KEY production <<EOF
$SECRET_KEY
EOF

vercel env add DATABASE_URL production <<EOF
$DATABASE_URL
EOF

vercel env add FLASK_ENV production <<EOF
production
EOF

if [ ! -z "$SUPABASE_URL" ]; then
    vercel env add SUPABASE_URL production <<EOF
$SUPABASE_URL
EOF
fi

if [ ! -z "$SUPABASE_ANON_KEY" ]; then
    vercel env add SUPABASE_ANON_KEY production <<EOF
$SUPABASE_ANON_KEY
EOF
fi

echo ""
echo "✅ Configuration Supabase terminée !"
echo ""
echo "📋 Variables configurées :"
echo "   ✓ SECRET_KEY"
echo "   ✓ DATABASE_URL (Supabase PostgreSQL)"
echo "   ✓ FLASK_ENV: production"
if [ ! -z "$SUPABASE_URL" ]; then
    echo "   ✓ SUPABASE_URL"
fi
if [ ! -z "$SUPABASE_ANON_KEY" ]; then
    echo "   ✓ SUPABASE_ANON_KEY"
fi
echo ""
echo "🎯 Prochaines étapes :"
echo "   1. Exécutez: python migrate_to_supabase.py"
echo "   2. Testez votre app localement"
echo "   3. Déployez: vercel --prod"
