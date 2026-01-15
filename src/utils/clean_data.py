"""
Module de nettoyage des données de vaccination.

Ce module transforme les données brutes (rawdata.csv) en données nettoyées (cleaneddata.csv)
en appliquant plusieurs étapes de nettoyage et de validation.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from config import CLEANED_DATA_DIR, RAW_DATA_DIR


def clean_vaccination_data(
    input_file: Path | None = None, output_file: Path | None = None
) -> pd.DataFrame:
    """
    Nettoie les données de vaccination brutes.

    Étapes de nettoyage :
    1. Suppression des lignes avec valeurs manquantes critiques
    2. Conversion des types de données
    3. Suppression des doublons
    4. Normalisation des valeurs de couverture
    5. Validation des années
    6. Nettoyage des noms de pays

    Args:
        input_file: Chemin du fichier d'entrée (défaut: data/raw/rawdata.csv)
        output_file: Chemin du fichier de sortie (défaut: data/cleaned/cleaneddata.csv)

    Returns:
        DataFrame contenant les données nettoyées

    Raises:
        FileNotFoundError: Si le fichier d'entrée n'existe pas
        ValueError: Si les données sont invalides
    """
    # chemins par défaut
    if input_file is None:
        input_file = RAW_DATA_DIR / "rawdata.csv"
    if output_file is None:
        output_file = CLEANED_DATA_DIR / "cleaneddata.csv"

    if not input_file.exists():
        raise FileNotFoundError(f"Le fichier {input_file} n'existe pas")

    print(f"📂 Chargement des données depuis {input_file}...")
    data = pd.read_csv(input_file)
    initial_rows = len(data)
    print(f"✓ {initial_rows} enregistrements chargés")
    print(f"\n📋 Colonnes détectées: {list(data.columns)}")

    # Supprime les lignes avec valeurs manquantes critiques
    print("\n🧹 Étape 1: Suppression des valeurs manquantes critiques...")
    critical_columns = ["GROUP", "CODE", "NAME", "YEAR", "ANTIGEN", "COVERAGE"]
    data_clean = data.dropna(subset=critical_columns)
    removed_missing = initial_rows - len(data_clean)
    print(f"✓ {removed_missing} lignes supprimées")

    # Convertit les types de données
    print("\n🔄 Étape 2: Conversion des types de données...")
    data_clean["YEAR"] = pd.to_numeric(data_clean["YEAR"], errors="coerce")
    data_clean["COVERAGE"] = pd.to_numeric(data_clean["COVERAGE"], errors="coerce")
    data_clean = data_clean.dropna(subset=["YEAR", "COVERAGE"])
    data_clean["YEAR"] = data_clean["YEAR"].astype(int)
    print("✓ Types convertis (YEAR: int, COVERAGE: float)")

    # Valide les années (1980-2025)
    print("\n📅 Étape 3: Validation des années...")
    current_year = 2025
    min_year = 1980
    data_clean = data_clean[(data_clean["YEAR"] >= min_year) & (data_clean["YEAR"] <= current_year)]
    year_range = f"{data_clean['YEAR'].min()} - {data_clean['YEAR'].max()}"
    print(f"✓ Années valides: {year_range}")

    # Normalise la couverture (0-100%)
    print("\n📊 Étape 4: Normalisation de la couverture...")
    data_clean.loc[data_clean["COVERAGE"] < 0, "COVERAGE"] = 0
    data_clean.loc[data_clean["COVERAGE"] > 100, "COVERAGE"] = 100
    coverage_stats = f"{data_clean['COVERAGE'].min():.1f}% - {data_clean['COVERAGE'].max():.1f}%"
    print(f"✓ Couverture normalisée: {coverage_stats}")

    # Nettoie les textes
    print("\n🔤 Étape 5: Nettoyage des textes...")
    text_columns = ["GROUP", "CODE", "NAME", "ANTIGEN", "COVERAGE_CATEGORY"]
    for col in text_columns:
        if col in data_clean.columns:
            data_clean[col] = data_clean[col].astype(str).str.strip()
            data_clean[col] = data_clean[col].replace("", np.nan)
    print(f"✓ {len(text_columns)} colonnes nettoyées")

    # Supprime les doublons
    print("\n🔍 Étape 6: Suppression des doublons...")
    before_dedup = len(data_clean)
    duplicate_cols = ["CODE", "NAME", "YEAR", "ANTIGEN", "COVERAGE_CATEGORY"]
    data_clean = data_clean.drop_duplicates(subset=duplicate_cols, keep="first")
    duplicates_removed = before_dedup - len(data_clean)
    print(f"✓ {duplicates_removed} doublons supprimés")

    # Trie les données
    print("\n📑 Étape 7: Tri des données...")
    data_clean = data_clean.sort_values(
        by=["NAME", "YEAR", "ANTIGEN"], ascending=[True, True, True]
    )
    print("✓ Données triées (NAME → YEAR → ANTIGEN)")

    data_clean = data_clean.reset_index(drop=True)

    final_rows = len(data_clean)
    retention_rate = (final_rows / initial_rows) * 100

    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU NETTOYAGE")
    print("=" * 60)
    print(f"Enregistrements initiaux : {initial_rows}")
    print(f"Enregistrements finaux   : {final_rows}")
    print(f"Supprimés                : {initial_rows - final_rows}")
    print(f"Taux de rétention        : {retention_rate:.1f}%")
    print(f"\nPays uniques             : {data_clean['NAME'].nunique()}")
    print(f"Années                   : {data_clean['YEAR'].nunique()}")
    print(f"Antigènes                : {data_clean['ANTIGEN'].nunique()}")
    print(f"Couverture moyenne       : {data_clean['COVERAGE'].mean():.2f}%")
    print("=" * 60)

    # Sauvegarde les données nettoyées
    print(f"\n💾 Sauvegarde dans {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    data_clean.to_csv(output_file, index=False)
    print("✓ Données sauvegardées!")

    return data_clean


def validate_cleaned_data(data: pd.DataFrame) -> bool:
    """Valide les données nettoyées."""
    print("\n🔍 Validation des données...")

    issues = []

    # Vérifie les colonnes requises
    required_columns = ["GROUP", "CODE", "NAME", "YEAR", "ANTIGEN", "COVERAGE"]
    for col in required_columns:
        if col not in data.columns:
            issues.append(f"❌ Colonne manquante: {col}")

    # Vérifie les valeurs manquantes
    for col in required_columns:
        if col in data.columns:
            missing = data[col].isna().sum()
            if missing > 0:
                issues.append(f"⚠️  {missing} valeurs manquantes dans {col}")

    # Vérifie les plages de valeurs
    if "COVERAGE" in data.columns and (
        (data["COVERAGE"] < 0).any() or (data["COVERAGE"] > 100).any()
    ):
        issues.append("❌ Couverture hors plage (0-100%)")

    if "YEAR" in data.columns and ((data["YEAR"] < 1980).any() or (data["YEAR"] > 2025).any()):
        issues.append("❌ Années invalides")

    # Affiche les résultats
    if issues:
        print("\n⚠️  Problèmes détectés:")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print("✅ Validation réussie")
        return True


def get_data_quality_report(data: pd.DataFrame) -> dict:
    """Génère un rapport de qualité des données."""
    missing_counts = data.isna().sum()
    completeness = (1 - (missing_counts / len(data))) * 100

    report = {
        "total_records": len(data),
        "countries": data["NAME"].nunique() if "NAME" in data.columns else 0,
        "years": data["YEAR"].nunique() if "YEAR" in data.columns else 0,
        "antigens": data["ANTIGEN"].nunique() if "ANTIGEN" in data.columns else 0,
        "coverage_mean": data["COVERAGE"].mean() if "COVERAGE" in data.columns else 0,
        "coverage_median": data["COVERAGE"].median() if "COVERAGE" in data.columns else 0,
        "coverage_std": data["COVERAGE"].std() if "COVERAGE" in data.columns else 0,
        "missing_values": missing_counts.to_dict(),
        "data_completeness": completeness.to_dict(),
    }

    return report


if __name__ == "__main__":
    """Script principal de nettoyage des données."""
    print("🏥 NETTOYAGE DES DONNÉES DE VACCINATION")
    print("=" * 60)

    try:
        # Nettoie les données
        cleaned_data = clean_vaccination_data()

        # Valide les données
        is_valid = validate_cleaned_data(cleaned_data)

        # Génère le rapport de qualité
        report = get_data_quality_report(cleaned_data)

        print("\n📈 RAPPORT DE QUALITÉ")
        print("=" * 60)
        print(f"Complétude moyenne: {np.mean(list(report['data_completeness'].values())):.1f}%")

        if is_valid:
            print("\n✅ Nettoyage terminé avec succès!")
        else:
            print("\n⚠️  Nettoyage terminé avec des avertissements")

    except Exception as e:
        print(f"\n❌ Erreur lors du nettoyage: {e}")
        raise
