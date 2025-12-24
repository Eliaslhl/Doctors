from dash import html, dcc, Input, Output
from dash.dash_table import DataTable
import pandas as pd
import plotly.graph_objects as go

from config import PLOTLY_CONFIG
from src.utils.get_data import get_filtered_data
from src.graphics import (
    create_country_details,
    create_pie_chart,
    create_statistics_histogram,
    create_statistics_boxplot,
    create_statistics_cards,
    create_timed_count,
    create_tree_map
)


def create_home_layout(data: pd.DataFrame) -> html.Div:
    """
    Crée le layout de la page d'accueil.
    
    Args:
        data: DataFrame contenant les données de vaccination
        
    Returns:
        Layout Dash de la page d'accueil
    """
    # Calcul de statistiques via le module graphics
    stats = create_statistics_cards(data)
    
    return html.Div([
        html.H1("Dashboard - Vaccination Coverage", className='page-title'),
        html.Hr(),
        
        # Section des statistiques principales
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Pays", className='stat-title'),
                    html.H2(f"{stats['n_countries']}", className='stat-value')
                ], className='card stat-card')
            ], className='col'),
            
            html.Div([
                html.Div([
                    html.H3("Années", className='stat-title'),
                    html.H2(f"{stats['n_years']}", className='stat-value')
                ], className='card stat-card')
            ], className='col'),
            
            html.Div([
                html.Div([
                    html.H3("Couverture moyenne", className='stat-title'),
                    html.H2(f"{stats['avg_coverage']:.1f}%", className='stat-value')
                ], className='card stat-card')
            ], className='col'),
        ], className='row stats-row'),
        
        # Pays par Couverture + Évolution Temporelle
        html.Div([
            # Pays par Couverture
            html.Div([
                html.Div([
                    html.H3("📊 Pays par Couverture Moyenne", className='card-title'),
                    dcc.Graph(
                        id='country-details-graph',
                        config=PLOTLY_CONFIG  # type: ignore
                    )
                ], className='card graph-container')
            ], className='col'),
            
            # Évolution Temporelle
            html.Div([
                html.Div([
                    html.H3("📈 Évolution de la Couverture dans le Temps", className='card-title'),
                    dcc.Graph(
                        id='timed-count-graph',
                        config=PLOTLY_CONFIG  # type: ignore
                    )
                ], className='card graph-container')
            ], className='col'),
        ], className='row'),
        
        # Graphiques d'Exploration
        html.Div([
            html.H3("🔍 Exploration des Données", className='section-title', 
                   style={'marginTop': '30px', 'marginBottom': '10px', 'color': '#2c3e50'}),
            html.P("Voici deux graphiques pour comparer différentes visualisations des mêmes données filtrées. "
                   "Parfait pour une analyse multi-angle ! 📊",
                   style={'color': '#7f8c8d', 'fontSize': '14px', 'marginBottom': '20px', 'fontStyle': 'italic'}),
        ], className='row'),
        
        # Graphique d'exploration 1 - Distribution
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("📊 Analyse de Distribution", className='card-title', style={'display': 'inline-block', 'marginRight': '10px'}),
                        html.Span("Première Vue", 
                                 style={'backgroundColor': '#3498db', 'color': 'white', 'padding': '4px 12px', 
                                        'borderRadius': '12px', 'fontSize': '12px', 'fontWeight': 'bold'})
                    ], style={'marginBottom': '10px'}),
                    html.P("Visualisez les distributions et quartiles des données", 
                          style={'color': '#7f8c8d', 'fontSize': '13px', 'marginBottom': '10px'}),
                    html.Div([
                        html.Label("Type de graphique:", className='dropdown-label'),
                        dcc.Dropdown(
                            id='graph-type-1',
                            options=[  # type: ignore
                                {'label': '📊 Histogram - Distribution des valeurs', 'value': 'histogram'},
                                {'label': '📦 Boxplot - Quartiles et outliers', 'value': 'boxplot'}
                            ],
                            value='histogram',
                            clearable=False,
                            className='custom-dropdown'
                        ),
                    ], className='dropdown-container', style={'marginTop': '10px'}),
                    dcc.Graph(
                        id='exploration-graph-1',
                        config=PLOTLY_CONFIG  # type: ignore
                    )
                ], className='card graph-container')
            ], className='col'),
            
            # Graphique d'exploration 2 - Composition
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("🗂️ Analyse de Composition", className='card-title', style={'display': 'inline-block', 'marginRight': '10px'}),
                        html.Span("Comparaison", 
                                 style={'backgroundColor': '#e74c3c', 'color': 'white', 'padding': '4px 12px', 
                                        'borderRadius': '12px', 'fontSize': '12px', 'fontWeight': 'bold'})
                    ], style={'marginBottom': '10px'}),
                    html.P("Visualisez les proportions et hiérarchies des données", 
                          style={'color': '#7f8c8d', 'fontSize': '13px', 'marginBottom': '10px'}),
                    html.Div([
                        html.Label("Type de graphique:", className='dropdown-label'),
                        dcc.Dropdown(
                            id='graph-type-2',
                            options=[  # type: ignore
                                {'label': '🥧 Pie Chart - Proportions par catégorie', 'value': 'pie'},
                                {'label': '🗺️ TreeMap - Hiérarchie détaillée', 'value': 'treemap'}
                            ],
                            value='pie',
                            clearable=False,
                            className='custom-dropdown'
                        ),
                    ], className='dropdown-container', style={'marginTop': '10px'}),
                    dcc.Graph(
                        id='exploration-graph-2',
                        config=PLOTLY_CONFIG  # type: ignore
                    )
                ], className='card graph-container')
            ], className='col'),
        ], className='row'),
        
        # Section du tableau de données
        html.Div([
            html.Div([
                html.H3("Aperçu des données", className='card-title'),
                html.P(f"Affichage des {min(10, len(data))} premières lignes"),
                html.Div([
                    DataTable(
                        data=data.head(10).to_dict('records'),  # type: ignore
                        columns=[{"name": col, "id": col} for col in data.columns],
                        style_table={
                            'overflowX': 'auto',
                            'maxWidth': '100%',
                        },
                        style_header={
                            'backgroundColor': '#2c3e50',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'left',
                            'padding': '8px 10px',
                            'border': 'none',
                            'fontSize': '0.85rem',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'minWidth': '80px',
                            'maxWidth': '180px',
                        },
                        style_cell={
                            'textAlign': 'left',
                            'padding': '8px 10px',
                            'border': '1px solid #bdc3c7',
                            'fontFamily': 'inherit',
                            'fontSize': '0.8rem',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'minWidth': '80px',
                            'maxWidth': '180px',
                        },
                        style_data={
                            'color': '#2c3e50',
                            'backgroundColor': 'white',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                        style_data_conditional=[  # type: ignore
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#f8f9fa',
                            },
                            {
                                'if': {'state': 'active'},
                                'backgroundColor': '#ecf0f1',
                            }
                        ],
                        tooltip_data=[  # type: ignore
                            {
                                column: {'value': str(value), 'type': 'markdown'}
                                for column, value in row.items()
                            } for row in data.head(10).to_dict('records')
                        ],
                        tooltip_duration=None,
                    )
                ], className='table-container')
            ], className='card')
        ], className='row'),
        
    ], className='home-page')


def register_callbacks(app, data: pd.DataFrame) -> None:
    """Enregistre tous les callbacks pour les graphiques hybrides (fixes + dynamiques)."""
    
    # callback - Pays par Couverture
    @app.callback(
        Output('country-details-graph', 'figure'),
        [
            Input('global-year-filter', 'value'),
            Input('global-country-filter', 'value'),
            Input('global-antigen-filter', 'value'),
            Input('global-category-filter', 'value')
        ]
    )
    def update_country_details(year_filter: str, country_filter: str, antigen_filter: str, category_filter: str) -> go.Figure:
        """Met à jour le graphique des pays par couverture (fixe)."""
        filtered_data = get_filtered_data(
            data=data,
            year=int(year_filter) if year_filter != 'all' else None,
            country=country_filter if country_filter != 'all' else None,
            antigen=antigen_filter if antigen_filter != 'all' else None,
            coverage_category=category_filter if category_filter != 'all' else None
        )
        
        if filtered_data.empty:
            return go.Figure().add_annotation(
                text="Aucune donnée disponible",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        return create_country_details(filtered_data, top_n=10)
    
    # Évolution Temporelle
    @app.callback(
        Output('timed-count-graph', 'figure'),
        [
            Input('global-year-filter', 'value'),
            Input('global-country-filter', 'value'),
            Input('global-antigen-filter', 'value'),
            Input('global-category-filter', 'value')
        ]
    )
    def update_timed_count(year_filter: str, country_filter: str, antigen_filter: str, category_filter: str) -> go.Figure:
        """Met à jour le graphique d'évolution temporelle (fixe)."""
        filtered_data = get_filtered_data(
            data=data,
            year=int(year_filter) if year_filter != 'all' else None,
            country=country_filter if country_filter != 'all' else None,
            antigen=antigen_filter if antigen_filter != 'all' else None,
            coverage_category=category_filter if category_filter != 'all' else None
        )
        
        if filtered_data.empty:
            return go.Figure().add_annotation(
                text="Aucune donnée disponible",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        return create_timed_count(filtered_data, time_column='YEAR', value_column='COVERAGE')
    
    # callback - Graphique d'Exploration 1
    @app.callback(
        Output('exploration-graph-1', 'figure'),
        [
            Input('graph-type-1', 'value'),
            Input('global-year-filter', 'value'),
            Input('global-country-filter', 'value'),
            Input('global-antigen-filter', 'value'),
            Input('global-category-filter', 'value')
        ]
    )
    def update_exploration_1(graph_type: str, year_filter: str, country_filter: str, antigen_filter: str, category_filter: str) -> go.Figure:
        """Met à jour le graphique d'exploration 1 (Distribution) selon le type sélectionné."""
        filtered_data = get_filtered_data(
            data=data,
            year=int(year_filter) if year_filter != 'all' else None,
            country=country_filter if country_filter != 'all' else None,
            antigen=antigen_filter if antigen_filter != 'all' else None,
            coverage_category=category_filter if category_filter != 'all' else None
        )
        
        if filtered_data.empty:
            return go.Figure().add_annotation(
                text="Aucune donnée disponible",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        # callback - Graphique 1 : Distribution uniquement (Histogram ou Boxplot)
        if graph_type == 'histogram':
            return create_statistics_histogram(filtered_data, column='COVERAGE', nbins=20)
        elif graph_type == 'boxplot':
            return create_statistics_boxplot(filtered_data, column='COVERAGE', group_by='COVERAGE_CATEGORY')
        else:
            return go.Figure().add_annotation(
                text="Type de graphique non reconnu",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    # callback - Graphique d'Exploration 2
    @app.callback(
        Output('exploration-graph-2', 'figure'),
        [
            Input('graph-type-2', 'value'),
            Input('global-year-filter', 'value'),
            Input('global-country-filter', 'value'),
            Input('global-antigen-filter', 'value'),
            Input('global-category-filter', 'value')
        ]
    )
    def update_exploration_2(graph_type: str, year_filter: str, country_filter: str, antigen_filter: str, category_filter: str) -> go.Figure:
        """Met à jour le graphique d'exploration 2 (Composition) selon le type sélectionné."""
        filtered_data = get_filtered_data(
            data=data,
            year=int(year_filter) if year_filter != 'all' else None,
            country=country_filter if country_filter != 'all' else None,
            antigen=antigen_filter if antigen_filter != 'all' else None,
            coverage_category=category_filter if category_filter != 'all' else None
        )
        
        if filtered_data.empty:
            return go.Figure().add_annotation(
                text="Aucune donnée disponible",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        # Graphique 2 : Composition uniquement (Pie Chart ou TreeMap)
        if graph_type == 'pie':
            return create_pie_chart(filtered_data, column='COVERAGE_CATEGORY')
        elif graph_type == 'treemap':
            return create_tree_map(filtered_data, path=['GROUP', 'ANTIGEN'], values='COVERAGE')
        else:
            return go.Figure().add_annotation(
                text="Type de graphique non reconnu",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
