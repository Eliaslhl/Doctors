"""
Module de graphiques pour le dashboard de vaccination.
"""

from .country_details import create_country_details
from .map import create_vaccination_map
from .pie_chart import create_pie_chart
from .statistics import (
    create_statistics_boxplot,
    create_statistics_cards,
    create_statistics_histogram,
)
from .timed_count import create_timed_count
from .tree_map import create_tree_map

__all__ = [
    "create_country_details",
    "create_vaccination_map",
    "create_pie_chart",
    "create_statistics_cards",
    "create_statistics_histogram",
    "create_statistics_boxplot",
    "create_timed_count",
    "create_tree_map",
]
