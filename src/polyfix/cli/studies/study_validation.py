# validation

from loguru import logger

from polyfix.examples.paths import ExamplePaths
from polyfix.geometry.modify.validate import (
    validate_layout_no_holes,
)
from polyfix.pydantic_models import read_layout_from_path


class StudyValidation:
    bad_case = "71308"
    good_case = "27540"
    ymove = "ymove/out.json"
    path = ExamplePaths.msd_outputs / bad_case / ymove

    @property
    def layout(self):
        return read_layout_from_path(self.path)

    def try_validate_no_holes(self):
        res = validate_layout_no_holes(self.layout)
        logger.info(res)

    # def try_validate_no_overlaps(self):
    #     validate_layout_domain(self.layout)
