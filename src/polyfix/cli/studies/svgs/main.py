from cyclopts import App

from polyfix.cli.studies.paths import ProjectPaths
from polyfix.main.process import plan
from polyfix.main.workflow_paths import SingleWorkflowPaths

svg = App("svg")


@svg.command
def fc():
    inpath = ProjectPaths.inputs.svg.ablation_c / "out.json"
    outpath = ProjectPaths.temp.svg

    sp = SingleWorkflowPaths(outpath)

    plan("X", inpath, sp.xplan)
