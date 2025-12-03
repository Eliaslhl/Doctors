"""
Graphique TreeMap pour visualisation hiérarchique des données.
"""

from typing import Optional, List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE, COLOR_PALETTE


def create_tree_map(
    data: pd.DataFrame,
    path: List[str],
    values: str = 'COVERAGE',
    title: Optional[str] = None
) -> go.Figure:
    """
    Crée un TreeMap pour visualiser des données hiérarchiques.
    
    Args:
        data: DataFrame contenant les données de vaccination
        path: Liste des colonnes définissant la hiérarchie (ex: ['GROUP', 'NAME', 'ANTIGEN'])
        values: Colonne contenant les valeurs numériques
        title: Titre personnalisé (optionnel)
        
    Returns:
        Figure Plotly avec le TreeMap
    """
    # Vérifier que toutes les colonnes existent
    missing_columns = [col for col in path + [values] if col not in data.columns]
    if missing_columns or data.empty:
        return go.Figure().add_annotation(
            text=f"Colonnes manquantes: {missing_columns}" if missing_columns else "Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Créer le TreeMap
    default_title = f'TreeMap hiérarchique - {" → ".join(path)}'
    fig = px.treemap(
        data,
        path=path,
        values=values,
        title=title or default_title,
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig.update_traces(
        textposition='middle center',
        textfont_size=12
    )
    
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25)
    )
    
    return fig


def create_sunburst(
    data: pd.DataFrame,
    path: List[str],
    values: str = 'COVERAGE',
    title: Optional[str] = None
) -> go.Figure:
    """
    Crée un graphique Sunburst (diagramme en rayons de soleil) pour visualisation hiérarchique.
    
    Args:
        data: DataFrame contenant les données de vaccination
        path: Liste des colonnes définissant la hiérarchie
        values: Colonne contenant les valeurs numériques
        title: Titre personnalisé (optionnel)
        
    Returns:
        Figure Plotly avec le Sunburst
    """
    # Vérifier que toutes les colonnes existent
    missing_columns = [col for col in path + [values] if col not in data.columns]
    if missing_columns or data.empty:
        return go.Figure().add_annotation(
            text=f"Colonnes manquantes: {missing_columns}" if missing_columns else "Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Créer le Sunburst
    default_title = f'Sunburst hiérarchique - {" → ".join(path)}'
    fig = px.sunburst(
        data,
        path=path,
        values=values,
        title=title or default_title,
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig.update_traces(
        textfont_size=12
    )
    
    return fig


def create_hierarchical_bar(
    data: pd.DataFrame,
    category_column: str,
    subcategory_column: str,
    value_column: str = 'COVERAGE',
    top_n: int = 10,
    title: Optional[str] = None
) -> go.Figure:
    """
    Crée un graphique en barres groupées pour montrer une hiérarchie.
    
    Args:
        data: DataFrame contenant les données de vaccination
        category_column: Colonne de la catégorie principale
        subcategory_column: Colonne de la sous-catégorie
        value_column: Colonne des valeurs
        top_n: Nombre de catégories principales à afficher
        title: Titre personnalisé (optionnel)
        
    Returns:
        Figure Plotly avec le graphique en barres groupées
    """
    required_columns = [category_column, subcategory_column, value_column]
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns or data.empty:
        return go.Figure().add_annotation(
            text=f"Colonnes manquantes: {missing_columns}" if missing_columns else "Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Agréger les données
    grouped_data = data.groupby([category_column, subcategory_column])[value_column].mean().reset_index()
    
    # Filtrer les top N catégories
    top_categories = grouped_data.groupby(category_column)[value_column].mean().nlargest(top_n).index
    grouped_data = grouped_data[grouped_data[category_column].isin(top_categories)]
    
    default_title = f'{category_column} par {subcategory_column} (Top {top_n})'
    fig = px.bar(
        grouped_data,
        x=category_column,
        y=value_column,
        color=subcategory_column,
        title=title or default_title,
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE,
        barmode='group'
    )
    
    fig.update_layout(
        xaxis_title=category_column,
        yaxis_title=f'{value_column} moyen',
        xaxis_tickangle=-45
    )
    
    return fig
