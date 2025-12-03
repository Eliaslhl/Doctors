from dash import html
import pandas as pd

from src.components.header import create_sidebar
from src.components.footer import create_footer
from src.pages.home import create_home_layout


def create_main_layout(data: pd.DataFrame) -> html.Div:
    """
    Crée le layout principal de l'application.
    
    Args:
        data: DataFrame contenant les données à afficher
        
    Returns:
        Layout principal de l'application
    """
    return html.Div([
        # Sidebar gauche avec filtre
        create_sidebar(data),
        
        # Contenu principal
        html.Div([
            html.Div([
                create_home_layout(data)
            ], className='container'),
            
            create_footer()
        ], className='main-content')
    ], className='app-container')
