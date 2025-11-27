from dash import html


def create_navbar():
    return html.Nav([
        html.Div([
            html.A("Doctors Dashboard", href="/", className='navbar-brand'),
            html.Ul([
                html.Li(html.A("Accueil", href="/", className='nav-link')),
            ], className='navbar-nav')
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'maxWidth': '1200px',
            'margin': '0 auto'
        })
    ], className='navbar')
