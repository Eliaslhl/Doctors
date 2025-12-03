from typing import List, Tuple
import pandas as pd
import numpy as np


def generate_sample_vaccination_data(seed: int = 42) -> pd.DataFrame:
    """
    Génère des données de vaccination simulées basées sur le format WHO.
    
    Args:
        seed: Graine pour la génération aléatoire (pour reproductibilité)
        
    Returns:
        DataFrame contenant les données de vaccination avec les colonnes:
        - GROUP: Groupe (COUNTRIES)
        - CODE: Code pays (ex: ABW, AFG)
        - NAME: Nom du pays
        - YEAR: Année (2020-2024)
        - ANTIGEN: Code de l'antigène
        - ANTIGEN_DESCRIPTION: Description de l'antigène
        - COVERAGE_CATEGORY: Catégorie de couverture (ADMIN/OFFICIAL)
        - COVERAGE_CATEGORY_DESCRIPTION: Description de la catégorie
        - TARGET_NUMBER: Nombre cible (ADMIN uniquement)
        - DOSES: Doses administrées (ADMIN uniquement)
        - COVERAGE: Taux de couverture en %
    """
    np.random.seed(seed)
    
    # Définition des paramètres
    countries: List[Tuple[str, str]] = [
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
    
    years: List[int] = [2020, 2021, 2022, 2023, 2024]
    
    antigens: List[Tuple[str, str]] = [
        ('DIPHCV4', 'Diphtheria-containing vaccine, 4th dose (1st booster)'),
        ('DIPHCV5', 'Diphtheria-containing vaccine, 5th dose (2nd booster)'),
        ('DIPHCV6', 'Diphtheria-containing vaccine, 6th dose (3rd booster)'),
        ('HepB3', 'Hepatitis B vaccine, 3rd dose'),
        ('MCV1', 'Measles-containing vaccine, 1st dose'),
        ('MCV2', 'Measles-containing vaccine, 2nd dose'),
        ('POL3', 'Polio vaccine, 3rd dose')
    ]
    
    coverage_categories: List[Tuple[str, str]] = [
        ('ADMIN', 'Administrative coverage'),
        ('OFFICIAL', 'Official coverage')
    ]
    
    # Génération des données
    data_rows: List[dict] = []
    
    for code, name in countries:
        for year in years:
            for antigen_code, antigen_desc in antigens:
                for cov_cat, cov_cat_desc in coverage_categories:
                    # Génération de la couverture vaccinale (entre 70% et 98%)
                    coverage: float = round(np.random.uniform(70, 98), 2)
                    
                    # Pour ADMIN, on génère des valeurs TARGET_NUMBER et DOSES
                    target_number: int | None
                    doses: int | None
                    
                    if cov_cat == 'ADMIN':
                        target_number = int(np.random.randint(800, 2000))
                        doses = int(target_number * (coverage / 100))
                    else:
                        # Pour OFFICIAL, ces champs restent vides
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
    
    return pd.DataFrame(data_rows)


def load_data_from_csv(filepath: str) -> pd.DataFrame:
    """
    Charge des données depuis un fichier CSV.
    
    Args:
        filepath: Chemin vers le fichier CSV
        
    Returns:
        DataFrame contenant les données chargées
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        pd.errors.EmptyDataError: Si le fichier est vide
    """
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {filepath} n'a pas été trouvé.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"Le fichier {filepath} est vide.")


def filter_data_by_year(data: pd.DataFrame, years: List[int]) -> pd.DataFrame:
    """
    Filtre les données par année(s).
    
    Args:
        data: DataFrame à filtrer
        years: Liste des années à conserver
        
    Returns:
        DataFrame filtré
    """
    if 'YEAR' not in data.columns:
        return data
    
    return data[data['YEAR'].isin(years)].copy()


def get_available_years(data: pd.DataFrame) -> List[int]:
    """
    Récupère la liste des années disponibles dans les données.
    
    Args:
        data: DataFrame contenant les données
        
    Returns:
        Liste triée des années uniques
    """
    if 'YEAR' not in data.columns:
        return []
    
    return sorted(data['YEAR'].unique().tolist())
