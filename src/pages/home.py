from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from config import PLOTLY_CONFIG, PLOTLY_TEMPLATE, COLOR_PALETTE


def create_home_layout(data):
    # Calcul de statistiques spécifiques aux données de vaccination
    n_countries = data['NAME'].nunique() if 'NAME' in data.columns else 0
    n_years = data['YEAR'].nunique() if 'YEAR' in data.columns else 0
    avg_coverage = data['COVERAGE'].mean() if 'COVERAGE' in data.columns else 0
    
    return html.Div([
        html.H1("Dashboard - Vaccination Coverage", className='page-title'),
        html.Hr(),
        
        # Section des statistiques principales
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Pays", className='stat-title'),
                    html.H2(f"{n_countries}", className='stat-value')
                ], className='card stat-card')
            ], className='col'),
            
            html.Div([
                html.Div([
                    html.H3("Années", className='stat-title'),
                    html.H2(f"{n_years}", className='stat-value')
                ], className='card stat-card')
            ], className='col'),
            
            html.Div([
                html.Div([
                    html.H3("Couverture moyenne", className='stat-title'),
                    html.H2(f"{avg_coverage:.1f}%", className='stat-value')
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


def register_callbacks(app, data):
    @app.callback(
        Output('graph-1', 'figure'),
        Input('column-dropdown-1', 'value')
    )
    def update_graph_1(selected_column):
        """Met à jour le premier graphique en fonction de la colonne sélectionnée."""
        if selected_column is None or selected_column not in data.columns:
            return go.Figure()
        
        # Graphiques spécifiques pour les données de vaccination
        if selected_column == 'COVERAGE':
            # Distribution de la couverture vaccinale
            fig = px.histogram(
                data,
                x=selected_column,
                title='Distribution de la couverture vaccinale (%)',
                template=PLOTLY_TEMPLATE,
                color_discrete_sequence=COLOR_PALETTE,
                nbins=30
            )
            fig.update_layout(
                xaxis_title='Couverture (%)',
                yaxis_title='Nombre d\'enregistrements',
                hovermode='x unified'
            )
        elif selected_column == 'YEAR':
            # Évolution par année
            year_data = data.groupby('YEAR')['COVERAGE'].mean().reset_index()
            fig = px.line(
                year_data,
                x='YEAR',
                y='COVERAGE',
                title='Couverture vaccinale moyenne par année',
                template=PLOTLY_TEMPLATE,
                color_discrete_sequence=COLOR_PALETTE,
                markers=True
            )
            fig.update_layout(
                xaxis_title='Année',
                yaxis_title='Couverture moyenne (%)',
                hovermode='x unified'
            )
        elif selected_column in ['NAME', 'ANTIGEN', 'COVERAGE_CATEGORY']:
            # Top 10 des valeurs pour les colonnes catégorielles
            value_counts = data[selected_column].value_counts().head(10)
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f'Top 10 - {selected_column}',
                labels={'x': selected_column, 'y': 'Nombre'},
                template=PLOTLY_TEMPLATE,
                color_discrete_sequence=COLOR_PALETTE
            )
            fig.update_layout(
                xaxis_title=selected_column,
                yaxis_title='Nombre d\'enregistrements',
                hovermode='x unified'
            )
        else:
            # Graphique par défaut
            if data[selected_column].dtype in ['int64', 'float64']:
                fig = px.histogram(
                    data,
                    x=selected_column,
                    title=f'Distribution de {selected_column}',
                    template=PLOTLY_TEMPLATE,
                    color_discrete_sequence=COLOR_PALETTE
                )
            else:
                value_counts = data[selected_column].value_counts().head(10)
                fig = px.bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    title=f'Top 10 des valeurs de {selected_column}',
                    labels={'x': selected_column, 'y': 'Nombre'},
                    template=PLOTLY_TEMPLATE,
                    color_discrete_sequence=COLOR_PALETTE
                )
            fig.update_layout(
                xaxis_title=selected_column,
                yaxis_title='Fréquence',
                hovermode='x unified'
            )
        
        return fig
    
    @app.callback(
        Output('graph-2', 'figure'),
        Input('column-dropdown-2', 'value')
    )
    def update_graph_2(selected_column):
        """Met à jour le deuxième graphique en fonction de la colonne sélectionnée."""
        if selected_column is None or selected_column not in data.columns:
            return go.Figure()
        
        # Graphiques spécifiques pour les données de vaccination
        if selected_column == 'COVERAGE':
            # Box plot de la couverture par catégorie
            fig = px.box(
                data,
                x='COVERAGE_CATEGORY',
                y='COVERAGE',
                title='Distribution de la couverture par catégorie',
                template=PLOTLY_TEMPLATE,
                color='COVERAGE_CATEGORY',
                color_discrete_sequence=COLOR_PALETTE
            )
            fig.update_layout(
                xaxis_title='Catégorie de couverture',
                yaxis_title='Couverture (%)',
                showlegend=False
            )
        elif selected_column == 'ANTIGEN':
            # Couverture moyenne par antigène
            antigen_data = data.groupby('ANTIGEN')['COVERAGE'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=antigen_data.index,
                y=antigen_data.values,
                title='Couverture moyenne par antigène (Top 10)',
                labels={'x': 'Antigène', 'y': 'Couverture moyenne (%)'},
                template=PLOTLY_TEMPLATE,
                color_discrete_sequence=COLOR_PALETTE
            )
            fig.update_layout(
                xaxis_title='Antigène',
                yaxis_title='Couverture moyenne (%)'
            )
        elif selected_column == 'NAME':
            # Top 10 pays par couverture moyenne
            country_data = data.groupby('NAME')['COVERAGE'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=country_data.values,
                y=country_data.index,
                orientation='h',
                title='Top 10 pays - Couverture moyenne',
                labels={'x': 'Couverture moyenne (%)', 'y': 'Pays'},
                template=PLOTLY_TEMPLATE,
                color_discrete_sequence=COLOR_PALETTE
            )
        elif selected_column in ['COVERAGE_CATEGORY', 'GROUP']:
            # Graphique en camembert
            value_counts = data[selected_column].value_counts()
            fig = px.pie(
                values=value_counts.values,
                names=value_counts.index,
                title=f'Répartition - {selected_column}',
                template=PLOTLY_TEMPLATE,
                color_discrete_sequence=COLOR_PALETTE
            )
        else:
            # Graphique par défaut
            if data[selected_column].dtype in ['int64', 'float64']:
                fig = px.box(
                    data,
                    y=selected_column,
                    title=f'Statistiques de {selected_column}',
                    template=PLOTLY_TEMPLATE,
                    color_discrete_sequence=COLOR_PALETTE
                )
            else:
                value_counts = data[selected_column].value_counts().head(8)
                fig = px.pie(
                    values=value_counts.values,
                    names=value_counts.index,
                    title=f'Répartition de {selected_column}',
                    template=PLOTLY_TEMPLATE,
                    color_discrete_sequence=COLOR_PALETTE
                )
        
        return fig
