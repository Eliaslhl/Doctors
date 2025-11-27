from dash import html, Output, Input


def register_sidebar_callbacks(app, data):
    """
    Enregistre les callbacks pour la sidebar (statistiques dynamiques).
    """
    
    @app.callback(
        Output('sidebar-stats', 'children'),
        [
            Input('global-year-filter', 'value'),
            Input('global-country-filter', 'value'),
            Input('global-antigen-filter', 'value')
        ]
    )
    def update_sidebar_stats(year, country, antigen):
        """Met à jour les statistiques de la sidebar en fonction des filtres."""
        
        # Filtrer les données
        filtered_data = data.copy()
        
        if year != 'all':
            filtered_data = filtered_data[filtered_data['YEAR'] == year]
        
        if country != 'all':
            filtered_data = filtered_data[filtered_data['NAME'] == country]
        
        if antigen != 'all':
            filtered_data = filtered_data[filtered_data['ANTIGEN'] == antigen]
        
        # Calculer les statistiques
        n_records = len(filtered_data)
        avg_coverage = filtered_data['COVERAGE'].mean() if len(filtered_data) > 0 else 0
        n_countries = filtered_data['NAME'].nunique() if len(filtered_data) > 0 else 0
        
        return html.Div([
            html.Div([
                html.Strong("Enregistrements: "),
                html.Span(f"{n_records:,}")
            ], style={'marginBottom': '8px'}),
            html.Div([
                html.Strong("Pays: "),
                html.Span(f"{n_countries}")
            ], style={'marginBottom': '8px'}),
            html.Div([
                html.Strong("Couverture moy.: "),
                html.Span(f"{avg_coverage:.1f}%")
            ])
        ])
