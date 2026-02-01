import pandas as pd
from dash import dcc, html

from src.utils.get_data import (
    get_available_antigens,
    get_available_countries,
    get_available_coverage_categories,
    get_available_years,
)


def create_sidebar(data: pd.DataFrame) -> html.Div:
    # Extrait les années disponibles
    years: list[int] = get_available_years(data)

    # Extrait les pays disponibles
    countries: list[str] = get_available_countries(data)

    # Extrait les antigènes disponibles
    antigens: list[str] = get_available_antigens(data)

    # Extrait les catégories de couverture disponibles
    coverage_categories: list[str] = get_available_coverage_categories(data)

    return html.Div(
        [
            # Logo/Titre
            html.Div(
                [
                    html.H2("🏥 Vaccination", className="sidebar-title"),
                    html.P("Dashboard", className="sidebar-subtitle"),
                ],
                className="sidebar-header",
            ),
            html.Hr(className="sidebar-divider"),
            # Filtres globaux
            html.Div(
                [
                    html.H3("Filtres", className="filter-section-title"),
                    # Filtre par groupe (Pays/Régions)
                    html.Div(
                        [
                            html.Label("Vue", className="filter-label"),
                            dcc.Dropdown(
                                id="global-group-filter",
                                options=[  # type: ignore
                                    {"label": "Tous", "value": "all"},
                                    {"label": "Pays uniquement", "value": "COUNTRIES"},
                                    {"label": "Régions WHO uniquement", "value": "WHO_REGIONS"},
                                ],
                                value="all",
                                clearable=False,
                                className="filter-dropdown",
                            ),
                        ],
                        className="filter-group",
                    ),
                    # Filtre par année
                    html.Div(
                        [
                            html.Label("Année", className="filter-label"),
                            dcc.Dropdown(
                                id="global-year-filter",
                                options=[  # type: ignore
                                    {"label": "Toutes les années", "value": "all"}
                                ]
                                + [{"label": str(year), "value": year} for year in years],
                                value="all",
                                clearable=False,
                                className="filter-dropdown",
                            ),
                        ],
                        className="filter-group",
                    ),
                    # Filtre par pays
                    html.Div(
                        [
                            html.Label("Pays", className="filter-label"),
                            dcc.Dropdown(
                                id="global-country-filter",
                                options=[  # type: ignore
                                    {"label": "Tous les pays", "value": "all"}
                                ]
                                + [{"label": country, "value": country} for country in countries],
                                value="all",
                                clearable=False,
                                className="filter-dropdown",
                            ),
                        ],
                        className="filter-group",
                    ),
                    # Filtre par antigène
                    html.Div(
                        [
                            html.Label("Antigène", className="filter-label"),
                            dcc.Dropdown(
                                id="global-antigen-filter",
                                options=[  # type: ignore
                                    {"label": "Tous les antigènes", "value": "all"}
                                ]
                                + [{"label": antigen, "value": antigen} for antigen in antigens],
                                value="all",
                                clearable=False,
                                className="filter-dropdown",
                            ),
                        ],
                        className="filter-group",
                    ),
                    # Filtre par type de données
                    html.Div(
                        [
                            html.Label("Type de données", className="filter-label"),
                            dcc.Dropdown(
                                id="global-category-filter",
                                options=[  # type: ignore
                                    {"label": "Toutes les catégories", "value": "all"}
                                ]
                                + [
                                    {"label": f"{cat}", "value": cat} for cat in coverage_categories
                                ],
                                value="all",
                                clearable=False,
                                className="filter-dropdown",
                            ),
                        ],
                        className="filter-group",
                    ),
                    # Bouton pour appliquer les filtres
                    html.Div(
                        [
                            html.Button(
                                "🔍 Appliquer les filtres",
                                id="apply-filters-button",
                                n_clicks=0,
                                className="apply-filters-btn",
                                style={
                                    "width": "100%",
                                    "padding": "12px 20px",
                                    "backgroundColor": "#27ae60",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "fontSize": "14px",
                                    "fontWeight": "bold",
                                    "cursor": "pointer",
                                    "marginTop": "20px",
                                    "transition": "all 0.3s ease",
                                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                                },
                            ),
                        ],
                        className="filter-group",
                    ),
                ],
                className="filters-container",
            ),
            # Store pour conserver les filtres validés
            dcc.Store(id="validated-filters", data={}),
            # Statistiques rapides
            html.Div(
                [
                    html.Hr(className="sidebar-divider"),
                    html.H3("Statistiques", className="filter-section-title"),
                    html.Div(id="sidebar-stats", className="sidebar-stats"),
                ],
                className="sidebar-footer",
            ),
        ],
        className="sidebar",
    )
