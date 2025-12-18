"""
Module pour récupérer les données depuis différentes sources.
Centralise toutes les fonctions de récupération de données.
"""

import pandas as pd
from pathlib import Path
from typing import Optional


def get_vaccination_data(use_cleaned: bool = True) -> pd.DataFrame:
    """
    Récupère les données de vaccination depuis le fichier CSV.
    
    Args:
        use_cleaned: Si True, charge cleaneddata.csv, sinon rawdata.csv
        
    Returns:
        DataFrame avec les données de vaccination
    """
    base_path = Path(__file__).parent.parent.parent / "data"
    
    if use_cleaned:
        file_path = base_path / "cleaned" / "cleaneddata.csv"
    else:
        file_path = base_path / "raw" / "rawdata.csv"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Fichier non trouvé: {file_path}")
    
    print(f"✓ Données chargées depuis {file_path} ", end="")
    data = pd.read_csv(file_path)
    print(f"({len(data)} enregistrements)")
    
    return data


def get_available_years(data: pd.DataFrame) -> list[int]:
    """
    Récupère la liste des années disponibles dans les données.
    
    Args:
        data: DataFrame contenant les données
        
    Returns:
        Liste triée des années uniques
    """
    if "YEAR" not in data.columns:
        return []
    
    return sorted(data["YEAR"].dropna().unique().tolist())


def get_available_countries(data: pd.DataFrame) -> list[str]:
    """
    Récupère la liste des pays disponibles dans les données.
    
    Args:
        data: DataFrame contenant les données
        
    Returns:
        Liste triée des pays uniques
    """
    if "NAME" not in data.columns:
        return []
    
    return sorted(data["NAME"].dropna().unique().tolist())


def get_available_antigens(data: pd.DataFrame) -> list[str]:
    """
    Récupère la liste des antigènes disponibles dans les données.
    
    Args:
        data: DataFrame contenant les données
        
    Returns:
        Liste triée des antigènes uniques
    """
    if "ANTIGEN" not in data.columns:
        return []
    
    return sorted(data["ANTIGEN"].dropna().unique().tolist())


def get_available_coverage_categories(data: pd.DataFrame) -> list[str]:
    """
    Récupère la liste des catégories de couverture disponibles.
    
    Args:
        data: DataFrame contenant les données
        
    Returns:
        Liste triée des catégories uniques
    """
    if "COVERAGE_CATEGORY" not in data.columns:
        return []
    
    return sorted(data["COVERAGE_CATEGORY"].dropna().unique().tolist())


def get_filtered_data(
    data: pd.DataFrame,
    year: Optional[int] = None,
    country: Optional[str] = None,
    antigen: Optional[str] = None,
    coverage_category: Optional[str] = None
) -> pd.DataFrame:
    """
    Filtre les données selon les critères spécifiés.
    
    Args:
        data: DataFrame contenant les données
        year: Année à filtrer (optionnel)
        country: Pays à filtrer (optionnel)
        antigen: Antigène à filtrer (optionnel)
        coverage_category: Catégorie de couverture à filtrer (optionnel)
        
    Returns:
        DataFrame filtré
    """
    filtered = data.copy()
    
    if year is not None and "YEAR" in filtered.columns:
        filtered = filtered[filtered["YEAR"] == year]
    
    if country is not None and "NAME" in filtered.columns:
        filtered = filtered[filtered["NAME"] == country]
    
    if antigen is not None and "ANTIGEN" in filtered.columns:
        filtered = filtered[filtered["ANTIGEN"] == antigen]
    
    if coverage_category is not None and "COVERAGE_CATEGORY" in filtered.columns:
        if coverage_category != "Toutes":
            filtered = filtered[filtered["COVERAGE_CATEGORY"] == coverage_category]
    
    return filtered


def get_data_summary(data: pd.DataFrame) -> dict:
    """
    Récupère un résumé des données.
    
    Args:
        data: DataFrame contenant les données
        
    Returns:
        Dictionnaire avec les statistiques résumées
    """
    summary = {
        "total_records": len(data),
        "total_countries": data["NAME"].nunique() if "NAME" in data.columns else 0,
        "total_antigens": data["ANTIGEN"].nunique() if "ANTIGEN" in data.columns else 0,
        "year_range": (
            int(data["YEAR"].min()), 
            int(data["YEAR"].max())
        ) if "YEAR" in data.columns else (None, None),
        "coverage_categories": data["COVERAGE_CATEGORY"].nunique() if "COVERAGE_CATEGORY" in data.columns else 0
    }
    
    return summary
