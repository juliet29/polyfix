from pathlib import Path

import pyprojroot

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
TEMP_PATH = "/scratch/users/jnwagwu/polyfix"


class StaticPaths:
    inputs = Path(BASE_PATH) / "static/1_inputs"
    temp = Path(TEMP_PATH) / "data"
    figures = Path(TEMP_PATH) / "figures"
