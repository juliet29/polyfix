from pathlib import Path

import pyprojroot

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
TEMP_PATH = "/scratch/users/jnwagwu/polyfix"


class StaticPaths:
    inputs = Path(BASE_PATH) / "static/1_inputs"
    temp = Path(TEMP_PATH) / "4_temp"
    figures = Path(TEMP_PATH) / "figures"


class MSDPaths:
    base = StaticPaths.inputs
    basic = base / "msd"
    hard = base / "msd_hard"


class Inputs:
    msd = MSDPaths


class Temp:
    base = StaticPaths.temp
    generated = base / "generated"
    process = base / "process"
    msd = base / "msd"


class ProjectPaths:
    inputs = Inputs
    temp = Temp
