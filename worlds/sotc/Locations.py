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
        table_order = [
            "Traversal",
            "Grid C1",
            "Grid D1",
            "Grid E1",
            "Grid F1",
            "Grid G1",
            "Grid C2",
            "Grid D2",
            "Grid E2",
            "Grid F2",
            "Grid G2",
            "Grid B3",
            "Grid C3",
            "Grid D3",
            "Grid E3",
            "Grid F3",
            "Grid G3",
            "Grid B4",
            "Grid C4",
            "Grid D4",
            "Grid E4",
            "Grid F4",
            "Grid G4",
            "Grid H4",
            "Grid B5",
            "Grid C5",
            "Grid D5",
            "Grid E5",
            "Grid F5",
            "Grid G5",
            "Grid C6",
            "Grid D6",
            "Grid E6",
            "Grid F6",
            "Grid G6",
            "Grid H6",
            "Grid D7",
            "Grid E7",
            "Grid F7",
            "Grid G7",
            "Grid H7",
            "Grid E8",
            "Grid F8",
            "Grid G8",
        ]

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
    "Grid C1": [
        SotcLocationData("Map Grid C1", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid D1": [
        SotcLocationData("Map Grid D1", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid E1": [
        SotcLocationData("Map Grid E1", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid F1": [
        SotcLocationData("Map Grid F1", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid G1": [
        SotcLocationData("Map Grid G1", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid C2": [
        SotcLocationData("Map Grid C2", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid D2": [
        SotcLocationData("Map Grid D2", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid E2": [
        SotcLocationData("Map Grid E2", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid F2": [
        SotcLocationData("Map Grid F2", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid G2": [
        SotcLocationData("Map Grid G2", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid B3": [
        SotcLocationData("Map Grid B3", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid C3": [
        SotcLocationData("Map Grid C3", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid D3": [
        SotcLocationData("Map Grid D3", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid E3": [
        SotcLocationData("Map Grid E3", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid F3": [
        SotcLocationData("Map Grid F3", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid G3": [
        SotcLocationData("Map Grid G3", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid B4": [
        SotcLocationData("Map Grid B4", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid C4": [
        SotcLocationData("Map Grid C4", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid D4": [
        SotcLocationData("Map Grid D4", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid E4": [
        SotcLocationData("Map Grid E4", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid F4": [
        SotcLocationData("Map Grid F4", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid G4": [
        SotcLocationData("Map Grid G4", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid H4": [
        SotcLocationData("Map Grid H4", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid B5": [
        SotcLocationData("Map Grid B5", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid C5": [
        SotcLocationData("Map Grid C5", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid D5": [
        SotcLocationData("Map Grid D5", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid E5": [
        SotcLocationData("Map Grid E5", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid F5": [
        SotcLocationData("Map Grid F5", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid G5": [
        SotcLocationData("Map Grid G5", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid C6": [
        SotcLocationData("Map Grid C6", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid D6": [
        SotcLocationData("Map Grid D6", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid E6": [
        SotcLocationData("Map Grid E6", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid F6": [
        SotcLocationData("Map Grid F6", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid G6": [
        SotcLocationData("Map Grid G6", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid H6": [
        SotcLocationData("Map Grid H6", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid D7": [
        SotcLocationData("Map Grid D7", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid E7": [
        SotcLocationData("Map Grid E7", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid F7": [
        SotcLocationData("Map Grid F7", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid G7": [
        SotcLocationData("Map Grid G7", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid H7": [
        SotcLocationData("Map Grid H7", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid E8": [
        SotcLocationData("Map Grid E8", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid F8": [
        SotcLocationData("Map Grid F8", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid G8": [
        SotcLocationData("Map Grid G8", "Sliver of Hope (HP)", SotcLocationCategory.GRID_LOCATION),
    ],
}

# Take the max distance you want and divide it by the break points to get the checks, then on the last one, if it doesn't round correctly
# just add the final check as whatever the distance would end at. Eg, 1000 distance with 300 break points would give you checks at 300, 600, 900,
# and then the final check would be at 1000 instead of 1200.

location_dictionary: Dict[str, SotcLocationData] = {}  #
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
