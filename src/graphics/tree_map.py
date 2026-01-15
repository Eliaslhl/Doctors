"""
Graphique TreeMap pour visualisation hiérarchique des données.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import COLOR_PALETTE, PLOTLY_TEMPLATE


def create_tree_map(
    data: pd.DataFrame, path: list[str], values: str = "COVERAGE", title: str | None = None
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
    # Vérifie que toutes les colonnes existent
    missing_columns = [col for col in path + [values] if col not in data.columns]
    if missing_columns or data.empty:
        return go.Figure().add_annotation(
            text=f"Colonnes manquantes: {missing_columns}"
            if missing_columns
            else "Aucune donnée disponible",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )

    # Crée le TreeMap
    default_title = f"TreeMap hiérarchique - {' → '.join(path)}"
    fig = px.treemap(
        data,
        path=path,
        values=values,
        title=title or default_title,
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE,
    )

    fig.update_traces(textposition="middle center", textfont_size=12)

    fig.update_layout(margin={"t": 50, "l": 25, "r": 25, "b": 25})

    return fig
