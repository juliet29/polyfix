from polyfix.paths import static_paths


class ExamplePaths:
    MSD_PATHS = static_paths.inputs / "msd"
    example_paths = static_paths.inputs / "examples"
    msd_outputs = static_paths.temp / "msd"
