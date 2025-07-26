#!/usr/bin/env python3
"""
Script pour exécuter l'application Flask localement sans Docker
"""
import subprocess
import sys
import os

def check_python():
    """Vérifier que Python est installé"""
    try:
        result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True, check=True)
        print(f"Python trouvé: {result.stdout.strip()}")
        return True
    except (FileNotFoundError, OSError):
        print("Python n'est pas installé ou accessible")
        return False

def install_requirements():
    """Installer les dépendances"""
    try:
        print("Installation des dépendances...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation des dépendances: {e}")
        return False

def run_app():
    """Exécuter l'application Flask"""
    try:
        print("Démarrage de l'application Flask...")
        print("L'application sera accessible sur http://localhost:5000")
        print("Appuyez sur Ctrl+C pour arrêter")
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\nApplication arrêtée")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du démarrage (subprocess): {e}")
    except OSError as e:
        print(f"Erreur système lors du démarrage: {e}")

def main():
    print("=== Démarrage de l'application Flask Bookstore ===")
    
    if not check_python():
        sys.exit(1)
    
    if not os.path.exists('requirements.txt'):
        print("Fichier requirements.txt non trouvé")
        sys.exit(1)
    
    if not os.path.exists('app.py'):
        print("Fichier app.py non trouvé")
        sys.exit(1)
    
    if not install_requirements():
        sys.exit(1)
    
    run_app()

if __name__ == "__main__":
    main()