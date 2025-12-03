"""
Tableau de données de vaccination.
"""

from typing import Optional
import pandas as pd
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE


def create_vaccination_table(
    data: pd.DataFrame,
    max_rows: int = 50,
    title: Optional[str] = None
) -> go.Figure:
    """
    Crée un tableau interactif avec les données de vaccination.
    
    Args:
        data: DataFrame contenant les données de vaccination
        max_rows: Nombre maximum de lignes à afficher
        title: Titre personnalisé (optionnel)
        
    Returns:
        Figure Plotly avec le tableau
    """
    if data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Limiter le nombre de lignes
    display_data = data.head(max_rows)
    
    # Créer le tableau
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(display_data.columns),
            fill_color='paleturquoise',
            align='left',
            font=dict(size=12, color='black')
        ),
        cells=dict(
            values=[display_data[col] for col in display_data.columns],
            fill_color='lavender',
            align='left',
            font=dict(size=11)
        )
    )])
    
    default_title = f'Données de vaccination ({len(display_data)} lignes)'
    fig.update_layout(
        title=title or default_title,
        template=PLOTLY_TEMPLATE
    )
    
    return fig
