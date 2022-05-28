from enum import Enum


class City(Enum):
    AUX = "Auckland"
    WGTN = "Wellington"
    CHCH = "Christchurch"
    DUD = "Dunedin"

    def to_dict():
        return {c.name: c.value for c in City}


class Country(Enum):
    NZ = "NZ"

    def to_dict():
        return {c.name: c.value for c in Country}
