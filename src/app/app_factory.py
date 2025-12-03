from typing import Dict, Any
from dash import Dash
import dash_bootstrap_components as dbc
import pandas as pd

from src.app.layout import create_main_layout
from src.callbacks import register_all_callbacks


def create_dash_app(
    data: pd.DataFrame,
    title: str = "Vaccination Coverage Dashboard",
    external_stylesheets: list | None = None
) -> Dash:
    """
    Crée et configure une instance de l'application Dash.
    
    Args:
        data: DataFrame contenant les données à afficher
        title: Titre de l'application
        external_stylesheets: Liste des feuilles de style externes
        
    Returns:
        Instance configurée de l'application Dash
    """
    if external_stylesheets is None:
        external_stylesheets = [dbc.themes.BOOTSTRAP]
    
    # Création de l'application Dash
    app = Dash(
        __name__,
        external_stylesheets=external_stylesheets,
        title=title,
        suppress_callback_exceptions=True,
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1.0"
            }
        ]
    )
    
    # Configuration du layout
    app.layout = create_main_layout(data)
    
    # Enregistrement des callbacks
    register_all_callbacks(app, data)
    
    return app


def get_server_config(
    host: str = '127.0.0.1',
    port: int = 8050,
    debug: bool = False,
    use_reloader: bool = True
) -> Dict[str, Any]:
    """
    Retourne la configuration du serveur.
    
    Args:
        host: Adresse d'hôte du serveur
        port: Port du serveur
        debug: Active le mode debug
        use_reloader: Active le rechargement automatique
        
    Returns:
        Dictionnaire de configuration pour app.run()
    """
    return {
        'host': host,
        'port': port,
        'debug': debug,
        'use_reloader': use_reloader
    }
