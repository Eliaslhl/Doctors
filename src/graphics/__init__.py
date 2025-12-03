"""
Module de graphiques pour le dashboard de vaccination.
"""

from .country_details import create_country_details
from .vaccination_table import create_vaccination_table
from .map import create_vaccination_map
from .pie_chart import create_pie_chart
from .statistics import (
    create_statistics_cards,
    create_statistics_histogram,
    create_statistics_boxplot
)
from .timed_count import (
    create_timed_count,
    create_yearly_comparison
)
from .tree_map import (
    create_tree_map,
    create_sunburst,
    create_hierarchical_bar
)

__all__ = [
    'create_country_details',
    'create_vaccination_table',
    'create_vaccination_map',
    'create_pie_chart',
    'create_statistics_cards',
    'create_statistics_histogram',
    'create_statistics_boxplot',
    'create_timed_count',
    'create_yearly_comparison',
    'create_tree_map',
    'create_sunburst',
    'create_hierarchical_bar',
]
