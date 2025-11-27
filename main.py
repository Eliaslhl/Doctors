import argparse
from dash import Dash, html
import pandas as pd
import numpy as np

from src.pages.home import create_home_layout
from src.components.navbar import create_navbar
from src.components.footer import create_footer
from src.components.header import create_sidebar


def load_sample_data():
    """
    Génère des données de vaccination simulées basées sur le format WHO.
    """
    np.random.seed(42)

    # Définition des paramètres (fausses données)
    countries = [
        ('ABW', 'Aruba'),
        ('AFG', 'Afghanistan'),
        ('AGO', 'Angola'),
        ('ALB', 'Albania'),
        ('AND', 'Andorra'),
        ('ARE', 'United Arab Emirates'),
        ('ARG', 'Argentina'),
        ('ARM', 'Armenia'),
        ('AUS', 'Australia'),
        ('AUT', 'Austria')
    ]
    
    years = [2020, 2021, 2022, 2023, 2024]
    
    antigens = [
        ('DIPHCV4', 'Diphtheria-containing vaccine, 4th dose (1st booster)'),
        ('DIPHCV5', 'Diphtheria-containing vaccine, 5th dose (2nd booster)'),
        ('DIPHCV6', 'Diphtheria-containing vaccine, 6th dose (3rd booster)'),
        ('HepB3', 'Hepatitis B vaccine, 3rd dose'),
        ('MCV1', 'Measles-containing vaccine, 1st dose'),
        ('MCV2', 'Measles-containing vaccine, 2nd dose'),
        ('POL3', 'Polio vaccine, 3rd dose')
    ]
    
    coverage_categories = [
        ('ADMIN', 'Administrative coverage'),
        ('OFFICIAL', 'Official coverage')
    ]
    
    # Génération des données (fausses données)
    data_rows = []
    
    for code, name in countries:
        for year in years:
            for antigen_code, antigen_desc in antigens:
                for cov_cat, cov_cat_desc in coverage_categories:
                    # Génération de la couverture vaccinale
                    coverage = round(np.random.uniform(70, 98), 2)
                    
                    # Pour ADMIN, on génère des valeurs TARGET_NUMBER et DOSES
                    if cov_cat == 'ADMIN':
                        target_number = np.random.randint(800, 2000)
                        doses = int(target_number * (coverage / 100))
                    else:
                        target_number = None
                        doses = None
                    
                    data_rows.append({
                        'GROUP': 'COUNTRIES',
                        'CODE': code,
                        'NAME': name,
                        'YEAR': year,
                        'ANTIGEN': antigen_code,
                        'ANTIGEN_DESCRIPTION': antigen_desc,
                        'COVERAGE_CATEGORY': cov_cat,
                        'COVERAGE_CATEGORY_DESCRIPTION': cov_cat_desc,
                        'TARGET_NUMBER': target_number,
                        'DOSES': doses,
                        'COVERAGE': coverage
                    })
    
    data = pd.DataFrame(data_rows)
    return data


def parse_arguments():
    """Parse les arguments en ligne de commande."""
    parser = argparse.ArgumentParser(description='Application Dash - Doctors')
    parser.add_argument('--port', type=int, default=8050,
                        help='Port du serveur (défaut: 8050)')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Hôte du serveur (défaut: 127.0.0.1)')
    parser.add_argument('--debug', action='store_true',
                        help='Active le mode debug')
    parser.add_argument('--no-reload', dest='use_reloader', action='store_false',
                        help='Désactive le rechargement automatique')
    parser.set_defaults(use_reloader=True)
    
    return parser.parse_args()


def create_dashboard_layout(app, data):
    """
    Crée le layout principal du dashboard avec sidebar à gauche.
    """
    return html.Div([
        # Sidebar à gauche
        create_sidebar(data),
        
        # Contenu principal
        html.Div([
            create_navbar(),
            
            html.Div([
                create_home_layout(data)
            ], className='container'),
            
            create_footer()
        ], className='main-content')
        
    ], className='app-container')


def init_callbacks(app, data):
    """
    Initialise tous les callbacks de l'application.
    """
    from src.pages.home import register_callbacks as register_home_callbacks
    from src.components.sidebar_callbacks import register_sidebar_callbacks
    
    register_home_callbacks(app, data)
    register_sidebar_callbacks(app, data)
    
    print("✓ Callbacks initialisés avec succès")


def main() -> None:
    """Main function to launch the dashboard."""
    # Parse
    args = parse_arguments()
    
    print("=" * 60)
    print("Démarrage de l'application Dash - Doctors")
    print("=" * 60)
    
    # Charge les données
    print("Chargement des données...")
    data = load_sample_data()
    print(f"✓ {len(data)} enregistrements chargés")
    
    # Initialise l'application Dash
    print("Initialisation de l'application Dash...")
    app = Dash(
        __name__,
        suppress_callback_exceptions=True,
        title='Doctors Dashboard',
        update_title='Chargement...'
    )
    
    # Crée le layout
    print("📐 Création du layout...")
    app.layout = create_dashboard_layout(app, data)
    print("✓ Layout créé")
    
    # Initialise les callbacks
    print("\n🔗 Initialisation des callbacks...")
    init_callbacks(app, data)
    
    # Lance le serveur
    print("\n" + "=" * 60)
    print(f"🌐 Serveur démarré sur http://{args.host}:{args.port}")
    print(f"🐛 Mode debug: {'activé' if args.debug else 'désactivé'}")
    print(f"🔄 Rechargement auto: {'activé' if args.use_reloader else 'désactivé'}")
    print("=" * 60)
    print("\nAppuyez sur CTRL+C pour arrêter le serveur\n")
    
    app.run(
        debug=args.debug,
        host=args.host,
        port=args.port,
        use_reloader=args.use_reloader
    )


if __name__ == "__main__":
    main()
