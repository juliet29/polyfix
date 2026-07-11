from dataclasses import dataclass

from pipe import where
from utils4plans.lists import chain_flatten

from polyfix.geometry.layout import Layout
from polyfix.geometry.range import FancyRange
from polyfix.geometry.surfaces import SMALL_SURFACE_SIZE, Surface

# north/east are the "positive" representatives (as in create_individual_graphs) so
# each facing pair is reported once, from the lower surface toward its neighbour.
POSITIVE_FACING = {"north", "east"}


@dataclass
class Gap:
    surface: Surface  # positive-facing (north/east)
    neighbor: Surface  # a facing surface across the gap (may be one of several)
    overlap: FancyRange
    distance: float

    @property
    def axis(self):
        return self.surface.parallel_axis

    def summary(self) -> str:
        return (
            f"{self.surface.name_w_domain} <-> {self.neighbor.name_w_domain} "
            f"| gap={self.distance:.4f} overlap=[{self.overlap.min:.3f},{self.overlap.max:.3f}]"
        )


def find_gaps(
    layout: Layout,
    eps_gap: float = 0.1,
    min_gap: float = 1e-3,
    min_overlap: float = SMALL_SURFACE_SIZE,
) -> list[Gap]:
    # Near-misses geomeppy won't match: for each positive-facing surface, every
    # facing surface (any room) that overlaps its span and sits min_gap < d <=
    # eps_gap beyond it. Unlike get_nbs_for_surf (which collapses to the single
    # binding neighbour for moving), detection must keep ALL overlapping faces so
    # partial-overlap gaps aren't missed. Units are the layout's own (polyfix frame).
    def facing_gaps(surf: Surface) -> list[Gap]:
        candidates = (
            layout.get_other_surfaces(surf, substantial_only=True)
            | where(lambda x: x.domain_name != surf.domain_name)
            | where(lambda x: x.parallel_axis == surf.parallel_axis)
            | where(lambda x: surf.range.is_coincident(x.range))
            | where(lambda x: min_gap < x.location - surf.location <= eps_gap)
        )
        return [
            Gap(surf, nb, overlap, nb.location - surf.location)
            for nb in candidates
            if (overlap := surf.range.intersection(nb.range, surf.parallel_axis)).size
            >= min_overlap
        ]

    representatives = layout.get_surfaces(substantial_only=True) | where(
        lambda s: s.direction.name in POSITIVE_FACING
    )
    gaps = chain_flatten([facing_gaps(s) for s in representatives])
    gaps.sort(
        key=lambda g: (
            g.axis,
            g.overlap.min,
            g.surface.domain_name,
            g.neighbor.domain_name,
        )
    )
    return gaps
