"""
Carte géographique de la couverture vaccinale.
Optimisée pour afficher le fond de carte mondial interactif (type OSM/Leaflet) SANS données réelles.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE


def create_vaccination_map(data: pd.DataFrame, title: str | None = None) -> go.Figure:
    """
    Crée une carte de fond interactive (type OSM/Leaflet) centrée sur le monde.
    Crée une carte choroplèthe de la couverture vaccinale par pays.

    Args:
        data: DataFrame (utilisé uniquement pour le fond de carte ou des données factices)
        title: Titre personnalisé (optionnel)

    Returns:
        Figure Plotly avec le fond de carte OSM interactif.
    """
    
    default_title = 'Carte mondiale interactive (Visuel OSM)'
        # 1. Utilisation de données factices pour forcer l'affichage de la carte
    dummy_data = {
        'lat': [0], 
        'lon': [0], 
        'label': ['Centre du Monde']
    }
    dummy_df = pd.DataFrame(dummy_data)
    
    # 2. Création de la figure avec un point unique invisible
    fig = px.scatter_mapbox(
        dummy_df, 
        lat="lat", 
        lon="lon", 
        hover_name="label",
        zoom=1,
    )

    # 3. Configuration du layout pour le style et le centrage
    fig.update_layout(
        title={
            'text': title or default_title,
            'x': 0.5,
            'xanchor': 'center'
        },
        
        # Configuration clé pour le style Leaflet/OSM
        mapbox_style="open-street-map",
        mapbox_center={"lat": 0, "lon": 0}, # Centrage initial
        mapbox_zoom=1, 
        showlegend=False,
        height=500,
        template=PLOTLY_TEMPLATE
    )    
    return fig
