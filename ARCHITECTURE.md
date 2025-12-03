# Architecture de l'application

## 📁 Structure des dossiers

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
│   ├── graphics/                # 📊 Graphiques modulaires (v2.0)
│   │   ├── __init__.py
│   │   ├── README.md                    # Documentation complète
│   │   ├── MIGRATION.md                 # Guide de migration v1 → v2
│   │   ├── country_details.py           # Détails et analyses par pays
│   │   ├── vaccination_table.py         # Tableaux interactifs Plotly
│   │   ├── map.py                       # Cartes géographiques (TODO)
│   │   ├── pie_chart.py                 # Graphiques en camembert
│   │   ├── statistics.py                # Stats, histogrammes, boxplots
│   │   ├── timed_count.py               # Évolutions temporelles
│   │   └── tree_map.py                  # TreeMap, Sunburst, hiérarchies
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
│   │   └── rawdata.csv          # Données de vaccination (WHO format)
│   ├── cleaned/                 # Données nettoyées
│   └── .gitkeep
│
└── images/                      # Images
    └── .gitkeep
```

## 🏗️ Principes d'architecture

### 1. **Séparation des responsabilités**
- `main.py` : Point d'entrée uniquement, lance l'application
- `src/app/` : Création et configuration de l'application
- `src/components/` : Composants UI réutilisables
- `src/pages/` : Pages avec leur layout et logique
- `src/graphics/` : **Graphiques modulaires isolés et réutilisables**
- `src/callbacks/` : Logique interactive (callbacks Dash)
- `src/utils/` : Fonctions utilitaires et chargement de données

### 2. **Type hints et documentation**
Tous les modules utilisent :
- **Type hints** pour une meilleure maintenabilité
- **Docstrings** au format Google/NumPy
- **Annotations** pour les arguments et retours

### 3. **Pattern Factory**
- `app_factory.py` utilise le pattern Factory pour créer l'application
- Configuration séparée de la logique métier
- Facilite les tests et la réutilisation

### 4. **Configuration centralisée**
- `config.py` : Toutes les constantes et configurations
- Type hints pour les configurations
- Séparation par sections (serveur, graphiques, chemins, etc.)

## 🔧 Qualité du code

### Type hints
```python
def create_sidebar(data: pd.DataFrame) -> html.Div:
    """Crée une sidebar avec filtres."""
    ...
```

### Docstrings
```python
def generate_sample_vaccination_data(seed: int = 42) -> pd.DataFrame:
    """
    Génère des données de vaccination simulées.
    
    Args:
        seed: Graine pour la génération aléatoire
        
    Returns:
        DataFrame contenant les données de vaccination
    """
    ...
```

### Organisation modulaire
- Chaque module a une responsabilité unique
- Imports explicites
- Code DRY (Don't Repeat Yourself)

## 🚀 Utilisation

### Lancer l'application
```bash
python main.py
```

### Options CLI
```bash
# Par défaut (port 8050)
python main.py

# Port personnalisé
python main.py --port 8080

# Hôte personnalisé
python main.py --host 0.0.0.0

# Mode debug
python main.py --debug

# Sans rechargement automatique
python main.py --no-reload

# Combinaison
python main.py --port 8080 --debug
```

### Développement
```bash
# Mode debug avec rechargement automatique (recommandé)
python main.py --debug

# Mode production
python main.py --no-reload
```

## 📊 Flux de données

1. **main.py** → Parse les arguments CLI
2. **data_loader.py** → Charge les données depuis `rawdata.csv` (1695 enregistrements)
3. **initialize_app()** → Crée l'application Dash
4. **create_main_layout()** → Assemble le layout principal
5. **register_all_callbacks()** → Enregistre tous les callbacks
6. **app.run()** → Lance le serveur

### Flux de création des graphiques

```
data (DataFrame) → home.py (callbacks) → src/graphics/* → Plotly Figure
```

Exemple :
```python
# Dans home.py
from src.graphics import create_timed_count, create_country_details

# Callback
def update_graph(column):
    if column == 'YEAR':
        return create_timed_count(data, time_column='YEAR', value_column='COVERAGE')
    elif column == 'NAME':
        return create_country_details(data, top_n=10)
```

## 📊 Module Graphics - Architecture détaillée

### Principe : Un fichier = Un type de visualisation

Le module `src/graphics/` est organisé par **type de visualisation**, pas par métrique :

| Fichier | Responsabilité | Fonctions principales |
|---------|---------------|----------------------|
| `country_details.py` | Analyses géographiques | `create_country_details()` |
| `vaccination_table.py` | Tableaux de données | `create_vaccination_table()` |
| `map.py` | Cartes choroplèthes | `create_vaccination_map()` (TODO) |
| `pie_chart.py` | Distributions catégorielles | `create_pie_chart()` |
| `statistics.py` | Stats descriptives | `create_statistics_cards()`, `create_statistics_histogram()`, `create_statistics_boxplot()` |
| `timed_count.py` | Séries temporelles | `create_timed_count()`, `create_yearly_comparison()` |
| `tree_map.py` | Visualisations hiérarchiques | `create_tree_map()`, `create_sunburst()`, `create_hierarchical_bar()` |

### Conventions du module graphics

1. **Nommage** : Tous les fichiers en `snake_case`
2. **Fonctions** : Préfixe `create_*` + type de graphique
3. **Signature** : `(data: pd.DataFrame, **kwargs) -> go.Figure`
4. **Gestion d'erreurs** : Retour d'une figure avec annotation si erreur
5. **Documentation** : Docstrings complètes avec exemples

### Exemple de fonction graphique

```python
def create_timed_count(
    data: pd.DataFrame,
    time_column: str = 'YEAR',
    value_column: str = 'COVERAGE',
    aggregation: str = 'mean',
    title: Optional[str] = None,
    group_by: Optional[str] = None
) -> go.Figure:
    """
    Crée un graphique d'évolution temporelle.
    
    Args:
        data: DataFrame avec les données
        time_column: Colonne temporelle
        value_column: Colonne de valeurs
        aggregation: 'mean', 'sum' ou 'count'
        title: Titre personnalisé
        group_by: Colonne pour grouper
        
    Returns:
        Figure Plotly
    """
    # Vérification des données
    if time_column not in data.columns:
        return go.Figure().add_annotation(...)
    
    # Logique du graphique
    ...
    
    return fig
```

## 🏭 Pattern utilisé

### Structure main.py
```python
def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    ...

def print_startup_info(...) -> None:
    """Affiche les informations de démarrage."""
    ...

def initialize_app(data) -> dash.Dash:
    """Initialize and configure the Dash application."""
    ...

def main() -> None:
    """Main function to launch the dashboard."""
    args = parse_arguments()
    data = load_vaccination_data()  # Charge depuis rawdata.csv
    app = initialize_app(data)
    print_startup_info(...)
    app.run(...)
```

Ce pattern permet :
- ✅ Séparation claire des responsabilités
- ✅ Testabilité facile
- ✅ Configuration flexible via CLI
- ✅ Logs informatifs

## 🎨 Utilisation du module graphics

### Import simple

```python
from src.graphics import (
    create_country_details,
    create_timed_count,
    create_statistics_histogram,
    create_tree_map,
    create_pie_chart
)
```

### Dans un callback

```python
@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value')
)
def update_graph(selected_column: str) -> go.Figure:
    if selected_column == 'COVERAGE':
        return create_statistics_histogram(data, column='COVERAGE')
    elif selected_column == 'YEAR':
        return create_timed_count(data, time_column='YEAR', value_column='COVERAGE')
    elif selected_column == 'NAME':
        return create_country_details(data, top_n=10)
    else:
        return create_pie_chart(data, column=selected_column)
```

### Personnalisation

```python
# Graphique simple avec paramètres par défaut
fig = create_timed_count(data)

# Graphique personnalisé
fig = create_timed_count(
    data,
    time_column='YEAR',
    value_column='COVERAGE',
    aggregation='mean',
    group_by='ANTIGEN',
    title='Évolution de la couverture vaccinale par antigène'
)

# TreeMap hiérarchique à 3 niveaux
fig = create_tree_map(
    data,
    path=['GROUP', 'NAME', 'ANTIGEN'],
    values='COVERAGE',
    title='Hiérarchie de la couverture vaccinale'
)
```

## ✅ Bonnes pratiques respectées

- ✅ Architecture modulaire et scalable
- ✅ Type hints partout (fonctions, variables, retours)
- ✅ Docstrings pour toutes les fonctions publiques
- ✅ Configuration centralisée (`config.py`)
- ✅ Séparation des responsabilités (SRP)
- ✅ Pattern Factory pour l'app Dash
- ✅ Code DRY (Don't Repeat Yourself)
- ✅ Nommage explicite et cohérent
- ✅ Imports organisés par catégorie
- ✅ **Graphiques modulaires réutilisables**
- ✅ Gestion d'erreurs gracieuse (données vides)
- ✅ Documentation complète (README, MIGRATION)

## 📈 Évolution de l'architecture

### Version 1.0 (Initiale)
- Graphiques intégrés dans `home.py`
- Code répétitif pour chaque type de graphique
- Difficile à maintenir et étendre

### Version 2.0 (Actuelle) ⭐
- Module `src/graphics/` dédié
- 7 fichiers spécialisés par type de visualisation
- 12+ fonctions de graphiques réutilisables
- Documentation complète avec exemples
- Guide de migration v1 → v2

## 🎯 Points clés de l'architecture

1. **Modularité** : Chaque graphique est une fonction pure isolée
2. **Réutilisabilité** : Import simple, utilisation facile
3. **Extensibilité** : Ajout de nouveaux graphiques sans toucher l'existant
4. **Maintenabilité** : Code organisé, documenté, typé
5. **Testabilité** : Fonctions pures faciles à tester
6. **Scalabilité** : Structure prête pour des centaines de graphiques

## 📚 Documentation disponible

- **README.md** : Documentation générale du projet
- **ARCHITECTURE.md** : Ce fichier - Architecture technique
- **src/graphics/README.md** : Documentation du module graphics
- **src/graphics/MIGRATION.md** : Guide de migration v1 → v2
- **Docstrings** : Dans chaque fonction du code

## 🔮 Évolutions futures possibles

- [ ] Tests unitaires pour chaque fonction graphique
- [ ] Graphiques animés (évolution temporelle)
- [ ] Export des graphiques en images (PNG, SVG)
- [ ] Implémentation complète de `map.py` avec choropleth
- [ ] Graphiques radar pour comparaisons multi-dimensions
- [ ] Heatmaps de corrélation
- [ ] Dashboard de monitoring des performances
- [ ] API REST pour accès aux graphiques

---

**Date de dernière mise à jour :** 3 décembre 2025  
**Version de l'architecture :** 2.0  
**Statut :** ✅ Production ready avec 1695 enregistrements réels
