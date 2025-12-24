from typing import List
from dash import html, dcc
import pandas as pd
from src.utils.get_data import (
    get_available_years,
    get_available_countries,
    get_available_antigens,
    get_available_coverage_categories
)


def create_sidebar(data: pd.DataFrame) -> html.Div:
    # Extrait les années disponibles
    years: List[int] = get_available_years(data)
    
    # Extrait les pays disponibles
    countries: List[str] = get_available_countries(data)
    
    # Extrait les antigènes disponibles
    antigens: List[str] = get_available_antigens(data)
    
    # Extrait les catégories de couverture disponibles
    coverage_categories: List[str] = get_available_coverage_categories(data)
    
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
                    options=[  # type: ignore
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
                    options=[  # type: ignore
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
                    options=[  # type: ignore
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
            
            # Filtre par type de données
            html.Div([
                html.Label("Type de données", className='filter-label'),
                dcc.Dropdown(
                    id='global-category-filter',
                    options=[  # type: ignore
                        {'label': 'Toutes les catégories', 'value': 'all'}
                    ] + [
                        {'label': f'{cat}', 'value': cat} 
                        for cat in coverage_categories
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
