from utils4plans.sets import set_difference

from polyfix.geometry.layout import Layout
from polyfix.layout.interfaces import Edge, EdgeData, EdgeDataDiGraph


def create_move_graph(layout: Layout, G: EdgeDataDiGraph):
    def transform(e: Edge):
        new_delta = -1 * (e.data.delta - min_edge.data.delta)
        new_domain = layout.get_surface_by_name(e.v).domain_name

        new_data = EdgeData(delta=new_delta, domain_name=new_domain)
        new_edge = Edge(e.v, e.u, new_data)
        return new_edge

    if len(G.edges) <= 1:
        return G

    # all the deltas are the same -> just need to move one..
    deltas = [i.data.delta for i in G.edge_data()]
    if len(set(deltas)) == 1:
        new_G = EdgeDataDiGraph()
        e = G.edge_data()[0]
        new_G.add_edge(e.u, e.v, data=e.data)
        return new_G

    min_edge = sorted(G.edge_data(), key=lambda x: x.data.delta)[0]
    other_edges = set_difference(G.edge_data(), [min_edge])
    new_edges = [transform(e) for e in other_edges] + [min_edge]

    new_G = EdgeDataDiGraph()
    for e in new_edges:
        if abs(e.data.delta) > 0:
            new_G.add_edge(e.u, e.v, data=e.data)
    # logger.info(pretty_repr(new_G.edge_data()))

    return new_G
