from typing import List
from dash import html, dcc
import pandas as pd


def create_sidebar(data: pd.DataFrame) -> html.Div:
    # Extraire les années disponibles (en gérant les NaN)
    years: List[int] = []
    if 'YEAR' in data.columns:
        years = sorted([int(y) for y in data['YEAR'].dropna().unique()])
    
    countries: List[str] = []
    if 'NAME' in data.columns:
        countries = sorted([str(c) for c in data['NAME'].dropna().unique()])
    
    antigens: List[str] = []
    if 'ANTIGEN' in data.columns:
        antigens = sorted([str(a) for a in data['ANTIGEN'].dropna().unique()])
    
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
