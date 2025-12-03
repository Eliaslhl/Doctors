"""
Configuration globale de l'application Vaccination Coverage Dashboard.

Ce module centralise toutes les configurations et constantes de l'application.
"""

import os
from pathlib import Path
from typing import Dict, List, Any


# ========================================
# CHEMINS DE FICHIERS
# ========================================

BASE_DIR: Path = Path(__file__).parent
DATA_DIR: Path = BASE_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
CLEANED_DATA_DIR: Path = DATA_DIR / "cleaned"
ASSETS_DIR: Path = BASE_DIR / "assets"
IMAGES_DIR: Path = BASE_DIR / "images"


# ========================================
# CONFIGURATION SERVEUR
# ========================================

# Configuration par défaut du serveur
DEFAULT_HOST: str = "127.0.0.1"
DEFAULT_PORT: int = 8050
DEFAULT_DEBUG: bool = False


# ========================================
# CONFIGURATION DASH
# ========================================

# Titre de l'application
APP_TITLE: str = "Vaccination Coverage Dashboard"
APP_UPDATE_TITLE: str = "Chargement..."

# Suppression des exceptions de callback
SUPPRESS_CALLBACK_EXCEPTIONS: bool = True


# ========================================
# CONFIGURATION DES GRAPHIQUES
# ========================================

# Configuration par défaut de Plotly
PLOTLY_CONFIG: Dict[str, Any] = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'graph_export',
        'height': 800,
        'width': 1200,
        'scale': 2
    }
}

# Palette de couleurs
COLOR_PALETTE: List[str] = [
    '#3498db',  # Bleu
    '#e74c3c',  # Rouge
    '#2ecc71',  # Vert
    '#f39c12',  # Orange
    '#9b59b6',  # Violet
    '#1abc9c',  # Turquoise
    '#34495e',  # Gris foncé
    '#e67e22',  # Orange foncé
]

# Template des graphiques
PLOTLY_TEMPLATE: str = "plotly_white"

# ========================================
# MESSAGES
# ========================================

MESSAGES: Dict[str, str] = {
    'no_data': "Aucune donnée disponible",
    'loading': "Chargement en cours...",
    'error': "Une erreur s'est produite",
    'success': "Opération réussie",
}
