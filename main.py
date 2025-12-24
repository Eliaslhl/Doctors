import argparse
from typing import Dict, Any

import dash

from src.app.layout import create_main_layout
from src.callbacks.callbacks import register_all_callbacks
from src.utils.get_data import get_vaccination_data


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Vaccination Coverage Dashboard - Application Dash'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8050,
        help='Port du serveur (défaut: 8050)'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Hôte du serveur (défaut: 127.0.0.1)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Active le mode debug'
    )
    parser.add_argument(
        '--no-reload',
        dest='use_reloader',
        action='store_false',
        help='Désactive le rechargement automatique'
    )
    parser.set_defaults(use_reloader=True)
    
    return parser.parse_args()


def print_startup_info(host: str, port: int, debug: bool, use_reloader: bool, n_records: int) -> None:
    """
    Affiche les informations de démarrage.
    
    Args:
        host: Adresse de l'hôte
        port: Port du serveur
        debug: Mode debug activé ou non
        use_reloader: Rechargement automatique activé ou non
        n_records: Nombre d'enregistrements chargés
    """
    print("\n" + "=" * 60)
    print("🏥 Vaccination Coverage Dashboard")
    print("=" * 60)
    print(f"📊 {n_records} enregistrements chargés")
    print(f"🌐 Serveur: http://{host}:{port}")
    print(f"🐛 Mode debug: {'activé' if debug else 'désactivé'}")
    print(f"🔄 Rechargement auto: {'activé' if use_reloader else 'désactivé'}")
    print("=" * 60)
    print("\nAppuyez sur CTRL+C pour arrêter le serveur\n")


def initialize_app(data) -> dash.Dash:
    """
    Initialize and configure the Dash application.
    
    Args:
        data: DataFrame contenant les données de vaccination
        
    Returns:
        A configured Dash application instance
    """
    # Initialize app
    app = dash.Dash(
        __name__,
        suppress_callback_exceptions=True,
        title='Vaccination Coverage Dashboard',
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1.0"
            }
        ]
    )
    
    # Set up layout
    app.layout = create_main_layout(data)
    
    # Initialize callbacks
    register_all_callbacks(app, data)
    
    return app


def main() -> None:
    """
    Fonction principale pour lancer le dashboard.
    """
    # On parse les arguments de la ligne de commande
    args = parse_arguments()
    
    # Chargement des données
    print("Chargement des données depuis le fichier CSV...")
    data = get_vaccination_data(use_cleaned=True)
    print(f"✓ {len(data)} enregistrements chargés")
    
    # Initialisation de l'application
    print("Création de l'application...")
    app = initialize_app(data)
    print("✓ Application créée et configurée")
    
    # Affichage des infos de démarrage
    print_startup_info(args.host, args.port, args.debug, args.use_reloader, len(data))

    # Démarrage du serveur
    app.run(
        debug=args.debug,
        host=args.host,
        port=args.port,
        use_reloader=args.use_reloader
    )


if __name__ == "__main__":
    main()
