"""
Module pour récupérer les données depuis différentes sources.
Centralise toutes les fonctions de récupération de données.
"""

from functools import lru_cache
from pathlib import Path

import pandas as pd


@lru_cache(maxsize=2)
def _load_csv_cached(file_path_str: str) -> pd.DataFrame:
    """
    Charge un fichier CSV avec mise en cache.

    Args:
        file_path_str: Chemin du fichier CSV (en string pour compatibilité cache)

    Returns:
        DataFrame chargé depuis le CSV
    """
    file_path = Path(file_path_str)
    return pd.read_csv(file_path)


def get_vaccination_data(use_cleaned: bool = True) -> pd.DataFrame:
    """
    Récupère les données de vaccination depuis le fichier CSV.
    Les données sont mises en cache pour améliorer les performances.

    Args:
        use_cleaned: Si True, charge cleaneddata.csv, sinon rawdata.csv

    Returns:
        DataFrame avec les données de vaccination

    Note:
        Les données sont automatiquement mises en cache. Pour rafraîchir,
        utilisez _load_csv_cached.cache_clear()
    """
    base_path = Path(__file__).parent.parent.parent / "data"

    if use_cleaned:
        file_path = base_path / "cleaned" / "cleaneddata.csv"
    else:
        file_path = base_path / "raw" / "rawdata.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Fichier non trouvé: {file_path}")

    print(f"✓ Données chargées depuis {file_path} ", end="")
    data = _load_csv_cached(str(file_path))
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


def get_available_regions(data: pd.DataFrame) -> list[str]:
    """
    Récupère la liste des régions WHO disponibles dans les données.

    Args:
        data: DataFrame contenant les données

    Returns:
        Liste triée des régions uniques
    """
    if "NAME" not in data.columns or "GROUP" not in data.columns:
        return []

    regions = data[data["GROUP"] == "WHO_REGIONS"]["NAME"].dropna().unique()
    return sorted(regions.tolist())


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
    group: str | None = None,
    year: int | None = None,
    country: str | None = None,
    antigen: str | None = None,
    coverage_category: str | None = None,
) -> pd.DataFrame:
    """
    Filtre les données selon les critères spécifiés.

    Args:
        data: DataFrame contenant les données
        group: Groupe à filtrer (COUNTRIES, WHO_REGIONS, etc.) (optionnel)
        year: Année à filtrer (optionnel)
        country: Pays/Région à filtrer (optionnel)
        antigen: Antigène à filtrer (optionnel)
        coverage_category: Catégorie de couverture à filtrer (optionnel)

    Returns:
        DataFrame filtré
    """
    filtered = data.copy()

    if group is not None and "GROUP" in filtered.columns:
        filtered = filtered[filtered["GROUP"] == group]

    if year is not None and "YEAR" in filtered.columns:
        filtered = filtered[filtered["YEAR"] == year]

    if country is not None and "NAME" in filtered.columns:
        filtered = filtered[filtered["NAME"] == country]

    if antigen is not None and "ANTIGEN" in filtered.columns:
        filtered = filtered[filtered["ANTIGEN"] == antigen]

    if (
        coverage_category is not None
        and "COVERAGE_CATEGORY" in filtered.columns
        and coverage_category != "Toutes"
    ):
        filtered = filtered[filtered["COVERAGE_CATEGORY"] == coverage_category]

    return filtered
