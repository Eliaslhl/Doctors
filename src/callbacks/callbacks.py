import pandas as pd

from src.pages.home import register_callbacks as register_home_callbacks


def register_all_callbacks(app, data: pd.DataFrame) -> None:
    """
    Enregistre tous les callbacks de l'application.
    
    Args:
        app: Instance de l'application Dash
        data: DataFrame contenant les données
    """
    
    register_home_callbacks(app, data)
    
    # TODO: Ajouter d'autres callbacks ici si nécessaire
