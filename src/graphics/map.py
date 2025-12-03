"""
Carte géographique de la couverture vaccinale.
TODO: À implémenter avec les données géographiques.
"""

from typing import Optional
import pandas as pd
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE


def create_vaccination_map(
    data: pd.DataFrame,
    title: Optional[str] = None
) -> go.Figure:
    """
    Crée une carte choroplèthe de la couverture vaccinale par pays.
    
    Args:
        data: DataFrame contenant les données de vaccination
        title: Titre personnalisé (optionnel)
        
    Returns:
        Figure Plotly avec la carte (non implémenté pour l'instant)
    """
    # TODO: Implémenter la carte géographique
    # Nécessite des codes ISO des pays et plotly.express.choropleth
    
    fig = go.Figure()
    fig.add_annotation(
        text="Carte géographique - À implémenter",
        xref="paper", yref="paper",
        x=0.5, y=0.5, 
        showarrow=False,
        font=dict(size=20)
    )
    
    default_title = 'Carte mondiale de la couverture vaccinale'
    fig.update_layout(
        title=title or default_title,
        template=PLOTLY_TEMPLATE
    )
    
    return fig
