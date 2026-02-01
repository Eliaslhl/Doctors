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
- [Graphiques et Visualisations](#-graphiques-et-visualisations)
- [Configuration](#-configuration)
- [Développement](#-développement)
- [Technologies](#-technologies)

## 📚 Documentation complémentaire

- **[GUIDE_UTILISATEUR.md](GUIDE_UTILISATEUR.md)** - Guide complet d'utilisation pas-à-pas
- **[CHANGELOG.md](CHANGELOG.md)** - Historique des versions et améliorations
- **[RESUME_AMELIORATIONS.md](RESUME_AMELIORATIONS.md)** - Synthèse détaillée des améliorations v2.0
- **[DEMO_VISUELLE.md](DEMO_VISUELLE.md)** - Démonstration visuelle des changements

---

## ✨ Fonctionnalités

### Interface utilisateur

- 🔍 **Système de filtres optimisé** avec bouton de validation pour éviter les rafraîchissements automatiques
- 📊 **Visualisations interactives avancées** avec Plotly
- 🎯 **Tooltips enrichis** affichant statistiques détaillées (moyenne, écart-type, quartiles)
- 🎨 **Interface moderne** avec CSS personnalisé et animations fluides
- 📱 **Design responsive** pour mobile et desktop

### Visualisations et analyses

- 🗺️ **Carte choroplèthe mondiale** avec gradient de couleur intelligent (rouge-jaune-vert)
- 📈 **Graphiques de tendance temporelle** avec intervalles de confiance
- 📊 **Top pays par couverture** avec visualisation en barres colorées
- 📉 **Histogrammes** avec lignes de moyenne et médiane
- 📦 **Box plots** affichant quartiles, outliers et écart-type
- 🥧 **Diagrammes circulaires** et treemaps pour la composition des données

### Fonctionnalités techniques

- 🔄 **Chargement dynamique** des données avec filtrage intelligent
- 🔧 **Configuration flexible** via arguments CLI
- 📉 **Statistiques descriptives** en temps réel
- 🗂️ **Architecture modulaire** facile à étendre
- 💾 **Gestion d'état** avec Dash Store pour optimiser les performances

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
│   │   └── layout.py            # Layout principal
│   │
│   ├── components/              # Composants réutilisables
│   │   ├── __init__.py
│   │   ├── header.py            # Sidebar avec filtres et bouton de validation
│   │   └── footer.py            # Pied de page
│   │
│   ├── pages/                   # Pages de l'application
│   │   ├── __init__.py
│   │   └── home.py              # Page d'accueil avec graphiques et callbacks
│   │
│   ├── callbacks/               # Callbacks Dash centralisés
│   │   ├── __init__.py
│   │   └── callbacks.py         # Enregistrement de tous les callbacks
│   │
│   ├── graphics/                # Modules de visualisation
│   │   ├── __init__.py
│   │   ├── map.py               # Carte choroplèthe mondiale
│   │   ├── country_details.py  # Graphique des top pays
│   │   ├── timed_count.py      # Évolution temporelle
│   │   ├── statistics.py       # Histogrammes et box plots
│   │   ├── pie_chart.py        # Diagrammes circulaires
│   │   └── tree_map.py         # TreeMaps hiérarchiques
│   │
│   └── utils/                   # Utilitaires
│       ├── __init__.py
│       ├── get_data.py          # Filtrage et accès aux données
│       └── clean_data.py        # Nettoyage des données brutes
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

4. **Nettoyer les données**

```bash
PYTHONPATH=. venv/bin/python src/utils/clean_data.py
```

---

## 💻 Utilisation

### Lancement rapide

Pour lancer l'application avec les paramètres par défaut :

```bash
python main.py
# ou
venv/bin/python main.py
```

L'application sera accessible à l'adresse : **http://127.0.0.1:8050**

### Utilisation de l'interface

#### 🔍 Filtres et Navigation

1. **Sélection des filtres** : Utilisez les dropdowns dans la barre latérale gauche pour :
   - Choisir la vue (Tous / Pays / Régions WHO)
   - Sélectionner une année spécifique ou toutes les années
   - Filtrer par pays/région
   - Choisir un antigène particulier
   - Sélectionner un type de données

2. **Validation des filtres** : Après avoir configuré vos filtres, cliquez sur le bouton **🔍 Appliquer les filtres** pour mettre à jour tous les graphiques. Cela évite les rechargements multiples pendant la configuration.

3. **Statistiques globales** : Les cartes en haut affichent des statistiques filtrées uniquement par année (nombre de pays, années, couverture moyenne).

#### 📊 Types de graphiques disponibles

- **Carte mondiale** : Visualisation géographique de la couverture vaccinale par pays
- **Top pays** : Classement des pays selon leur couverture moyenne
- **Évolution temporelle** : Tendances de couverture au fil des années
- **Distribution** : Histogramme ou boxplot pour analyser la répartition des valeurs
- **Composition** : Diagramme circulaire ou treemap pour visualiser les proportions

#### 💡 Astuces d'utilisation

- **Survolez les graphiques** pour voir des informations détaillées (tooltips)
- **Utilisez le zoom** sur les graphiques pour explorer en détail
- **Téléchargez les graphiques** via le menu qui apparaît en survolant (icône appareil photo)
- **Changez le type de graphique** dans les sections d'exploration pour différentes perspectives

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

| Argument      | Type | Défaut    | Description                    |
| ------------- | ---- | --------- | ------------------------------ |
| `--port`      | int  | 8050      | Port du serveur                |
| `--host`      | str  | 127.0.0.1 | Adresse d'écoute               |
| `--debug`     | flag | False     | Active le mode debug           |
| `--no-reload` | flag | False     | Désactive le rechargement auto |

### Arrêter l'application

Appuyez sur **CTRL+C** dans le terminal pour arrêter le serveur.

---

## 📊 Graphiques et Visualisations

### Vue d'ensemble des graphiques

L'application propose plusieurs types de visualisations optimisées pour différents types d'analyses :

#### 🗺️ Carte choroplèthe mondiale

- **Objectif** : Visualisation géographique de la couverture vaccinale
- **Caractéristiques** :
  - Gradient de couleur rouge (faible) → jaune (moyen) → vert (élevé)
  - Tooltips affichant : pays, couverture moyenne, nombre d'enregistrements
  - Projection Natural Earth pour une meilleure lisibilité
  - Zoom et navigation interactifs

#### 📊 Top pays par couverture

- **Objectif** : Comparer les performances des pays
- **Caractéristiques** :
  - Barres horizontales avec gradient de couleur
  - Affichage des valeurs directement sur les barres
  - Tooltips avec : couverture moyenne, écart-type, nombre d'enregistrements
  - Hauteur dynamique selon le nombre de pays

#### 📈 Évolution temporelle

- **Objectif** : Analyser les tendances dans le temps
- **Caractéristiques** :
  - Ligne avec marqueurs pour chaque année
  - Tooltips détaillés : année, moyenne, écart-type, nombre d'enregistrements
  - Mode "hover unifié" pour comparer plusieurs années facilement

#### 📉 Histogramme de distribution

- **Objectif** : Analyser la répartition des valeurs de couverture
- **Caractéristiques** :
  - Lignes verticales pour la moyenne (rouge) et médiane (verte)
  - Écart-type affiché dans le titre
  - Nombre de bins configurable
  - Tooltips montrant les intervalles et fréquences

#### 📦 Box plot (Boîte à moustaches)

- **Objectif** : Visualiser les quartiles et détecter les outliers
- **Caractéristiques** :
  - Affichage de la moyenne et écart-type
  - Identification visuelle des valeurs extrêmes
  - Comparaison par catégorie (si filtre appliqué)
  - Tooltips avec min, Q1, médiane, Q3, max

#### 🥧 Diagramme circulaire et TreeMap

- **Objectif** : Visualiser les proportions et hiérarchies
- **Caractéristiques** :
  - Pie chart pour les proportions simples
  - TreeMap pour les hiérarchies multi-niveaux
  - Couleurs cohérentes et contrastées

### Conseils d'interprétation

- **Carte** : Identifiez rapidement les zones géographiques à faible/haute couverture
- **Top pays** : Comparez les performances relatives entre pays
- **Évolution** : Détectez les tendances à la hausse ou à la baisse
- **Histogramme** : Évaluez si la distribution est normale, bimodale, etc.
- **Box plot** : Identifiez les valeurs aberrantes et la dispersion des données

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

### Architecture de l'application

L'application suit une architecture modulaire basée sur les principes de séparation des responsabilités :

#### Flux de données et callbacks

1. **Sélection des filtres** → Dropdowns dans la sidebar ([src/components/header.py](src/components/header.py))
2. **Validation** → Clic sur le bouton "Appliquer les filtres"
3. **Stockage** → Les valeurs sont stockées dans un `dcc.Store` (composant Dash)
4. **Déclenchement** → Tous les callbacks écoutent le Store plutôt que les dropdowns
5. **Rendu** → Les graphiques sont mis à jour en une seule fois

Cette approche optimise les performances en évitant les recalculs multiples lors de la configuration des filtres.

### Ajouter un nouveau graphique

1. **Créer la fonction de visualisation** dans `src/graphics/`

```python
# src/graphics/mon_graphique.py
import plotly.graph_objects as go
from config import PLOTLY_TEMPLATE

def create_mon_graphique(data, **kwargs):
    """Crée mon graphique personnalisé."""
    fig = go.Figure()
    # ... votre logique
    fig.update_layout(template=PLOTLY_TEMPLATE)
    return fig
```

2. **Ajouter le graphique au layout** dans [src/pages/home.py](src/pages/home.py)

```python
dcc.Graph(
    id="mon-graphique",
    config=PLOTLY_CONFIG,
)
```

3. **Créer le callback** pour le rendre dynamique

```python
@app.callback(
    Output("mon-graphique", "figure"),
    [Input("validated-filters", "data")],
)
def update_mon_graphique(validated_filters):
    # Récupérer les filtres
    group_filter = validated_filters.get("group", "all")
    # ... autres filtres

    # Filtrer les données
    filtered_data = get_filtered_data(data, ...)

    # Créer le graphique
    return create_mon_graphique(filtered_data)
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

### Système de filtrage optimisé

L'application utilise un système de filtrage avec validation manuelle pour améliorer l'expérience utilisateur :

- **Avant** : Chaque changement de filtre déclenchait un recalcul de tous les graphiques
- **Maintenant** : Les filtres sont stockés temporairement et appliqués uniquement lors du clic sur le bouton
- **Avantage** : Permet de configurer plusieurs filtres sans ralentissements

### Performance et optimisation

- Les graphiques utilisent des **tooltips personnalisés** pour afficher plus d'informations sans surcharger la vue
- Les **couleurs sont cohérentes** à travers toute l'application (défini dans `config.py`)
- Les **statistiques descriptives** (moyenne, écart-type, quartiles) sont calculées à la volée
- Le **template Plotly** est centralisé pour un style uniforme

### Personnalisation des graphiques

Tous les graphiques dans `src/graphics/` acceptent des paramètres optionnels :

- `title` : Pour personnaliser le titre
- `color_scale` : Pour modifier les couleurs (cartes)
- `top_n` : Pour limiter le nombre d'éléments affichés
- Voir la documentation de chaque fonction pour plus de détails

### Dossier utils/

Le dossier [src/utils/](src/utils/) contient :

- `get_data.py` : Fonctions de filtrage et accès aux données
- `clean_data.py` : Script de nettoyage des données brutes

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
