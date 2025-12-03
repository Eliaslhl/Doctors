"""
Module de chargement et traitement de données.
"""

from typing import List
from pathlib import Path
import pandas as pd

from config import RAW_DATA_DIR


def load_vaccination_data() -> pd.DataFrame:
    """
    Charge les données de vaccination depuis le fichier CSV.
    Si le fichier n'existe pas ou est vide, retourne un DataFrame vide avec les bonnes colonnes.
    
    Returns:
        DataFrame contenant les données de vaccination (peut être vide)
    """
    filepath = RAW_DATA_DIR / "rawdata.csv"
    
    # Colonnes attendues pour les données de vaccination
    expected_columns = ['GROUP', 'CODE', 'NAME', 'YEAR', 'ANTIGEN', 'COVERAGE']
    
    try:
        data = pd.read_csv(filepath)
        print(f"✓ Données chargées depuis {filepath}")
        return data
    except (FileNotFoundError, pd.errors.EmptyDataError):
        print(f"⚠️  Fichier {filepath} non trouvé ou vide - Dashboard lancé en mode vide")
        # Retourne un DataFrame vide avec les colonnes attendues
        return pd.DataFrame(columns=expected_columns)


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
