import pytest

from polyfix.cli.studies.examples.domains import create_ortho_domain
from polyfix.cli.studies.examples.layout import split_gap_example
from polyfix.geometry.layout import create_layout_from_dict
from polyfix.geometry.modify.update import Move, update_domain
from polyfix.reconcile.move_segment import move_segment
from polyfix.reconcile.split import split_surface


def get_wide():
    return create_layout_from_dict(split_gap_example).get_domain("wide")


def north_segments(domain):
    return sorted(
        [s for s in domain.surfaces if s.direction.name == "north"],
        key=lambda s: s.range.min,
    )


def test_move_split_middle_cuts_notch():
    dom = get_wide()
    split = split_surface(dom, dom.get_surface("north"), at=[1, 3])
    middle = next(s for s in north_segments(split) if s.range.min == 1)
    notched = move_segment(Move(split, middle, delta=0.05))
    assert notched.polygon.is_valid
    assert notched.is_orthogonal
    # notch = middle width (2) * delta (0.05)
    assert notched.polygon.area == pytest.approx(dom.polygon.area + 2 * 0.05)
    # the raised segment now sits at y = 2.05
    raised = [s for s in north_segments(notched) if s.range.min == 1][0]
    assert raised.location == pytest.approx(2.05)


def test_move_split_end_segment_cuts_step():
    # split at one point, move the left segment: one collinear neighbour (jog) and
    # one perpendicular neighbour (stretched) -> a single step, still orthogonal.
    dom = get_wide()
    split = split_surface(dom, dom.get_surface("north"), at=[2])
    left = next(s for s in north_segments(split) if s.range.min == 0)
    stepped = move_segment(Move(split, left, delta=0.05))
    assert stepped.polygon.is_valid
    assert stepped.is_orthogonal
    assert stepped.polygon.area == pytest.approx(dom.polygon.area + 2 * 0.05)


def test_move_segment_matches_update_domain_on_whole_wall():
    # both neighbours perpendicular -> jog-aware move must reduce to update_domain
    dom = create_ortho_domain("SQUARE")
    north = dom.get_surface("north")
    a = move_segment(Move(dom, north, delta=0.5))
    b = update_domain(Move(dom, north, delta=0.5))
    assert a.polygon.equals(b.polygon)
