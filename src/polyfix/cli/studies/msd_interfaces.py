from typing import Literal
from typing_extensions import NamedTuple
from polyfix.geometry.ortho import FancyOrthoDomain
from polyfix.geometry.layout import Layout

MSD_IDs = Literal[
    "106493",
    "146903",
    "146915",
    "146965",
    "19792",
    "22940",
    "27540",
    "48204",
    "48205",
    "49943",
    "56958",
    "57231",
    "58613",
    "60529",
    "60532",
    "60553",
    "67372",
    "67408",
    "71308",
    "71318",
]

DEFAULT_MSD: MSD_IDs = "106493"


class MSDLayout(NamedTuple):
    layout_id: str | MSD_IDs
    layout: Layout


class MSDDomainName(NamedTuple):
    layout_id: str | MSD_IDs
    domain_name: str

    def __repr__(self) -> str:
        return f"({self.layout_id}, {self.domain_name})"

    @property
    def display_name(self):
        return self.__repr__()


class MSDDomain(NamedTuple):
    name: MSDDomainName
    domain: FancyOrthoDomain
