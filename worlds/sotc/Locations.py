from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import SotcItem


class SotcLocationCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    BOSS_KILL = 2
    LIZARD = 3
    FRUIT = 4
    CLIMB_DISTANCE = 5
    RIDE_DISTANCE = 6
    GRID_LOCATION = 7
    SHRINE = 8


class SotcLocationData(NamedTuple):
    name: str
    default_item: str
    category: SotcLocationCategory


class SotcLocation(Location):
    game: str = "Shadow of the Colossus"
    category: SotcLocationCategory
    default_item_name: str

    def __init__(
        self,
        player: int,
        name: str,
        category: SotcLocationCategory,
        default_item_name: str,
        address: Optional[int] = None,
        parent: Optional[Region] = None,
    ):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category
        self.name = name

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 99110000
        region_offset = 1000
        table_order = [""]

        output = {}
        for i, region_name in enumerate(table_order):
            current_region_base_id = base_id + (i * region_offset)
            # Ensure the region exists in location_tables
            if region_name in location_tables:
                # Enumerate the items within the current region, starting from current_region_base_id
                for j, location_data in enumerate(location_tables[region_name]):
                    # Assign an ID to each location within the region
                    # The ID for each location in a region will be current_region_base_id + j
                    # print(f"{current_region_base_id + j}: {location_data.name}")
                    output[location_data.name] = current_region_base_id + j

        return output

        # return {location_data.name: (base_id + location_data.m_code) for location_data in location_tables["MainWorld"]}

    def place_locked_item(self, item: SotcItem):
        self.item = item
        self.locked = True
        item.location = self


location_tables = {
    "Traversal": [
        SotcLocationData("Riding Distance: 1000", "Sliver of Hope (HP)", SotcLocationCategory.RIDE_DISTANCE),
    ],
    "C1": [],
    "D1": [],
    "E1": [],
    "F1": [],
    "G1": [],
    "C2": [],
    "D2": [],
    "E2": [],
    "F2": [],
    "G2": [],
    "B3": [],
    "C3": [],
    "D3": [],
    "E3": [],
    "F3": [],
    "G3": [],
    "B4": [],
    "C4": [],
    "D4": [],
    "E4": [],
    "F4": [],
    "G4": [],
    "H4": [],
    "B5": [],
    "C5": [],
    "D5": [],
    "E5": [],
    "F5": [],
    "G5": [],
    "C6": [],
    "D6": [],
    "E6": [],
    "F6": [],
    "G6": [],
    "H6": [],
    "D7": [],
    "E7": [],
    "F7": [],
    "G7": [],
    "H7": [],
    "E8": [],
    "F8": [],
    "G8": [],
}

location_dictionary: Dict[str, SotcLocationData] = {}  #
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
