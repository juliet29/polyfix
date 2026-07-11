from utils4plans.geom import Coord
from utils4plans.geom import CoordsType

green_north = 3.9
pink_north = 3.8

layout_coords: dict[str, CoordsType] = {
    "blue": [(1, 1), (4, 1), (4, 2), (1, 2)],
    "yellow": [(1, 2.1), (2, 2.1), (2, 3), (1, 3)],
    "green": [
        (2.1, 2.2),
        (4, 2.2),
        (4, 3.1),
        (3, 3.1),
        (3, green_north),
        (2.1, green_north),
    ],
    "pink": [(3.1, 3.3), (4, 3.3), (4, pink_north), (3.1, pink_north)],
    "red": [(1, 3.1), (2, 3.1), (2, 4), (4, 4), (4, 5), (1, 5), (1, 3.1)],
}


def gen_square(top_left: tuple[float, float], size: int) -> CoordsType:
    tl = Coord(*top_left)
    sz = size
    tr = (tl.x + sz, tl.y)
    br = (tl.x + sz, tl.y - sz)
    bl = (tl.x, tl.y - sz)

    order = [tl.as_tuple, tr, br, bl]
    # logger.debug(f"{tl=}")
    # logger.debug(f"{size=}")
    # logger.debug(f"{tr=}")
    return order


smart_graph_example: dict[str, CoordsType] = {
    "A": gen_square((0, 3), 2),
    "B": gen_square((3, 3), 1),
    "C": gen_square((4, 1.5), 1),
}

# Partial-overlap gap after y-move: `wide`'s north wall (x 0->4 @ y=2) faces
# `narrow`'s south wall (x 1->3 @ y=2.05) across a 0.05 gap. Because wide.north
# overhangs the overlap (0->1 and 3->4 stick out), closing the gap correctly
# requires splitting wide.north at x=1,3 and moving only the middle segment.
split_gap_example: dict[str, CoordsType] = {
    "wide": [(0, 0), (4, 0), (4, 2), (0, 2)],
    "narrow": [(1, 2.05), (3, 2.05), (3, 4), (1, 4)],
}

example_layouts = [layout_coords, smart_graph_example, split_gap_example]
