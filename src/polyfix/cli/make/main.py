from pathlib import Path

from cyclopts import App
from utils4plans.logs import logset

from polyfix.geometry.vectors import Axes
from polyfix.main.process import move, ortho, plan, rotate, simplify

app = App()


@app.command()
def do_rotate(path: Path, out_path: Path):
    rotate(path, out_path)


@app.command()
def do_ortho(path: Path, out_path: Path):
    ortho(path, out_path)


@app.command()
def do_simplify(path: Path, out_path: Path):
    simplify(path, out_path)


@app.command()
def do_plan(ax: Axes, path: Path, out_path: Path):
    plan(ax, path, out_path)


@app.command()
def do_move(ax: Axes, path: Path, out_path: Path):
    move(ax, path, out_path)


def main():
    logset(to_stderr=True)
    app()


if __name__ == "__main__":
    main()
