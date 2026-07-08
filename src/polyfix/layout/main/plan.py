import networkx as nx
from loguru import logger
from pipe import sort, where
from rich.pretty import pretty_repr
from utils4plans.lists import chain_flatten

from polyfix.geometry.layout import Layout
from polyfix.geometry.paired_coords import PairedCoord
from polyfix.geometry.surfaces import FancyRange, Surface
from polyfix.geometry.vectors import Axes
from polyfix.layout.interfaces import AxGraph, Edge, EdgeData, EdgeDataDiGraph
from polyfix.layout.neighbors import get_nbs_for_surf


def compute_delta_between_surfs(s1: Surface, s2: Surface):
    # TODO: feels like it should be a method on surface..
    delta = FancyRange(s1.location, s2.location).size
    return delta


def create_graph_for_surface(
    layout: Layout,
    surf: Surface,
):
    nbs = get_nbs_for_surf(layout, surf)
    G = EdgeDataDiGraph()  # nx.DiGraph()
    for nb in nbs:
        delta = compute_delta_between_surfs(surf, nb)
        # delta = FancyRange(surf.location, nb.location).size
        G.add_edge(str(surf), str(nb), data=EdgeData(delta, surf.domain_name))

    # TODO: modify delta based on the overarching graph...., basically, have opportunities for bi-directional moves..
    return G


def create_individual_graphs(layout: Layout, axis: Axes):
    surfaces = list(
        layout.get_surfaces(substantial_only=True)
        | where(lambda x: x.perpendicular_axis == axis)
        | where(lambda x: x.direction.name == "north" or x.direction.name == "east")
        | sort(key=lambda x: x.location)
    )

    graphs = [create_graph_for_surface(layout, i) for i in surfaces]
    return graphs


def create_graph_for_all_surfaces_along_axis(layout: Layout, axis: Axes):
    # TODO: this is duplicated below, and appears to only exist for testing -> fix!
    graphs = create_individual_graphs(layout, axis)

    G = nx.compose_all(graphs)
    return AxGraph(G, axis, layout)


def filter_intersections(Gax: AxGraph):
    # TODO: this may have to live somewhere elsee..
    def handle_edge(e: Edge):
        IS_VALID = True
        surf_u = Gax.layout.get_surface_by_name(e.u)
        surf_v = Gax.layout.get_surface_by_name(e.v)
        cu, cv = surf_u.centroid, surf_v.centroid
        pc = PairedCoord(cu, cv)
        line = pc.shapely_line
        for shape in domain_shapes:
            if line.crosses(shape):
                IS_VALID = False

        logger.debug(f"{e.u}:{cu} --- {e.v}:{cv} -- {IS_VALID}")
        return IS_VALID

    domain_shapes = [i.polygon for i in Gax.layout.domains]
    # NOTE: MODIFYING IN PLACE -> hopefully not too dangerous
    # for e in Gax.G.edge_data():
    #     is_valid = handle_edge(e)
    invalid_edges = [(e.u, e.v) for e in Gax.G.edge_data() if not handle_edge(e)]
    logger.info(f"Found invalid_edges: {invalid_edges}")

    Gax.G.remove_edges_from(invalid_edges)
    return Gax


def summarize_graph_list(graphs: list[EdgeDataDiGraph]):
    res = chain_flatten([g.edge_summary_list() for g in graphs])
    logger.info(pretty_repr(res))


def create_move_graph_for_all_surfaces_along_axis(layout: Layout, axis: Axes):
    graphs = create_individual_graphs(layout, axis)
    summarize_graph_list(graphs)

    G = nx.compose_all(graphs)
    Gax = AxGraph(G, axis, layout)
    filtered_Gax = filter_intersections(Gax)
    return filtered_Gax
