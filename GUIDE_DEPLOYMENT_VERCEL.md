# Guide de Déploiement Vercel - Application Flask Bookstore

## 🚀 Étapes de Déploiement

### 1. Prérequis
- Compte Vercel (https://vercel.com)
- Repository GitHub avec votre code

### 2. Configuration des Variables d'Environnement sur Vercel

Dans le dashboard Vercel, allez dans les settings de votre projet et ajoutez :

```bash
SECRET_KEY=votre-cle-secrete-super-longue-et-complexe
DATABASE_URL=sqlite:///:memory:
FLASK_ENV=production
```

### 3. Structure des Fichiers Critique pour Vercel

✅ **Fichiers présents et configurés :**
- `vercel.json` - Configuration Vercel
- `requirements.txt` - Dépendances Python  
- `api/index.py` - Point d'entrée pour Vercel
- `config_vercel.py` - Configuration de production

### 4. Fichiers Importants

#### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production",
    "SECRET_KEY": "@secret_key",
    "DATABASE_URL": "@database_url"
  },
  "functions": {
    "api/index.py": {
      "maxDuration": 10
    }
  }
}
```

#### api/index.py
Point d'entrée qui :
- Charge votre application Flask
- Configure la base de données en mémoire
- Gère les erreurs de manière gracieuse
- Crée un utilisateur admin par défaut

### 5. Commandes de Déploiement

#### Option A : Via CLI Vercel
```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter
vercel login

# Déployer
vercel --prod
```

#### Option B : Via GitHub (Recommandé)
1. Connectez votre repo GitHub à Vercel
2. Chaque push sur `main` déclenchera un déploiement automatique

### 6. Base de Données

⚠️ **Important :** Vercel utilise des fonctions serverless qui ne persistent pas les données.

**Solutions recommandées :**

#### Option A : Base de données externe (Recommandée)
```bash
# Ajouter une variable d'environnement DATABASE_URL pointant vers :
# - PostgreSQL (Neon, Supabase, Railway)
# - MySQL (PlanetScale, Railway)
# Exemple :
DATABASE_URL=postgresql://user:password@host:port/dbname
```

#### Option B : Base de données en mémoire (Actuelle)
- Données perdues à chaque redémarrage
- Appropriée pour les démonstrations uniquement

### 7. Utilisateur Admin par Défaut

L'application crée automatiquement :
- **Username :** `admin`
- **Password :** `admin123`
- **Rôle :** `ADMIN`

⚠️ **Changez ce mot de passe en production !**

### 8. Vérifications Post-Déploiement

1. **Test de la page d'accueil :**
   ```
   https://votre-app.vercel.app/
   ```
   Devrait rediriger vers `/login`

2. **Test de connexion :**
   ```
   https://votre-app.vercel.app/login
   ```
   Utilisez admin/admin123

3. **Test de l'admin :**
   ```
   https://votre-app.vercel.app/admin/bookstore
   ```

### 9. Logs de Débogage

Pour voir les logs d'erreur :
```bash
vercel logs --follow
```

### 10. Résolution de Problèmes Courants

#### Erreur 500 : FUNCTION_INVOCATION_FAILED
- Vérifiez les logs : `vercel logs`
- Vérifiez les variables d'environnement
- Vérifiez que tous les imports fonctionnent

#### Base de données non trouvée
- Utilisez une base externe ou acceptez la perte de données
- Vérifiez la variable `DATABASE_URL`

#### Timeout des fonctions
- Les fonctions Vercel ont un timeout (10s configuré)
- Optimisez les requêtes lentes

### 11. Commandes Utiles

```bash
# Tester localement
python debug_vercel.py

# Voir les logs en temps réel
vercel logs --follow

# Redéployer
vercel --prod

# Variables d'environnement
vercel env list
vercel env add SECRET_KEY
```

## 🎯 Prochaines Étapes

1. **Base de données persistante** : Migrez vers PostgreSQL/MySQL
2. **Sécurité** : Changez les mots de passe par défaut
3. **Monitoring** : Configurez les alertes Vercel
4. **Cache** : Implémentez du cache pour les performances

---

**🔗 Liens Utiles :**
- [Documentation Vercel Python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Flask sur Vercel](https://vercel.com/guides/using-flask-with-vercel)
- [Variables d'environnement Vercel](https://vercel.com/docs/projects/environment-variables)
