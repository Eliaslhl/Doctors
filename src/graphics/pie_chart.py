"""
Graphiques en camembert pour les distributions catégorielles.
"""

from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE, COLOR_PALETTE


def create_pie_chart(
    data: pd.DataFrame,
    column: str = 'COVERAGE_CATEGORY',
    title: Optional[str] = None,
    max_categories: int = 10
) -> go.Figure:
    """
    Crée un graphique en camembert pour une colonne catégorielle.
    
    Args:
        data: DataFrame contenant les données de vaccination
        column: Nom de la colonne à visualiser
        title: Titre personnalisé (optionnel)
        max_categories: Nombre maximum de catégories à afficher
        
    Returns:
        Figure Plotly avec le graphique en camembert
    """
    if column not in data.columns or data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Comptage des valeurs (top N si trop de catégories)
    value_counts = data[column].value_counts()
    if len(value_counts) > max_categories:
        value_counts = value_counts.head(max_categories)
    
    default_title = f'Répartition - {column}'
    fig = px.pie(
        values=value_counts.values,
        names=value_counts.index,
        title=title or default_title,
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )
    
    return fig
