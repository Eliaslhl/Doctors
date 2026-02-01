"""
Graphique détaillé des pays - Top pays par couverture vaccinale.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import PLOTLY_TEMPLATE


def create_country_details(
    data: pd.DataFrame, top_n: int = 10, title: str | None = None
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
    if "NAME" not in data.columns or "COVERAGE" not in data.columns or data.empty:
        return go.Figure().add_annotation(
            text="Aucune donnée disponible",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )

    # Calcul de la couverture moyenne par pays
    country_stats = data.groupby("NAME").agg({"COVERAGE": ["mean", "std", "count"]}).reset_index()
    country_stats.columns = ["NAME", "COVERAGE_MEAN", "COVERAGE_STD", "N_RECORDS"]
    country_stats = country_stats.sort_values("COVERAGE_MEAN", ascending=False).head(top_n)

    if len(country_stats) == top_n:
        default_title = f"Top {top_n} pays - Couverture moyenne"
    else:
        default_title = f"Pays par couverture moyenne ({len(country_stats)} pays)"

    fig = go.Figure()

    # Ajout des barres avec gradient de couleur
    if len(country_stats) > 1:
        colors = px.colors.sample_colorscale(
            "RdYlGn", [n / (len(country_stats) - 1) for n in range(len(country_stats))]
        )
    else:
        colors = ["#90EE90"]  # Couleur par défaut si un seul pays

    fig.add_trace(
        go.Bar(
            x=country_stats["COVERAGE_MEAN"],
            y=country_stats["NAME"],
            orientation="h",
            marker={"color": colors},
            text=country_stats["COVERAGE_MEAN"].round(1),
            textposition="auto",
            texttemplate="%{text}%",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Couverture moyenne: %{x:.1f}%<br>"
                "Écart-type: %{customdata[0]:.1f}%<br>"
                "Nombre d'enregistrements: %{customdata[1]}<br>"
                "<extra></extra>"
            ),
            customdata=country_stats[["COVERAGE_STD", "N_RECORDS"]].values,
        )
    )

    fig.update_layout(
        title=title or default_title,
        template=PLOTLY_TEMPLATE,
        xaxis_title="Couverture moyenne (%)",
        yaxis_title="Pays",
        yaxis={"categoryorder": "total ascending"},
        showlegend=False,
        height=max(400, top_n * 40),  # Hauteur dynamique
    )

    return fig
