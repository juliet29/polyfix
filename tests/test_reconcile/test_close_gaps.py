from utils4plans.geom import CoordsType

from polyfix.cli.studies.examples.layout import split_gap_example
from polyfix.geometry.layout import create_layout_from_dict
from polyfix.reconcile.close_gaps import close_gaps
from polyfix.reconcile.gaps import find_gaps
from polyfix.reconcile.metrics import adjacency_graph, graph_edit_distance, is_valid

# full-overlap near-miss: two stacked full-width rooms offset by 0.05
offset_stack: dict[str, CoordsType] = {
    "low": [(0, 0), (4, 0), (4, 2), (0, 2)],
    "high": [(0, 2.05), (4, 2.05), (4, 4), (0, 4)],
}

aligned: dict[str, CoordsType] = {
    "low": [(0, 0), (4, 0), (4, 2), (0, 2)],
    "high": [(0, 2), (4, 2), (4, 4), (0, 4)],
}


def test_closes_partial_overlap_gap():
    layout = create_layout_from_dict(split_gap_example)
    G0 = adjacency_graph(layout)
    fixed = close_gaps(layout)
    assert find_gaps(fixed) == []
    assert is_valid(fixed)[0]
    assert graph_edit_distance(G0, adjacency_graph(fixed)) == 0


def test_closes_full_overlap_gap_by_coincidence():
    layout = create_layout_from_dict(offset_stack)
    assert len(find_gaps(layout)) == 1
    fixed = close_gaps(layout)
    assert find_gaps(fixed) == []
    # the two facing walls now sit on the same line
    low_n = fixed.get_domain("low").get_surface("north").location
    high_s = fixed.get_domain("high").get_surface("south").location
    assert low_n == high_s


def test_no_gaps_is_noop():
    layout = create_layout_from_dict(aligned)
    fixed = close_gaps(layout)
    assert [d.tuple_list for d in fixed.domains] == [d.tuple_list for d in layout.domains]
