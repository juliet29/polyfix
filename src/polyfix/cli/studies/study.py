from pathlib import Path

from cyclopts import App
from loguru import logger
from utils4plans.io import read_json
from utils4plans.logs import logset

from polyfix.cli.studies.examples.layout import example_layouts
from polyfix.cli.studies.msd.study_msd import StudyMSDBends
from polyfix.cli.studies.paths import ProjectPaths
from polyfix.cli.studies.svgs.main import svg
from polyfix.geometry.layout import create_layout_from_dict
from polyfix.layout.main.move import try_moves
from polyfix.pydantic_models import AxGraphModel, write_layout

app = App()
app.command(svg)


@app.command()
def generate_examples():
    for ix, coords in enumerate(example_layouts):
        layout = create_layout_from_dict(coords)
        path = ProjectPaths.temp.generated / f"{1000 + ix}.json"
        write_layout(layout, path)


@app.command()
def report_bends_on_msd():
    s = StudyMSDBends()
    s.study_moves_all_domain()


@app.command()
def trial_move(path: Path):
    logger.info(path)
    Gax = AxGraphModel.model_validate(read_json(path)).to_axgraph()
    try_moves(Gax)


def main():
    logset(to_stderr=False)
    app()


if __name__ == "__main__":
    main()
