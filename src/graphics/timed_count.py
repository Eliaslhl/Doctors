"""
Graphique d'évolution temporelle de la couverture vaccinale.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import COLOR_PALETTE, PLOTLY_TEMPLATE


def create_timed_count(
    data: pd.DataFrame,
    time_column: str = "YEAR",
    value_column: str = "COVERAGE",
    aggregation: str = "mean",
    title: str | None = None,
    group_by: str | None = None,
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
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )

    # Agrégation des données
    if group_by and group_by in data.columns:
        # Évolution par groupe
        if aggregation == "mean":
            time_data = data.groupby([time_column, group_by])[value_column].mean().reset_index()
        elif aggregation == "sum":
            time_data = data.groupby([time_column, group_by])[value_column].sum().reset_index()
        else:  # count
            time_data = data.groupby([time_column, group_by]).size().reset_index(name=value_column)

        fig = px.line(
            time_data,
            x=time_column,
            y=value_column,
            color=group_by,
            title=title or f"Évolution de {value_column} par {group_by}",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_PALETTE,
            markers=True,
        )
    else:
        # Évolution globale
        if aggregation == "mean":
            time_data = data.groupby(time_column)[value_column].mean().reset_index()
        elif aggregation == "sum":
            time_data = data.groupby(time_column)[value_column].sum().reset_index()
        else:  # count
            time_data = data.groupby(time_column).size().reset_index(name=value_column)

        default_title = f"Évolution de {value_column} dans le temps"
        fig = px.line(
            time_data,
            x=time_column,
            y=value_column,
            title=title or default_title,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_PALETTE,
            markers=True,
        )

    fig.update_layout(xaxis_title=time_column, yaxis_title=value_column, hovermode="x unified")

    return fig
