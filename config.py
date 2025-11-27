"""
Configuration de l'application Doctors Dashboard.
"""

import os
from pathlib import Path

# ========================================
# CHEMINS DE FICHIERS
# ========================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = BASE_DIR / "images"


# ========================================
# CONFIGURATION SERVEUR
# ========================================

# Configuration par défaut du serveur
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8050
DEFAULT_DEBUG = False


# ========================================
# CONFIGURATION DASH
# ========================================

# Titre de l'application
APP_TITLE = "Doctors Dashboard"
APP_UPDATE_TITLE = "Chargement..."

# Suppression des exceptions de callback
SUPPRESS_CALLBACK_EXCEPTIONS = True


# ========================================
# CONFIGURATION DES GRAPHIQUES
# ========================================

# Configuration par défaut de Plotly
PLOTLY_CONFIG = {
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
COLOR_PALETTE = [
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
PLOTLY_TEMPLATE = "plotly_white"

# ========================================
# MESSAGES
# ========================================

MESSAGES = {
    'no_data': "Aucune donnée disponible",
    'loading': "Chargement en cours...",
    'error': "Une erreur s'est produite",
    'success': "Opération réussie",
}
