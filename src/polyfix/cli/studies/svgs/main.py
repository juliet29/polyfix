from copy import deepcopy
from pathlib import Path

from cyclopts import App
from loguru import logger
from rich.pretty import pretty_repr

from polyfix.cli.studies.paths import ProjectPaths
from polyfix.geometry.layout import Layout
from polyfix.geometry.vectors import Axes
from polyfix.layout.interfaces import AxGraph, GraphPairs
from polyfix.layout.main.plan import create_move_graph_for_all_surfaces_along_axis
from polyfix.main.process import move, plan
from polyfix.main.workflow_paths import SingleWorkflowPaths
from polyfix.pydantic_models import read_layout_from_path

svg = App("svg")


def get_domain_by_surface(surface_name: str, layout: Layout):
    return layout.get_surface_by_name(surface_name).domain_name


def mod_plan(ax: Axes, path: Path):
    in_layout = read_layout_from_path(path)
    Gax = create_move_graph_for_all_surfaces_along_axis(in_layout, ax)
    logger.debug(pretty_repr(Gax.nb_pairs))


def handle_Gs(Gx: AxGraph, Gy: AxGraph):
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


@svg.command
def fc():
    inpath = ProjectPaths.inputs.svg.ablation_c / "out.json"
    outpath = ProjectPaths.temp.svg

    sp = SingleWorkflowPaths(outpath)

    Gx = plan("X", inpath, sp.xplan)
    move("X", sp.xplan, sp.xmove)

    Gy = plan("Y", sp.xmove, sp.yplan)
    move("Y", sp.yplan, sp.ymove)

    dnew = handle_Gs(Gx, Gy)
    logger.debug(pretty_repr(dnew))
