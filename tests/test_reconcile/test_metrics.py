import pytest
import shapely
from utils4plans.geom import CoordsType

from polyfix.geometry.layout import create_layout_from_dict
from polyfix.reconcile.metrics import (
    adjacency_graph,
    graph_edit_distance,
    is_valid,
    shape_factor,
)

two_rooms: dict[str, CoordsType] = {
    "bottom": [(0, 0), (4, 0), (4, 2), (0, 2)],
    "top": [(0, 2), (4, 2), (4, 4), (0, 4)],
}

overlapping: dict[str, CoordsType] = {
    "a": [(0, 0), (4, 0), (4, 2), (0, 2)],
    "b": [(1, 1), (5, 1), (5, 3), (1, 3)],
}


def test_shape_factor_of_square_is_16():
    assert shape_factor(shapely.Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])) == pytest.approx(16)


def test_adjacency_graph_finds_shared_edge():
    G = adjacency_graph(create_layout_from_dict(two_rooms))
    assert G.has_edge("bottom", "top")


def test_ged_of_identical_graphs_is_zero():
    G = adjacency_graph(create_layout_from_dict(two_rooms))
    H = adjacency_graph(create_layout_from_dict(two_rooms))
    assert graph_edit_distance(G, H) == 0


def test_is_valid_accepts_disjoint_rooms():
    ok, _ = is_valid(create_layout_from_dict(two_rooms))
    assert ok


def test_is_valid_rejects_overlap():
    ok, reason = is_valid(create_layout_from_dict(overlapping))
    assert not ok
    assert "overlap" in reason
