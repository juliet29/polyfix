import pytest
from utils4plans.geom import CoordsType

from polyfix.cli.studies.examples.layout import split_gap_example
from polyfix.geometry.layout import create_layout_from_dict
from polyfix.reconcile.gaps import find_gaps

# two stacked rooms sharing a full-width edge, perfectly aligned at y=2
aligned: dict[str, CoordsType] = {
    "bottom": [(0, 0), (4, 0), (4, 2), (0, 2)],
    "top": [(0, 2), (4, 2), (4, 4), (0, 4)],
}


def test_detects_partial_overlap_gap():
    layout = create_layout_from_dict(split_gap_example)
    gaps = find_gaps(layout)
    assert len(gaps) == 1
    g = gaps[0]
    assert g.surface.name_w_domain == "wide-north_0"
    assert g.neighbor.name_w_domain == "narrow-south_0"
    assert g.distance == pytest.approx(0.05)
    assert (g.overlap.min, g.overlap.max) == (1, 3)


def test_aligned_layout_has_no_gaps():
    layout = create_layout_from_dict(aligned)
    assert find_gaps(layout) == []


def test_eps_gap_threshold_excludes_wide_gaps():
    layout = create_layout_from_dict(split_gap_example)
    assert find_gaps(layout, eps_gap=0.01) == []


def test_min_overlap_excludes_slivers():
    layout = create_layout_from_dict(split_gap_example)
    # overlap is 2 wide; demand more than that
    assert find_gaps(layout, min_overlap=2.5) == []
