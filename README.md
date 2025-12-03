# Doctors Dashboard

Application web interactive développée avec **Dash** et **Plotly** pour la visualisation et l'analyse de données médicales.

![Dash](https://img.shields.io/badge/Dash-2.14.2-blue)
![Plotly](https://img.shields.io/badge/Plotly-5.18.0-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Structure du projet](#-structure-du-projet)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Configuration](#-configuration)
- [Développement](#-développement)
- [Technologies](#-technologies)

---

## ✨ Fonctionnalités

- 📊 **Visualisations interactives** avec Plotly
- 🔄 **Chargement dynamique** des données
- 📈 **Graphiques personnalisables** (histogrammes, barres, camemberts, box plots)
- 🎨 **Interface moderne** avec CSS personnalisé
- 📱 **Design responsive** pour mobile et desktop
- 🔧 **Configuration flexible** via arguments CLI
- 📉 **Statistiques descriptives** en temps réel
- 🗂️ **Architecture modulaire** facile à étendre

---

## 📁 Structure du projet

```
Doctors/
├── main.py                      # Point d'entrée de l'application
├── config.py                    # Configuration globale avec typing
├── requirements.txt             # Dépendances Python
├── README.md                    # Documentation principale
│
├── src/                         # Code source principal
│   ├── app/                     # Module d'application
│   │   ├── __init__.py
│   │   ├── app_factory.py       # Factory pattern pour créer l'app Dash
│   │   └── layout.py            # Layout principal
│   │
│   ├── components/              # Composants réutilisables
│   │   ├── __init__.py
│   │   ├── header.py            # Sidebar avec filtres
│   │   ├── navbar.py            # Barre de navigation
│   │   └── footer.py            # Pied de page
│   │
│   ├── pages/                   # Pages de l'application
│   │   ├── __init__.py
│   │   └── home.py              # Page d'accueil avec graphiques
│   │
│   ├── callbacks/               # Callbacks Dash centralisés
│   │   ├── __init__.py
│   │   └── callbacks.py         # Enregistrement de tous les callbacks
│   │
│   └── utils/                   # Utilitaires
│       ├── __init__.py
│       └── data_loader.py       # Chargement et génération de données
│
├── assets/                      # Ressources statiques
│   ├── style.css                # Styles CSS
│   └── .gitkeep
│
├── data/                        # Données
│   ├── raw/                     # Données brutes
│   ├── cleaned/                 # Données nettoyées
│   └── .gitkeep
│
└── images/                      # Images
    └── .gitkeep
```

---

## 🚀 Installation

### Prérequis

- **Python 3.8+** installé sur votre machine
- **pip** (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet** (ou télécharger les fichiers)

```bash
cd /Users/elias/Documents/E3FI/multidisciplinaire/Doctors
```

2. **Créer un environnement virtuel** (recommandé)

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux:
source venv/bin/activate

# Sur Windows:
# venv\Scripts\activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

---

## 💻 Utilisation

### Lancement rapide

Pour lancer l'application avec les paramètres par défaut :

```bash
python main.py
```

L'application sera accessible à l'adresse : **http://127.0.0.1:8050**

### Options de ligne de commande

```bash
# Lancer sur un port spécifique
python main.py --port 8080

# Lancer en mode debug
python main.py --debug

# Lancer sur toutes les interfaces réseau
python main.py --host 0.0.0.0

# Désactiver le rechargement automatique
python main.py --no-reload

# Combiner plusieurs options
python main.py --port 8080 --debug
```

### Arguments disponibles

| Argument | Type | Défaut | Description |
|----------|------|--------|-------------|
| `--port` | int | 8050 | Port du serveur |
| `--host` | str | 127.0.0.1 | Adresse d'écoute |
| `--debug` | flag | False | Active le mode debug |
| `--no-reload` | flag | False | Désactive le rechargement auto |

### Arrêter l'application

Appuyez sur **CTRL+C** dans le terminal pour arrêter le serveur.

---

## ⚙️ Configuration

### Fichier `config.py`

Le fichier `config.py` contient toutes les configurations de l'application :

- **Chemins des fichiers** de données
- **Configuration serveur** (host, port)
- **Paramètres Plotly** (template, palette de couleurs)
- **Messages** de l'application

### Personnalisation des styles

Les styles CSS sont dans `assets/style.css`. Dash charge automatiquement tous les fichiers CSS du dossier `assets/`.

### Ajout de données

Pour utiliser vos propres données :

1. **Placez vos fichiers CSV** dans `data/raw/` ou `data/cleaned/`

2. **Modifiez la fonction `load_sample_data()`** dans `main.py` pour charger vos données :

```python
def load_sample_data():
    """Charge vos données personnalisées."""
    import pandas as pd
    data = pd.read_csv('data/cleaned/votre_fichier.csv')
    return data
```

**Note :** Par défaut, l'application génère des données d'exemple pour la démonstration.

---

## 🛠️ Développement

### Ajouter une nouvelle page

1. Créer un fichier dans `src/pages/` (ex: `new_page.py`)
2. Définir la fonction `create_layout(data)`
3. Définir la fonction `register_callbacks(app, data)`
4. Importer et utiliser dans `main.py`

**Exemple :**

```python
# src/pages/new_page.py
from dash import html

def create_layout(data):
    return html.Div([
        html.H1("Nouvelle Page"),
        # Votre contenu...
    ])

def register_callbacks(app, data):
    # Vos callbacks...
    pass
```

### Ajouter un composant

1. Créer un fichier dans `src/components/` (ex: `card.py`)
2. Définir une fonction qui retourne un composant Dash

**Exemple :**

```python
from dash import html

def create_card(title, content):
    return html.Div([
        html.H3(title, className='card-title'),
        html.P(content)
    ], className='card')
```

### Structure d'un callback

```python
from dash import Input, Output

@app.callback(
    Output('output-id', 'children'),
    Input('input-id', 'value')
)
def update_output(input_value):
    return f"Valeur: {input_value}"
```

---

## 🔧 Technologies

### Frameworks et bibliothèques

- **[Dash](https://dash.plotly.com/)** (2.14.2) - Framework web basé sur Flask
- **[Plotly](https://plotly.com/)** (5.18.0) - Visualisations interactives
- **[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)** (1.5.0) - Composants Bootstrap pour Dash
- **[Pandas](https://pandas.pydata.org/)** (2.1.4) - Manipulation de données
- **[NumPy](https://numpy.org/)** (1.26.2) - Calcul numérique

### Fonctionnalités clés de Dash

- **Callbacks** : Réactivité et interactivité
- **Components** : HTML, Core Components (dcc), Bootstrap
- **Layouts** : Structure hiérarchique des pages
- **Assets** : Chargement automatique CSS/JS

---

## 📝 Notes importantes

### Dossier utils/


## 🤝 Contribution

Pour contribuer au projet :

1. Fork le projet
2. Créer une branche (`git checkout -b nom-branche`)
3. Commit vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

---

## 📧 Contact

Pour toute question ou suggestion :
- **GitHub** : jsp

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---