from polyfix.paths import StaticPaths


class ExamplePaths:
    MSD_PATHS = StaticPaths.inputs / "msd"
    example_paths = StaticPaths.inputs / "examples"
    msd_outputs = StaticPaths.temp / "msd"
