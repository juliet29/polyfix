from cyclopts import App
from loguru import logger
from utils4plans.io.extras.yaml import read_yaml, write_yaml

from polyfix.adjacencies.zonal import capture_zone_adjacencies
from polyfix.cli.studies.paths import ProjectPaths
from polyfix.main.process import move, plan
from polyfix.main.workflow_paths import SingleWorkflowPaths

svg = App("svg")


@svg.command
def fc():
    inpath = ProjectPaths.inputs.svg.ablation_c / "out.json"
    outpath = ProjectPaths.temp.svg

    sp = SingleWorkflowPaths(outpath)

    Gx = plan("X", inpath, sp.xplan)
    move("X", sp.xplan, sp.xmove)
    Gy = plan("Y", sp.xmove, sp.yplan)
    move("Y", sp.yplan, sp.ymove)
    zone_adjacencies = capture_zone_adjacencies(Gx, Gy)
    write_yaml(zone_adjacencies, outpath / "out.adj.yaml")
    res = read_yaml(outpath / "out.adj.yaml")
    logger.debug(res)

    # TODO: have workflow paths output matching tuples..
    # # Taking 2
    # plan("X", sp.ymove, sp.xplan_i())
    # plan("Y", sp.ymove, sp.yplan_i())
