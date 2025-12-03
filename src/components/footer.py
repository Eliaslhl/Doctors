from dash import html
from datetime import datetime


def create_footer() -> html.Footer:
    current_year: int = datetime.now().year
    
    return html.Footer([
        html.Div([
            html.P(f"© {current_year} Doctors Dashboard - Tous droits réservés"),
        ], style={'maxWidth': '1200px', 'margin': '0 auto'})
    ], className='footer')
