"""Module de chargement et traitement de données."""

from typing import List, Optional
from pathlib import Path
import pandas as pd

from config import RAW_DATA_DIR, CLEANED_DATA_DIR


def load_vaccination_data(use_cleaned: bool = True) -> pd.DataFrame:
    """
    Charge les données de vaccination depuis le CSV.
    Par défaut, utilise cleaneddata.csv. Si absent, charge rawdata.csv.
    """
    expected_columns = ['GROUP', 'CODE', 'NAME', 'YEAR', 'ANTIGEN', 'COVERAGE']
    
    # Détermine quel fichier charger
    if use_cleaned:
        filepath = CLEANED_DATA_DIR / "cleaneddata.csv"
        fallback_filepath = RAW_DATA_DIR / "rawdata.csv"
    else:
        filepath = RAW_DATA_DIR / "rawdata.csv"
        fallback_filepath = None
    
    # Charge les données
    try:
        data = pd.read_csv(filepath)
        print(f"✓ Données chargées depuis {filepath} ({len(data)} enregistrements)")
        return data
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        # Fallback vers rawdata si cleaneddata absent
        if fallback_filepath and fallback_filepath.exists():
            print(f"⚠️  {filepath} non trouvé, utilisation de {fallback_filepath}")
            try:
                data = pd.read_csv(fallback_filepath)
                print(f"✓ Données brutes chargées ({len(data)} enregistrements)")
                print("💡 Exécute 'python src/utils/clean_data.py' pour générer cleaneddata.csv")
                return data
            except Exception:
                pass
        
        print(f"⚠️  Aucun fichier trouvé - Dashboard en mode vide")
        return pd.DataFrame(columns=expected_columns)


def filter_data_by_year(data: pd.DataFrame, years: List[int]) -> pd.DataFrame:
    """Filtre les données par année(s)."""
    if 'YEAR' not in data.columns:
        return data
    
    return data[data['YEAR'].isin(years)].copy()


def get_available_years(data: pd.DataFrame) -> List[int]:
    """Récupère la liste des années disponibles."""
    if 'YEAR' not in data.columns:
        return []
    
    return sorted(data['YEAR'].unique().tolist())
