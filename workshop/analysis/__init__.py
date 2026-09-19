"""Reusable teaching helpers for NBML eye-tracking analysis sessions."""

from .aoi import aoi_metrics_from_fixations, hit_test_rectangles, load_default_food_aois
from .ivt import ivt_classify, summarize_ivt_events
from .paths import REPO_ROOT, data_path, stimuli_path
from .stats_report import apa_ttest, cohens_d, mean_sd_table
from .viz import fixation_heatmap, gaze_plot_tobii_like

__all__ = [
    "REPO_ROOT",
    "data_path",
    "stimuli_path",
    "ivt_classify",
    "summarize_ivt_events",
    "hit_test_rectangles",
    "load_default_food_aois",
    "aoi_metrics_from_fixations",
    "fixation_heatmap",
    "gaze_plot_tobii_like",
    "mean_sd_table",
    "cohens_d",
    "apa_ttest",
]
