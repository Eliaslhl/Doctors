"""
Configuration globale de l'application Vaccination Coverage Dashboard.

Ce module centralise toutes les configurations et constantes de l'application.
"""

from pathlib import Path
from typing import Any

# ========================================
# CHEMINS DE FICHIERS
# ========================================

BASE_DIR: Path = Path(__file__).parent
DATA_DIR: Path = BASE_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
CLEANED_DATA_DIR: Path = DATA_DIR / "cleaned"


# ========================================
# CONFIGURATION DASH
# ========================================

# Configuration par défaut de Plotly
PLOTLY_CONFIG: dict[str, Any] = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["pan2d", "lasso2d", "select2d"],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "graph_export",
        "height": 800,
        "width": 1200,
        "scale": 2,
    },
}

# Palette de couleurs
COLOR_PALETTE: list[str] = [
    "#3498db",  # Bleu
    "#e74c3c",  # Rouge
    "#2ecc71",  # Vert
    "#f39c12",  # Orange
    "#9b59b6",  # Violet
    "#1abc9c",  # Turquoise
    "#34495e",  # Gris foncé
    "#e67e22",  # Orange foncé
]

# Template des graphiques
PLOTLY_TEMPLATE: str = "plotly_white"
