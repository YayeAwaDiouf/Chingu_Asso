# Gestion Associative — Mini PGI (Flask + SQLite)

Application web simple pour gérer une association : membres, événements, participations et cotisations.

## Fonctionnalités
- Tableau de bord (membres, événements, participations, cotisations payées / impayées)
- CRUD Membres
- CRUD Événements
- CRUD Cotisations (par membre)
- Gestion des participations (lier un membre à un événement)
- Base de données SQLite auto-créée au premier lancement
- Données d'exemple (seed) facultatives

## Démarrage rapide
```bash
# 1) Créer et activer un environnement virtuel (optionnel mais recommandé)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Installer les dépendances
pip install -r requirements.txt
----------------------------------------------------------------------------------------------------Comment accéder à l’application

Se placer dans le disque D :
Dans le terminal, taper :

D:


Aller dans le dossier du projet :
Utiliser la commande cd pour accéder au fichier source, par exemple :

cd D:\Documents\L3\cours\Introduction aux systemes d'information\gestion_associative_app


Activer l’environnement virtuel :
Dans le dossier du projet, taper :

.\.venv\Scripts\activate


Tester si Flask fonctionne :
Lancer l’application avec l’une des commandes suivantes :

flask run


ou

python app.py


Accéder à l’application dans le navigateur :
Ouvrir l’adresse suivante dans un navigateur :

http://127.0.0.1:5000
# 3) Démarrer l'appli
export FLASK_APP=app.py   # Windows PowerShell: $Env:FLASK_APP="app.py"
flask run
# L'application est accessible sur http://127.0.0.1:5000
```

## Structure
```
gestion_associative_app/
├─ app.py
├─ models.py
├─ requirements.txt
├─ README.md
├─ templates/
│  ├─ base.html
│  ├─ dashboard.html
│  ├─ members_list.html
│  ├─ members_form.html
│  ├─ events_list.html
│  ├─ events_form.html
│  ├─ dues_list.html
│  ├─ dues_form.html
│  ├─ participations.html
└─ static/
   └─ style.css
```

