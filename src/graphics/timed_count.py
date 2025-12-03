"""
Graphique d'évolution temporelle de la couverture vaccinale.
"""

from typing import Optional, List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE, COLOR_PALETTE


def create_timed_count(
    data: pd.DataFrame,
    time_column: str = 'YEAR',
    value_column: str = 'COVERAGE',
    aggregation: str = 'mean',
    title: Optional[str] = None,
    group_by: Optional[str] = None
) -> go.Figure:
    """
    Crée un graphique en ligne montrant l'évolution temporelle.
    
    Args:
        data: DataFrame contenant les données de vaccination
        time_column: Colonne temporelle (YEAR par défaut)
        value_column: Colonne de valeurs à agréger
        aggregation: Type d'agrégation ('mean', 'sum', 'count')
        title: Titre personnalisé (optionnel)
        group_by: Colonne pour créer plusieurs séries (optionnel)
        
    Returns:
        Figure Plotly avec le graphique en ligne
    """
    if time_column not in data.columns or value_column not in data.columns or data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Agrégation des données
    if group_by and group_by in data.columns:
        # Évolution par groupe
        if aggregation == 'mean':
            time_data = data.groupby([time_column, group_by])[value_column].mean().reset_index()
        elif aggregation == 'sum':
            time_data = data.groupby([time_column, group_by])[value_column].sum().reset_index()
        else:  # count
            time_data = data.groupby([time_column, group_by]).size().reset_index(name=value_column)
        
        fig = px.line(
            time_data,
            x=time_column,
            y=value_column,
            color=group_by,
            title=title or f'Évolution de {value_column} par {group_by}',
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_PALETTE,
            markers=True
        )
    else:
        # Évolution globale
        if aggregation == 'mean':
            time_data = data.groupby(time_column)[value_column].mean().reset_index()
        elif aggregation == 'sum':
            time_data = data.groupby(time_column)[value_column].sum().reset_index()
        else:  # count
            time_data = data.groupby(time_column).size().reset_index(name=value_column)
        
        default_title = f'Évolution de {value_column} dans le temps'
        fig = px.line(
            time_data,
            x=time_column,
            y=value_column,
            title=title or default_title,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_PALETTE,
            markers=True
        )
    
    fig.update_layout(
        xaxis_title=time_column,
        yaxis_title=value_column,
        hovermode='x unified'
    )
    
    return fig


def create_yearly_comparison(
    data: pd.DataFrame,
    years: Optional[List[int]] = None,
    metric: str = 'COVERAGE',
    title: Optional[str] = None
) -> go.Figure:
    """
    Crée un graphique de comparaison entre différentes années.
    
    Args:
        data: DataFrame contenant les données de vaccination
        years: Liste d'années à comparer (None = toutes)
        metric: Métrique à comparer
        title: Titre personnalisé (optionnel)
        
    Returns:
        Figure Plotly avec le graphique de comparaison
    """
    if 'YEAR' not in data.columns or metric not in data.columns or data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Filtrer par années si spécifié
    if years:
        data = data[data['YEAR'].isin(years)]
    
    # Calculer les moyennes par année
    yearly_data = data.groupby('YEAR')[metric].mean().reset_index()
    
    fig = go.Figure(data=[go.Bar(
        x=yearly_data['YEAR'],
        y=yearly_data[metric],
        marker_color=COLOR_PALETTE[0]
    )])
    
    default_title = f'Comparaison annuelle - {metric}'
    fig.update_layout(
        title=title or default_title,
        xaxis_title='Année',
        yaxis_title=f'{metric} moyen',
        template=PLOTLY_TEMPLATE
    )
    
    return fig
