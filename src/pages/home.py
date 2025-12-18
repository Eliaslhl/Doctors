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
        
        # Section des graphiques
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Visualisation 1", className='card-title'),
                    html.Div([
                        html.Label("Sélectionner une colonne:", className='dropdown-label'),
                        dcc.Dropdown(
                            id='column-dropdown-1',
                            options=[{'label': col, 'value': col} for col in data.columns],
                            value=data.columns[0] if len(data.columns) > 0 else None,
                            clearable=False
                        ),
                    ], className='dropdown-container'),
                    dcc.Graph(
                        id='graph-1',
                        config=PLOTLY_CONFIG  # type: ignore
                    )
                ], className='card graph-container')
            ], className='col'),
            
            html.Div([
                html.Div([
                    html.H3("Visualisation 2", className='card-title'),
                    html.Div([
                        html.Label("Sélectionner une colonne:", className='dropdown-label'),
                        dcc.Dropdown(
                            id='column-dropdown-2',
                            options=[{'label': col, 'value': col} for col in data.columns],
                            value=data.columns[1] if len(data.columns) > 1 else data.columns[0],
                            clearable=False
                        ),
                    ], className='dropdown-container'),
                    dcc.Graph(
                        id='graph-2',
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
    """
    Enregistre les callbacks pour la page d'accueil.
    Tous les graphiques utilisent le module src/graphics/.
    """
    
    @app.callback(
        Output('graph-1', 'figure'),
        [
            Input('column-dropdown-1', 'value'),
            Input('global-year-filter', 'value'),
            Input('global-country-filter', 'value'),
            Input('global-antigen-filter', 'value'),
            Input('global-category-filter', 'value')
        ]
    )
    def update_graph_1(
        selected_column: str,
        year_filter: str,
        country_filter: str,
        antigen_filter: str,
        category_filter: str
    ) -> go.Figure:
        """Mise à jour du graphique 1 avec filtres globaux."""
        if selected_column is None or selected_column not in data.columns:
            return go.Figure()
        
        # Applique les filtres globaux via get_filtered_data
        filtered_data = get_filtered_data(
            data=data,
            year=int(year_filter) if year_filter != 'all' else None,
            country=country_filter if country_filter != 'all' else None,
            antigen=antigen_filter if antigen_filter != 'all' else None,
            coverage_category=category_filter if category_filter != 'all' else None
        )
        
        if filtered_data.empty:
            return go.Figure()
        
        if selected_column == 'COVERAGE':
            return create_statistics_histogram(filtered_data, column='COVERAGE', nbins=30)
        elif selected_column == 'YEAR':
            return create_timed_count(filtered_data, time_column='YEAR', value_column='COVERAGE')
        elif selected_column == 'NAME':
            return create_country_details(filtered_data, top_n=10)
        elif selected_column == 'ANTIGEN':
            return create_tree_map(filtered_data, path=['ANTIGEN'], values='COVERAGE')
        elif selected_column in ['COVERAGE_CATEGORY', 'GROUP']:
            return create_pie_chart(filtered_data, column=selected_column)
        else:
            if filtered_data[selected_column].dtype in ['int64', 'float64']:
                return create_statistics_histogram(filtered_data, column=selected_column)
            else:
                return create_pie_chart(filtered_data, column=selected_column, max_categories=10)
    
    @app.callback(
        Output('graph-2', 'figure'),
        [
            Input('column-dropdown-2', 'value'),
            Input('global-year-filter', 'value'),
            Input('global-country-filter', 'value'),
            Input('global-antigen-filter', 'value'),
            Input('global-category-filter', 'value')
        ]
    )
    def update_graph_2(
        selected_column: str,
        year_filter: str,
        country_filter: str,
        antigen_filter: str,
        category_filter: str
    ) -> go.Figure:
        """Mise à jour du graphique 2 avec filtres globaux."""
        if selected_column is None or selected_column not in data.columns:
            return go.Figure()
        
        # Applique les filtres globaux via get_filtered_data
        filtered_data = get_filtered_data(
            data=data,
            year=int(year_filter) if year_filter != 'all' else None,
            country=country_filter if country_filter != 'all' else None,
            antigen=antigen_filter if antigen_filter != 'all' else None,
            coverage_category=category_filter if category_filter != 'all' else None
        )
        
        if filtered_data.empty:
            return go.Figure()
        
        # Génère le graphique
        if selected_column == 'COVERAGE':
            return create_statistics_boxplot(filtered_data, column='COVERAGE', group_by='COVERAGE_CATEGORY')
        elif selected_column == 'YEAR':
            return create_timed_count(filtered_data, time_column='YEAR', value_column='COVERAGE', group_by='GROUP')
        elif selected_column == 'NAME':
            return create_country_details(filtered_data, top_n=15)
        elif selected_column == 'ANTIGEN':
            return create_tree_map(filtered_data, path=['GROUP', 'ANTIGEN'], values='COVERAGE')
        elif selected_column in ['COVERAGE_CATEGORY', 'GROUP']:
            return create_pie_chart(filtered_data, column=selected_column)
        else:
            if filtered_data[selected_column].dtype in ['int64', 'float64']:
                return create_statistics_boxplot(filtered_data, column=selected_column)
            else:
                return create_pie_chart(filtered_data, column=selected_column, max_categories=8)
