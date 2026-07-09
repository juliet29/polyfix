from copy import deepcopy

from polyfix.geometry.layout import Layout
from polyfix.layout.interfaces import AxGraph, GraphPairs


def get_domain_by_surface(surface_name: str, layout: Layout):
    return layout.get_surface_by_name(surface_name).domain_name


def capture_zone_adjacencies(Gx: AxGraph, Gy: AxGraph):
    # TODO: this is pretty inefficient
    def nb_pairs_to_domain_pairs(pairs: GraphPairs, layout: Layout):
        d: dict[str, list[str]] = {}
        for k, v in pairs.items():
            new_k = get_domain_by_surface(k, layout)
            new_vs = [get_domain_by_surface(k, layout) for k in v]
            d[new_k] = new_vs
        return d

    layout = Gx.layout
    dx = nb_pairs_to_domain_pairs(Gx.nb_pairs, layout)
    dy = nb_pairs_to_domain_pairs(Gy.nb_pairs, layout)

    dnew = deepcopy(dx)
    for k, v in dy.items():
        if k in dnew.keys():
            dnew[k].extend(v)
        else:
            dnew[k] = v
    return dnew
