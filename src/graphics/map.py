"""
Carte géographique de la couverture vaccinale.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE


def create_vaccination_map(data: pd.DataFrame, title: str | None = None) -> go.Figure:
    """
    Crée une carte choroplèthe de la couverture vaccinale par pays.

    Args:
        data: DataFrame contenant les données de vaccination
        title: Titre personnalisé (optionnel)

    Returns:
        Figure Plotly avec la carte choroplèthe interactive
    """
    if "NAME" not in data.columns or "COVERAGE" not in data.columns or data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible pour la carte",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )

    # Préparation des données : Moyenne par pays
    df_map = data.groupby("NAME").agg({"COVERAGE": "mean", "YEAR": "count"}).reset_index()
    df_map.columns = ["NAME", "COVERAGE", "N_RECORDS"]

    # Création de la carte choroplèthe avec tooltips enrichis
    fig = px.choropleth(
        data_frame=df_map,
        locations="NAME",
        locationmode="country names",
        color="COVERAGE",
        hover_name="NAME",
        hover_data={
            "COVERAGE": ":.1f",
            "N_RECORDS": True,
            "NAME": False,
        },
        color_continuous_scale=[
            [0.0, "#d73027"],  # Rouge pour faible couverture
            [0.5, "#fee08b"],  # Jaune pour couverture moyenne
            [1.0, "#1a9850"],  # Vert pour haute couverture
        ],
        projection="natural earth",
        labels={
            "COVERAGE": "Couverture moyenne (%)",
            "N_RECORDS": "Nombre d'enregistrements",
        },
    )

    # Configuration du layout
    default_title = "Couverture vaccinale mondiale par pays"
    fig.update_layout(
        title={"text": title or default_title, "x": 0.5, "xanchor": "center"},
        template=PLOTLY_TEMPLATE,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        dragmode="pan",
    )

    return fig
