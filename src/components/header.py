from typing import List
from dash import html, dcc
import pandas as pd


def create_sidebar(data: pd.DataFrame) -> html.Div:
    # Extraire les années disponibles
    years: List[int] = sorted(data['YEAR'].unique().tolist()) if 'YEAR' in data.columns else []
    countries: List[str] = sorted(data['NAME'].unique().tolist()) if 'NAME' in data.columns else []
    antigens: List[str] = sorted(data['ANTIGEN'].unique().tolist()) if 'ANTIGEN' in data.columns else []
    
    return html.Div([
        # Logo/Titre
        html.Div([
            html.H2("🏥 Vaccination", className='sidebar-title'),
            html.P("Dashboard", className='sidebar-subtitle')
        ], className='sidebar-header'),
        
        html.Hr(className='sidebar-divider'),
        
        # Filtres globaux
        html.Div([
            html.H3("Filtres", className='filter-section-title'),
            
            # Filtre par année
            html.Div([
                html.Label("Année", className='filter-label'),
                dcc.Dropdown(
                    id='global-year-filter',
                    options=[
                        {'label': 'Toutes les années', 'value': 'all'}
                    ] + [
                        {'label': str(year), 'value': year} for year in years
                    ],
                    value='all',
                    clearable=False,
                    className='filter-dropdown'
                )
            ], className='filter-group'),
            
            # Filtre par pays
            html.Div([
                html.Label("Pays", className='filter-label'),
                dcc.Dropdown(
                    id='global-country-filter',
                    options=[
                        {'label': 'Tous les pays', 'value': 'all'}
                    ] + [
                        {'label': country, 'value': country} 
                        for country in countries
                    ],
                    value='all',
                    clearable=False,
                    className='filter-dropdown'
                )
            ], className='filter-group'),
            
            # Filtre par antigène
            html.Div([
                html.Label("Antigène", className='filter-label'),
                dcc.Dropdown(
                    id='global-antigen-filter',
                    options=[
                        {'label': 'Tous les antigènes', 'value': 'all'}
                    ] + [
                        {'label': antigen, 'value': antigen} 
                        for antigen in antigens
                    ],
                    value='all',
                    clearable=False,
                    className='filter-dropdown'
                )
            ], className='filter-group'),
            
        ], className='filters-container'),
        
        # Statistiques rapides
        html.Div([
            html.Hr(className='sidebar-divider'),
            html.H3("Statistiques", className='filter-section-title'),
            html.Div(id='sidebar-stats', className='sidebar-stats')
        ], className='sidebar-footer')
        
    ], className='sidebar')
