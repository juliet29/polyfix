from dataclasses import dataclass

from polyfix.geometry.ortho import FancyOrthoDomain


@dataclass(frozen=True)
class DomainName:
    layout_id: str
    domain_name: str

    def __repr__(self) -> str:
        return f"({self.layout_id}, {self.domain_name})"

    @property
    def display_name(self):
        return self.__repr__()


@dataclass(frozen=True)
class NamedDomain:
    name: DomainName
    domain: FancyOrthoDomain
