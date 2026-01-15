"""
Carte géographique de la couverture vaccinale.
Optimisée pour afficher le fond de carte mondial interactif (type OSM/Leaflet) SANS données réelles.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE


def create_vaccination_map(data: pd.DataFrame, title: str | None = None) -> go.Figure:
    """
    Crée une carte de fond interactive (type OSM/Leaflet) centrée sur le monde.
    Crée une carte choroplèthe de la couverture vaccinale par pays.

    Args:
        data: DataFrame (utilisé uniquement pour le fond de carte ou des données factices)
        title: Titre personnalisé (optionnel)

    Returns:
        Figure Plotly avec le fond de carte OSM interactif.
    """
    # 1. Vérification des données (comme dans ton autre fonction)
    if "NAME" not in data.columns or "COVERAGE" not in data.columns or data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible pour la carte",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )

    # 2. Préparation des données : Moyenne par pays
    # On reset_index() pour que 'NAME' redevenue une colonne utilisable par Plotly
    df_map = data.groupby("NAME")["COVERAGE"].mean().reset_index()

    # 3. Création de la carte Choroplèthe
    fig = px.choropleth(
        data_frame=df_map,
        locations="NAME",  # La colonne contenant les noms des pays
        locationmode="country names",  # Indique à Plotly d'utiliser les noms (France, Canada, etc.)
        color="COVERAGE",  # La donnée qui définit la couleur
        hover_name="NAME",  # Ce qui s'affiche au survol
        color_continuous_scale=px.colors.sequential.Viridis,  # Échelle de couleur (ex: Viridis, Plasma, Blues)
        projection="natural earth",  # Type de vue (on peut bouger et zoomer dessus)
        labels={"COVERAGE": "Couverture (%)"},
    )

    # 4. Configuration du Layout et de la taille
    default_title = "Couverture vaccinale mondiale par pays"
    fig.update_layout(
        title={"text": title or default_title, "x": 0.5, "xanchor": "center"},
        template=PLOTLY_TEMPLATE,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},  # Optimise l'espace
        # Cette partie permet de garder la carte "bougeable"
        dragmode="pan",
    )

    return fig
