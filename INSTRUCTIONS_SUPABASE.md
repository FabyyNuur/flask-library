# 📋 Instructions pour Récupérer vos Informations Supabase

## 🔍 Étape 1: Récupérer la Connection String

D'après votre capture d'écran, vous êtes dans **Database Settings**. Maintenant :

### Dans la même page (Database Settings):

1. **Faites défiler vers le bas** jusqu'à trouver la section **"Connection string"**
2. Vous devriez voir quelque chose comme :
   ```
   postgresql://postgres.[project-ref]:[password]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
   ```

### Important à Noter:
- ✅ **SSL est activé** (je vois "Enforce SSL on incoming connections" est ON)
- ✅ **Pool Size: 15** (visible dans votre capture)
- ✅ **Max Client Connections: 200** (visible dans votre capture)

## 🔑 Étape 2: Récupérer les API Keys

1. Allez dans **Settings** → **API** (dans le menu latéral)
2. Copiez :
   - **Project URL** : `https://[votre-project-id].supabase.co`
   - **anon public key** : `eyJhbGci...` (une longue chaîne)

## 📝 Étape 3: Format Final pour vos Variables

Une fois que vous avez récupéré ces informations, vos variables ressembleront à :

```bash
# DATABASE_URL (remplacez [password] par votre mot de passe réel)
DATABASE_URL=postgresql://postgres.[project-ref]:[VOTRE_MOT_DE_PASSE]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres

# SECRET_KEY (basé sur votre config actuelle)
SECRET_KEY=NurulHalbiii-Supabase-Production-2025-SecureBooksStore

# FLASK_ENV
FLASK_ENV=production

# SUPABASE_URL (optionnel)
SUPABASE_URL=https://[votre-project-id].supabase.co

# SUPABASE_ANON_KEY (optionnel)
SUPABASE_ANON_KEY=[votre-anon-key]
```

## 🚨 Points Importants

### SSL Configuration
Votre base a SSL activé, donc votre DATABASE_URL devrait inclure `?sslmode=require` si nécessaire :
```bash
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres?sslmode=require
```

### Connection Pooling
- Votre configuration utilise le **Shared Pooler** (port 6543)
- Pool Size: 15 connexions max
- Parfait pour Vercel !

## 🔄 Prochaines Étapes

1. **Récupérez votre CONNECTION STRING** dans la section en dessous de votre capture
2. **Testez la connexion** : `python test_supabase.py`
3. **Configurez Vercel** : `./setup_vercel_env.sh`

---

**Pouvez-vous faire défiler vers le bas dans la page Database Settings pour trouver la "Connection string" ?** 

C'est généralement juste en dessous de la section "Connection pooling configuration" que je vois dans votre capture.
