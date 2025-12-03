from dash import html


def create_navbar() -> html.Nav:
    return html.Nav([
        html.Div([
            html.A("Doctors Dashboard", href="/", className='navbar-brand'),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'maxWidth': '1200px',
            'margin': '0 auto'
        })
    ], className='navbar')
