import pytest

from polyfix.cli.studies.examples.layout import split_gap_example
from polyfix.geometry.layout import create_layout_from_dict
from polyfix.geometry.modify.update import InvalidPolygonError, Move, update_domain
from polyfix.reconcile.split import split_surface


def get_wide():
    layout = create_layout_from_dict(split_gap_example)
    return layout.get_domain("wide")


def north_segments(domain):
    return sorted(
        [s for s in domain.surfaces if s.direction.name == "north"],
        key=lambda s: s.range.min,
    )


def test_split_preserves_geometry():
    dom = get_wide()
    split = split_surface(dom, dom.get_surface("north"), at=[1, 3])
    assert split.polygon.equals(dom.polygon)
    assert split.polygon.area == pytest.approx(dom.polygon.area)
    assert split.num_coords == dom.num_coords + 2


def test_split_creates_collinear_segments():
    dom = get_wide()
    split = split_surface(dom, dom.get_surface("north"), at=[1, 3])
    segs = north_segments(split)
    assert [(s.range.min, s.range.max) for s in segs] == [(0, 1), (1, 3), (3, 4)]


def test_naive_move_of_split_segment_is_non_ortho():
    # update_domain is a whole-wall move: it stretches the (perpendicular) side
    # walls. Applied to a split mid-segment, whose neighbours are COLLINEAR, it
    # slants them into diagonals instead of cutting a perpendicular jog. close_gaps
    # will need a jog-aware move; this pins the current boundary.
    dom = get_wide()
    split = split_surface(dom, dom.get_surface("north"), at=[1, 3])
    middle = next(s for s in north_segments(split) if s.range.min == 1)
    with pytest.raises(InvalidPolygonError):
        update_domain(Move(split, middle, delta=0.05))


def test_split_position_outside_range_rejected():
    dom = get_wide()
    with pytest.raises(AssertionError):
        split_surface(dom, dom.get_surface("north"), at=[5])
