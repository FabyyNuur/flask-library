#!/bin/bash
# Script automatique pour configurer Vercel avec vos informations Supabase

echo "🔧 Configuration automatique Vercel avec Supabase..."
echo "✅ Informations Supabase détectées"
echo ""

# Variables basées sur vos informations réelles
SECRET_KEY="NurulHalbiii-Supabase-Production-2025-SecureBooksStore"
DATABASE_URL="postgresql://postgres:Allahloveme26%25@db.ljbtpnbtcfqyrshulkyy.supabase.co:5432/postgres"
SUPABASE_URL="https://ljbtpnbtcfqyrshulkyy.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxqYnRwbmJ0Y2ZxeXJzaHVsa3l5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMyMDMwMjIsImV4cCI6MjA2ODc3OTAyMn0.IEmOxaINs1Zr2zp3h7pHHgkVUCsTKHc6I8xn_Ojciaw"

# Vérifier si vercel CLI est installé
if ! command -v vercel &> /dev/null; then
    echo "📦 Installation de Vercel CLI..."
    npm install -g vercel
fi

echo "🚀 Configuration des variables sur Vercel..."

# Configurer les variables une par une
vercel env add SECRET_KEY production <<EOF
$SECRET_KEY
EOF

vercel env add DATABASE_URL production <<EOF
$DATABASE_URL
EOF

vercel env add FLASK_ENV production <<EOF
production
EOF

vercel env add SUPABASE_URL production <<EOF
$SUPABASE_URL
EOF

vercel env add SUPABASE_ANON_KEY production <<EOF
$SUPABASE_ANON_KEY
EOF

echo ""
echo "✅ Configuration Vercel terminée !"
echo ""
echo "📋 Variables configurées :"
echo "   ✓ SECRET_KEY"
echo "   ✓ DATABASE_URL (Supabase PostgreSQL)"
echo "   ✓ FLASK_ENV: production"
echo "   ✓ SUPABASE_URL"
echo "   ✓ SUPABASE_ANON_KEY"
echo ""
echo "🎯 Votre application est maintenant prête pour le déploiement !"
echo ""
echo "🚀 Pour déployer :"
echo "   vercel --prod"
