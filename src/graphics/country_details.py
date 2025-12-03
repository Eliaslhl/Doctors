"""
Graphique détaillé des pays - Top pays par couverture vaccinale.
"""

from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE, COLOR_PALETTE


def create_country_details(
    data: pd.DataFrame,
    top_n: int = 10,
    title: Optional[str] = None
) -> go.Figure:
    """
    Crée un graphique en barres horizontales des pays avec la meilleure couverture moyenne.
    
    Args:
        data: DataFrame contenant les données de vaccination
        top_n: Nombre de pays à afficher
        title: Titre personnalisé (optionnel)
        
    Returns:
        Figure Plotly avec le graphique en barres
    """
    if 'NAME' not in data.columns or 'COVERAGE' not in data.columns or data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Calcul de la couverture moyenne par pays
    country_data = data.groupby('NAME')['COVERAGE'].mean().sort_values(ascending=False).head(top_n)
    
    default_title = f'Top {top_n} pays - Couverture moyenne'
    fig = px.bar(
        x=country_data.values,
        y=country_data.index,
        orientation='h',
        title=title or default_title,
        labels={'x': 'Couverture moyenne (%)', 'y': 'Pays'},
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig.update_layout(
        xaxis_title='Couverture moyenne (%)',
        yaxis_title='Pays',
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig
