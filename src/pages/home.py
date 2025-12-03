from dash import html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go

from config import PLOTLY_CONFIG
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
                        config=PLOTLY_CONFIG
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
                        config=PLOTLY_CONFIG
                    )
                ], className='card graph-container')
            ], className='col'),
        ], className='row'),
        
        # Section du tableau de données
        html.Div([
            html.Div([
                html.H3("Aperçu des données", className='card-title'),
                html.Div([
                    html.P(f"Affichage des {min(10, len(data))} premières lignes"),
                    html.Div(
                        data.head(10).to_html(classes='data-table', index=False),
                        className='table-container'
                    )
                ], style={'overflowX': 'auto'})
            ], className='card')
        ], className='row'),
        
    ], className='home-page')


def register_callbacks(app, data: pd.DataFrame) -> None:
    """
    Enregistre les callbacks pour la page d'accueil.
    Tous les graphiques utilisent le module src/graphics/.
    
    Args:
        app: Application Dash
        data: DataFrame contenant les données de vaccination
    """
    
    @app.callback(
        Output('graph-1', 'figure'),
        Input('column-dropdown-1', 'value')
    )
    def update_graph_1(selected_column: str) -> go.Figure:
        """Mise à jour du graphique 1 en fonction de la colonne sélectionnée."""
        if selected_column is None or selected_column not in data.columns:
            return go.Figure()
        
        # Utilisation exclusive des fonctions du module graphics
        if selected_column == 'COVERAGE':
            return create_statistics_histogram(data, column='COVERAGE', nbins=30)
        
        elif selected_column == 'YEAR':
            return create_timed_count(data, time_column='YEAR', value_column='COVERAGE')
        
        elif selected_column == 'NAME':
            return create_country_details(data, top_n=10)
        
        elif selected_column == 'ANTIGEN':
            return create_tree_map(data, path=['ANTIGEN'], values='COVERAGE')
        
        elif selected_column in ['COVERAGE_CATEGORY', 'GROUP']:
            return create_pie_chart(data, column=selected_column)
        
        else:
            # Pour les autres colonnes, utiliser histogramme ou pie selon le type
            if data[selected_column].dtype in ['int64', 'float64']:
                return create_statistics_histogram(data, column=selected_column)
            else:
                return create_pie_chart(data, column=selected_column, max_categories=10)
    
    @app.callback(
        Output('graph-2', 'figure'),
        Input('column-dropdown-2', 'value')
    )
    def update_graph_2(selected_column: str) -> go.Figure:
        """Mise à jour du graphique 2 en fonction de la colonne sélectionnée."""
        if selected_column is None or selected_column not in data.columns:
            return go.Figure()
        
        # Utilisation exclusive des fonctions du module graphics
        if selected_column == 'COVERAGE':
            return create_statistics_boxplot(data, column='COVERAGE', group_by='COVERAGE_CATEGORY')
        
        elif selected_column == 'YEAR':
            # Graphique différent pour le graph-2 : comparaison annuelle
            return create_timed_count(data, time_column='YEAR', value_column='COVERAGE', group_by='GROUP')
        
        elif selected_column == 'NAME':
            return create_country_details(data, top_n=15)
        
        elif selected_column == 'ANTIGEN':
            return create_tree_map(data, path=['GROUP', 'ANTIGEN'], values='COVERAGE')
        
        elif selected_column in ['COVERAGE_CATEGORY', 'GROUP']:
            return create_pie_chart(data, column=selected_column)
        
        else:
            # Pour les autres colonnes, utiliser boxplot ou pie selon le type
            if data[selected_column].dtype in ['int64', 'float64']:
                return create_statistics_boxplot(data, column=selected_column)
            else:
                return create_pie_chart(data, column=selected_column, max_categories=8)
