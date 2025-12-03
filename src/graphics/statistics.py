"""
Statistiques et indicateurs clés de vaccination.
"""

from typing import Optional, Dict, Any
import pandas as pd
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE, COLOR_PALETTE


def create_statistics_cards(
    data: pd.DataFrame
) -> Dict[str, Any]:
    """
    Calcule les statistiques principales pour les cartes d'indicateurs.
    
    Args:
        data: DataFrame contenant les données de vaccination
        
    Returns:
        Dictionnaire avec les statistiques calculées
    """
    if data.empty:
        return {
            'n_countries': 0,
            'n_years': 0,
            'avg_coverage': 0.0,
            'total_records': 0,
            'n_antigens': 0,
            'max_coverage': 0.0,
            'min_coverage': 0.0
        }
    
    stats = {
        'n_countries': int(data['NAME'].nunique()) if 'NAME' in data.columns else 0,
        'n_years': int(data['YEAR'].nunique()) if 'YEAR' in data.columns else 0,
        'avg_coverage': float(data['COVERAGE'].mean()) if 'COVERAGE' in data.columns else 0.0,
        'total_records': len(data),
        'n_antigens': int(data['ANTIGEN'].nunique()) if 'ANTIGEN' in data.columns else 0,
        'max_coverage': float(data['COVERAGE'].max()) if 'COVERAGE' in data.columns else 0.0,
        'min_coverage': float(data['COVERAGE'].min()) if 'COVERAGE' in data.columns else 0.0
    }
    
    return stats


def create_statistics_histogram(
    data: pd.DataFrame,
    column: str = 'COVERAGE',
    nbins: int = 30,
    title: Optional[str] = None
) -> go.Figure:
    """
    Crée un histogramme pour visualiser la distribution statistique.
    
    Args:
        data: DataFrame contenant les données de vaccination
        column: Colonne à visualiser
        nbins: Nombre de bins pour l'histogramme
        title: Titre personnalisé (optionnel)
        
    Returns:
        Figure Plotly avec l'histogramme
    """
    if column not in data.columns or data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure(data=[go.Histogram(
        x=data[column],
        nbinsx=nbins,
        marker_color=COLOR_PALETTE[0]
    )])
    
    default_title = f'Distribution statistique - {column}'
    fig.update_layout(
        title=title or default_title,
        xaxis_title=column,
        yaxis_title='Fréquence',
        template=PLOTLY_TEMPLATE,
        showlegend=False
    )
    
    return fig


def create_statistics_boxplot(
    data: pd.DataFrame,
    column: str = 'COVERAGE',
    group_by: Optional[str] = None,
    title: Optional[str] = None
) -> go.Figure:
    """
    Crée un boxplot pour les statistiques descriptives.
    
    Args:
        data: DataFrame contenant les données de vaccination
        column: Colonne numérique à analyser
        group_by: Colonne pour grouper les données (optionnel)
        title: Titre personnalisé (optionnel)
        
    Returns:
        Figure Plotly avec le boxplot
    """
    if column not in data.columns or data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    if group_by and group_by in data.columns:
        # Boxplot groupé
        fig = go.Figure()
        for i, category in enumerate(data[group_by].unique()):
            category_data = data[data[group_by] == category][column]
            fig.add_trace(go.Box(
                y=category_data,
                name=str(category),
                marker_color=COLOR_PALETTE[i % len(COLOR_PALETTE)]
            ))
        default_title = f'Statistiques de {column} par {group_by}'
    else:
        # Boxplot simple
        fig = go.Figure(data=[go.Box(
            y=data[column],
            marker_color=COLOR_PALETTE[0]
        )])
        default_title = f'Statistiques descriptives - {column}'
    
    fig.update_layout(
        title=title or default_title,
        yaxis_title=column,
        template=PLOTLY_TEMPLATE
    )
    
    return fig
