from dash import html, dcc


def create_sidebar(data):
    """
    Crée une sidebar à gauche avec filtres globaux.
    """
    # Extraire les années disponibles
    years = sorted(data['YEAR'].unique()) if 'YEAR' in data.columns else []
    
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
                        for country in sorted(data['NAME'].unique()) if 'NAME' in data.columns
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
                        for antigen in sorted(data['ANTIGEN'].unique()) if 'ANTIGEN' in data.columns
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
