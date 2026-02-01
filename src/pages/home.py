import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
from dash.dash_table import DataTable

from config import PLOTLY_CONFIG
from src.graphics import (
    create_country_details,
    create_pie_chart,
    create_statistics_boxplot,
    create_statistics_cards,
    create_statistics_histogram,
    create_timed_count,
    create_tree_map,
    create_vaccination_map,
)
from src.utils.get_data import get_filtered_data


def create_home_layout(data: pd.DataFrame) -> html.Div:
    """
    Crée le layout de la page d'accueil.

    Args:
        data: DataFrame contenant les données de vaccination

    Returns:
        Layout Dash de la page d'accueil
    """
    return html.Div(
        [
            html.H1("Dashboard - Vaccination Coverage", className="page-title"),
            html.Hr(),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "📊 Statistiques Globales",
                                style={
                                    "display": "inline-block",
                                    "marginRight": "10px",
                                    "fontSize": "18px",
                                    "color": "#2c3e50",
                                    "marginBottom": "15px",
                                },
                            ),
                            html.Span(
                                "Filtrées par année uniquement",
                                style={
                                    "backgroundColor": "#f39c12",
                                    "color": "white",
                                    "padding": "4px 12px",
                                    "borderRadius": "12px",
                                    "fontSize": "11px",
                                    "fontWeight": "bold",
                                },
                            ),
                        ],
                        style={"marginBottom": "10px"},
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3("Pays", className="stat-title"),
                                    html.H2(
                                        id="stat-countries", children="—", className="stat-value"
                                    ),
                                ],
                                className="card stat-card",
                            )
                        ],
                        className="col",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3("Années", className="stat-title"),
                                    html.H2(id="stat-years", children="—", className="stat-value"),
                                ],
                                className="card stat-card",
                            )
                        ],
                        className="col",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3("Couverture moyenne", className="stat-title"),
                                    html.H2(
                                        id="stat-coverage", children="—", className="stat-value"
                                    ),
                                ],
                                className="card stat-card",
                            )
                        ],
                        className="col",
                    ),
                ],
                className="row stats-row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "🔄 Données Filtrées",
                                style={
                                    "display": "inline-block",
                                    "marginRight": "10px",
                                    "fontSize": "18px",
                                    "color": "#2c3e50",
                                    "marginTop": "30px",
                                    "marginBottom": "15px",
                                },
                            ),
                            html.Span(
                                "Affectés par les filtres de la sidebar",
                                style={
                                    "backgroundColor": "#27ae60",
                                    "color": "white",
                                    "padding": "4px 12px",
                                    "borderRadius": "12px",
                                    "fontSize": "11px",
                                    "fontWeight": "bold",
                                },
                            ),
                        ],
                        style={"marginBottom": "15px"},
                    ),
                ],
                className="row",
            ),
            # Section de la carte de vaccination
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Carte de la couverture vaccinale", className="card-title"),
                            dcc.Graph(
                                id="vaccination-map",
                                config=PLOTLY_CONFIG,  # type: ignore
                                style={"height": "500px", "width": "75vw", "text-align": "center"},
                            ),
                        ],
                        className="card map-container",
                    )
                ],
                className="row",
            ),
            # Pays par Couverture + Évolution Temporelle
            html.Div(
                [
                    # Pays par Couverture
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "📊 Pays par Couverture Moyenne", className="card-title"
                                    ),
                                    dcc.Graph(
                                        id="country-details-graph",
                                        config=PLOTLY_CONFIG,  # type: ignore
                                    ),
                                ],
                                className="card graph-container",
                            )
                        ],
                        className="col",
                    ),
                    # Évolution Temporelle
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "📈 Évolution de la Couverture dans le Temps",
                                        className="card-title",
                                    ),
                                    dcc.Graph(
                                        id="timed-count-graph",
                                        config=PLOTLY_CONFIG,  # type: ignore
                                    ),
                                ],
                                className="card graph-container",
                            )
                        ],
                        className="col",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.H3(
                        "🔍 Exploration des Données",
                        className="section-title",
                        style={"marginTop": "30px", "marginBottom": "10px", "color": "#2c3e50"},
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H3(
                                                "📊 Analyse de Distribution",
                                                className="card-title",
                                                style={
                                                    "display": "inline-block",
                                                    "marginRight": "10px",
                                                },
                                            ),
                                            html.Span(
                                                "Première Vue",
                                                style={
                                                    "backgroundColor": "#3498db",
                                                    "color": "white",
                                                    "padding": "4px 12px",
                                                    "borderRadius": "12px",
                                                    "fontSize": "12px",
                                                    "fontWeight": "bold",
                                                },
                                            ),
                                        ],
                                        style={"marginBottom": "10px"},
                                    ),
                                    html.P(
                                        "Visualisez les distributions et quartiles des données",
                                        style={
                                            "color": "#7f8c8d",
                                            "fontSize": "13px",
                                            "marginBottom": "10px",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Type de graphique:", className="dropdown-label"
                                            ),
                                            dcc.Dropdown(
                                                id="graph-type-1",
                                                options=[  # type: ignore
                                                    {
                                                        "label": "📊 Histogram - Distribution des valeurs",
                                                        "value": "histogram",
                                                    },
                                                    {
                                                        "label": "📦 Boxplot - Quartiles et outliers",
                                                        "value": "boxplot",
                                                    },
                                                ],
                                                value="histogram",
                                                clearable=False,
                                                className="custom-dropdown",
                                            ),
                                        ],
                                        className="dropdown-container",
                                        style={"marginTop": "10px"},
                                    ),
                                    dcc.Graph(
                                        id="exploration-graph-1",
                                        config=PLOTLY_CONFIG,  # type: ignore
                                    ),
                                ],
                                className="card graph-container",
                            )
                        ],
                        className="col",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H3(
                                                "🗂️ Analyse de Composition",
                                                className="card-title",
                                                style={
                                                    "display": "inline-block",
                                                    "marginRight": "10px",
                                                },
                                            ),
                                            html.Span(
                                                "Comparaison",
                                                style={
                                                    "backgroundColor": "#e74c3c",
                                                    "color": "white",
                                                    "padding": "4px 12px",
                                                    "borderRadius": "12px",
                                                    "fontSize": "12px",
                                                    "fontWeight": "bold",
                                                },
                                            ),
                                        ],
                                        style={"marginBottom": "10px"},
                                    ),
                                    html.P(
                                        "Visualisez les proportions et hiérarchies des données",
                                        style={
                                            "color": "#7f8c8d",
                                            "fontSize": "13px",
                                            "marginBottom": "10px",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Type de graphique:", className="dropdown-label"
                                            ),
                                            dcc.Dropdown(
                                                id="graph-type-2",
                                                options=[  # type: ignore
                                                    {
                                                        "label": "🥧 Pie Chart - Proportions par catégorie",
                                                        "value": "pie",
                                                    },
                                                    {
                                                        "label": "🗺️ TreeMap - Hiérarchie détaillée",
                                                        "value": "treemap",
                                                    },
                                                ],
                                                value="pie",
                                                clearable=False,
                                                className="custom-dropdown",
                                            ),
                                        ],
                                        className="dropdown-container",
                                        style={"marginTop": "10px"},
                                    ),
                                    dcc.Graph(
                                        id="exploration-graph-2",
                                        config=PLOTLY_CONFIG,  # type: ignore
                                    ),
                                ],
                                className="card graph-container",
                            )
                        ],
                        className="col",
                    ),
                ],
                className="row",
            ),
            # Section du tableau de données
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Aperçu des données", className="card-title"),
                            html.P(f"Affichage des {min(10, len(data))} premières lignes"),
                            html.Div(
                                [
                                    DataTable(
                                        data=data.head(10).to_dict("records"),  # type: ignore
                                        columns=[{"name": col, "id": col} for col in data.columns],
                                        style_table={
                                            "overflowX": "auto",
                                            "maxWidth": "100%",
                                        },
                                        style_header={
                                            "backgroundColor": "#2c3e50",
                                            "color": "white",
                                            "fontWeight": "bold",
                                            "textAlign": "left",
                                            "padding": "8px 10px",
                                            "border": "none",
                                            "fontSize": "0.85rem",
                                            "whiteSpace": "normal",
                                            "height": "auto",
                                            "minWidth": "80px",
                                            "maxWidth": "180px",
                                        },
                                        style_cell={
                                            "textAlign": "left",
                                            "padding": "8px 10px",
                                            "border": "1px solid #bdc3c7",
                                            "fontFamily": "inherit",
                                            "fontSize": "0.8rem",
                                            "overflow": "hidden",
                                            "textOverflow": "ellipsis",
                                            "minWidth": "80px",
                                            "maxWidth": "180px",
                                        },
                                        style_data={
                                            "color": "#2c3e50",
                                            "backgroundColor": "white",
                                            "whiteSpace": "normal",
                                            "height": "auto",
                                        },
                                        style_data_conditional=[  # type: ignore
                                            {
                                                "if": {"row_index": "odd"},
                                                "backgroundColor": "#f8f9fa",
                                            },
                                            {
                                                "if": {"state": "active"},
                                                "backgroundColor": "#ecf0f1",
                                            },
                                        ],
                                        tooltip_data=[  # type: ignore
                                            {
                                                column: {"value": str(value), "type": "markdown"}
                                                for column, value in row.items()
                                            }
                                            for row in data.head(10).to_dict("records")
                                        ],
                                        tooltip_duration=None,
                                    )
                                ],
                                className="table-container",
                            ),
                        ],
                        className="card",
                    )
                ],
                className="row",
            ),
        ],
        className="home-page",
    )


def register_callbacks(app, data: pd.DataFrame) -> None:
    """Enregistre tous les callbacks pour les graphiques hybrides (fixes + dynamiques)."""

    # Callback pour stocker les filtres validés lors du clic sur le bouton
    @app.callback(
        Output("validated-filters", "data"),
        [Input("apply-filters-button", "n_clicks")],
        [
            Input("global-group-filter", "value"),
            Input("global-year-filter", "value"),
            Input("global-country-filter", "value"),
            Input("global-antigen-filter", "value"),
            Input("global-category-filter", "value"),
        ],
    )
    def store_validated_filters(
        n_clicks: int,
        group_filter: str,
        year_filter: str,
        country_filter: str,
        antigen_filter: str,
        category_filter: str,
    ):
        """Stocke les valeurs des filtres quand le bouton est cliqué."""
        if n_clicks == 0:
            # Initialisation avec les valeurs par défaut
            return {
                "group": "all",
                "year": "all",
                "country": "all",
                "antigen": "all",
                "category": "all",
            }

        return {
            "group": group_filter,
            "year": year_filter,
            "country": country_filter,
            "antigen": antigen_filter,
            "category": category_filter,
        }

    # Callback pour mettre à jour les options du dropdown Pays/Régions
    @app.callback(
        [
            Output("global-country-filter", "options"),
            Output("global-country-filter", "value"),
        ],
        [Input("global-group-filter", "value")],
    )
    def update_country_options(group_filter: str):
        """Met à jour les options du dropdown pays/régions selon le groupe sélectionné."""
        from src.utils.get_data import get_available_countries, get_available_regions

        if group_filter == "COUNTRIES":
            countries = get_available_countries(data[data["GROUP"] == "COUNTRIES"])
            options = [{"label": "Tous les pays", "value": "all"}] + [
                {"label": country, "value": country} for country in countries
            ]
        elif group_filter == "WHO_REGIONS":
            regions = get_available_regions(data)
            options = [{"label": "Toutes les régions", "value": "all"}] + [
                {"label": region, "value": region} for region in regions
            ]
        else:
            # Affiche tous (pays + régions)
            all_names = sorted(data["NAME"].dropna().unique().tolist())
            options = [{"label": "Tous", "value": "all"}] + [
                {"label": name, "value": name} for name in all_names
            ]

        return options, "all"

    # Callback pour les Statistiques Globales (filtrées par année uniquement)
    @app.callback(
        [
            Output("stat-countries", "children"),
            Output("stat-years", "children"),
            Output("stat-coverage", "children"),
        ],
        [Input("validated-filters", "data")],
    )
    def update_stats(validated_filters: dict):
        """Met à jour les statistiques globales selon le filtre année validé."""
        year_filter = validated_filters.get("year", "all")
        
        # Filtrer uniquement par année
        filtered_data = data if year_filter == "all" else data[data["YEAR"] == int(year_filter)]

        # Calculer les stats
        stats = create_statistics_cards(filtered_data)

        return (f"{stats['n_countries']}", f"{stats['n_years']}", f"{stats['avg_coverage']:.1f}%")

    # Callback pour la carte de vaccination
    @app.callback(
        Output("vaccination-map", "figure"),
        [Input("validated-filters", "data")],
    )
    def update_vaccination_map(validated_filters: dict) -> go.Figure:
        """Met à jour la carte de vaccination selon les filtres validés."""
        group_filter = validated_filters.get("group", "all")
        year_filter = validated_filters.get("year", "all")
        country_filter = validated_filters.get("country", "all")
        antigen_filter = validated_filters.get("antigen", "all")
        category_filter = validated_filters.get("category", "all")
        
        filtered_data = get_filtered_data(
            data=data,
            group=group_filter if group_filter != "all" else None,
            year=int(year_filter) if year_filter != "all" else None,
            country=country_filter if country_filter != "all" else None,
            antigen=antigen_filter if antigen_filter != "all" else None,
            coverage_category=category_filter if category_filter != "all" else None,
        )

        if filtered_data.empty:
            return go.Figure().add_annotation(
                text="Aucune donnée disponible pour la carte avec ces filtres",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font={"size": 16},
            )

        return create_vaccination_map(filtered_data)

    # Callback pour le graphique des pays par couverture
    @app.callback(
        Output("country-details-graph", "figure"),
        [Input("validated-filters", "data")],
    )
    def update_country_details(validated_filters: dict) -> go.Figure:
        """Met à jour le graphique des pays par couverture selon les filtres validés."""
        group_filter = validated_filters.get("group", "all")
        year_filter = validated_filters.get("year", "all")
        country_filter = validated_filters.get("country", "all")
        antigen_filter = validated_filters.get("antigen", "all")
        category_filter = validated_filters.get("category", "all")
        
        filtered_data = get_filtered_data(
            data=data,
            group=group_filter if group_filter != "all" else None,
            year=int(year_filter) if year_filter != "all" else None,
            country=country_filter if country_filter != "all" else None,
            antigen=antigen_filter if antigen_filter != "all" else None,
            coverage_category=category_filter if category_filter != "all" else None,
        )

        if filtered_data.empty:
            return go.Figure().add_annotation(
                text="Aucune donnée disponible",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        return create_country_details(filtered_data, top_n=10)

    # Callback pour l'évolution temporelle
    @app.callback(
        Output("timed-count-graph", "figure"),
        [Input("validated-filters", "data")],
    )
    def update_timed_count(validated_filters: dict) -> go.Figure:
        """Met à jour le graphique d'évolution temporelle selon les filtres validés."""
        group_filter = validated_filters.get("group", "all")
        year_filter = validated_filters.get("year", "all")
        country_filter = validated_filters.get("country", "all")
        antigen_filter = validated_filters.get("antigen", "all")
        category_filter = validated_filters.get("category", "all")
        
        filtered_data = get_filtered_data(
            data=data,
            group=group_filter if group_filter != "all" else None,
            year=int(year_filter) if year_filter != "all" else None,
            country=country_filter if country_filter != "all" else None,
            antigen=antigen_filter if antigen_filter != "all" else None,
            coverage_category=category_filter if category_filter != "all" else None,
        )

        if filtered_data.empty:
            return go.Figure().add_annotation(
                text="Aucune donnée disponible",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        return create_timed_count(filtered_data, time_column="YEAR", value_column="COVERAGE")

    # Callback pour le graphique d'exploration 1
    @app.callback(
        Output("exploration-graph-1", "figure"),
        [
            Input("graph-type-1", "value"),
            Input("validated-filters", "data"),
        ],
    )
    def update_exploration_1(graph_type: str, validated_filters: dict) -> go.Figure:
        """Met à jour le graphique d'exploration 1 (Distribution) selon les filtres validés."""
        group_filter = validated_filters.get("group", "all")
        year_filter = validated_filters.get("year", "all")
        country_filter = validated_filters.get("country", "all")
        antigen_filter = validated_filters.get("antigen", "all")
        category_filter = validated_filters.get("category", "all")
        
        filtered_data = get_filtered_data(
            data=data,
            group=group_filter if group_filter != "all" else None,
            year=int(year_filter) if year_filter != "all" else None,
            country=country_filter if country_filter != "all" else None,
            antigen=antigen_filter if antigen_filter != "all" else None,
            coverage_category=category_filter if category_filter != "all" else None,
        )

        if filtered_data.empty:
            return go.Figure().add_annotation(
                text="Aucune donnée disponible",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        if graph_type == "histogram":
            return create_statistics_histogram(filtered_data, column="COVERAGE", nbins=20)
        elif graph_type == "boxplot":
            return create_statistics_boxplot(
                filtered_data, column="COVERAGE", group_by="COVERAGE_CATEGORY"
            )
        else:
            return go.Figure().add_annotation(
                text="Type de graphique non reconnu",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

    # Callback pour le graphique d'exploration 2
    @app.callback(
        Output("exploration-graph-2", "figure"),
        [
            Input("graph-type-2", "value"),
            Input("validated-filters", "data"),
        ],
    )
    def update_exploration_2(graph_type: str, validated_filters: dict) -> go.Figure:
        """Met à jour le graphique d'exploration 2 (Composition) selon les filtres validés."""
        group_filter = validated_filters.get("group", "all")
        year_filter = validated_filters.get("year", "all")
        country_filter = validated_filters.get("country", "all")
        antigen_filter = validated_filters.get("antigen", "all")
        category_filter = validated_filters.get("category", "all")
        
        filtered_data = get_filtered_data(
            data=data,
            group=group_filter if group_filter != "all" else None,
            year=int(year_filter) if year_filter != "all" else None,
            country=country_filter if country_filter != "all" else None,
            antigen=antigen_filter if antigen_filter != "all" else None,
            coverage_category=category_filter if category_filter != "all" else None,
        )

        if filtered_data.empty:
            return go.Figure().add_annotation(
                text="Aucune donnée disponible",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        if graph_type == "pie":
            return create_pie_chart(filtered_data, column="COVERAGE_CATEGORY")
        elif graph_type == "treemap":
            return create_tree_map(filtered_data, path=["GROUP", "ANTIGEN"], values="COVERAGE")
        else:
            return go.Figure().add_annotation(
                text="Type de graphique non reconnu",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )
