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

## 🏗️ Principes d'architecture

### 1. **Séparation des responsabilités**
- `main.py` : Point d'entrée uniquement, lance l'application
- `src/app/` : Création et configuration de l'application
- `src/components/` : Composants UI réutilisables
- `src/pages/` : Pages avec leur layout et logique
- `src/callbacks/` : Logique interactive (callbacks Dash)
- `src/utils/` : Fonctions utilitaires

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
2. **data_loader.py** → Génère/charge les données (700 enregistrements)
3. **initialize_app()** → Crée l'application Dash
4. **create_main_layout()** → Assemble le layout principal
5. **register_all_callbacks()** → Enregistre tous les callbacks
6. **app.run()** → Lance le serveur

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
    data = generate_sample_vaccination_data()
    app = initialize_app(data)
    print_startup_info(...)
    app.run(...)
```

Ce pattern permet :
- ✅ Séparation claire des responsabilités
- ✅ Testabilité facile
- ✅ Configuration flexible via CLI
- ✅ Logs informatifs

## ✅ Bonnes pratiques respectées

- ✅ Architecture modulaire
- ✅ Type hints partout
- ✅ Docstrings pour toutes les fonctions publiques
- ✅ Configuration centralisée
- ✅ Séparation des responsabilités
- ✅ Pattern Factory
- ✅ Code DRY
- ✅ Nommage explicite
- ✅ Imports organisés
