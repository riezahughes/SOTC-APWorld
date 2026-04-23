from enum import IntEnum
from typing import Optional, NamedTuple, Dict, List

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
            "Grid F0",
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

        # Pre-register all possible Climbing Distance check IDs (max range 5000m, min breakpoint 1m)
        _climb_id_base = 99200001
        for n in range(1, 5001):
            output[f"Climbing Distance: {n}"] = _climb_id_base + n - 1

        # Pre-register all possible Riding Distance check IDs (max range 50000m, min breakpoint 1m)
        _ride_id_base = 99210001
        for n in range(1, 50001):
            output[f"Riding Distance: {n}"] = _ride_id_base + n - 1

        return output

        # return {location_data.name: (base_id + location_data.m_code) for location_data in location_tables["MainWorld"]}

    def place_locked_item(self, item: SotcItem):
        self.item = item
        self.locked = True
        item.location = self


location_tables = {
    "Grid F0": [
        SotcLocationData("Map Grid F0", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid C1": [
        SotcLocationData("Map Grid C1", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("C1 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("C1 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("C1 - Fruit - South 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("C1 - Fruit - South 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid D1": [
        SotcLocationData("Map Grid D1", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("Eel Kill - Col. 7", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
    ],
    "Grid E1": [
        SotcLocationData("Map Grid E1", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("E1 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("E1 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid F1": [
        SotcLocationData("Map Grid F1", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("Leo Kill - Col. 11", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("F1 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F1 - Fruit - South West", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid G1": [
        SotcLocationData("Map Grid G1", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("G1 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("Minotaur C Kill - Col. 15", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("G1 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G1 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid C2": [
        SotcLocationData("Map Grid C2", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid D2": [
        SotcLocationData("Map Grid D2", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("D2 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("D2 - Lizard - North", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("D2 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid E2": [
        SotcLocationData("Map Grid E2", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
    ],
    "Grid F2": [
        SotcLocationData("Map Grid F2", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("F2 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("F2 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F2 - Lizard - North", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid G2": [
        SotcLocationData("Map Grid G2", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("G2 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("Poseidon Kill - Col. 12", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("G2 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid B3": [
        SotcLocationData("Map Grid B3", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("B3 - Lizard - South East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid C3": [
        SotcLocationData("Map Grid C3", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("C3 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("Cerberus Kill - Col. 14", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("C3 - Lizard - South West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("C3 - Fruit - South", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid D3": [
        SotcLocationData("Map Grid D3", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("Kame Kill - Col. 9", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
    ],
    "Grid E3": [
        SotcLocationData("Map Grid E3", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("E3 - Shrine North", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("E3 - Shrine South", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("Knight Kill - Col. 3", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("E3 - Lizard - South East 1", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E3 - Lizard - South East 2", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E3 - Lizard - North West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E3 - Fruit - North East 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("E3 - Fruit - North East 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid F3": [
        SotcLocationData("Map Grid F3", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("Mammoth Kill - Col. 2", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
    ],
    "Grid G3": [
        SotcLocationData("Map Grid G3", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("G3 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("G3 - Lizard - North West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid B4": [
        SotcLocationData("Map Grid B4", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("B4 - Shrine North", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("B4 - Shrine South", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("Narga Kill - Col. 10", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("B4 - Lizard - North East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("B4 - Lizard - South West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid C4": [
        SotcLocationData("Map Grid C4", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("C4 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("C4 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("C4 - Lizard - North East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("C4 - Lizard - North West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("C4 - Fruit - Center 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("C4 - Fruit - Center 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid D4": [
        SotcLocationData("Map Grid D4", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("D4 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("D4 - Lizard - North West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("C4 - Fruit - North West 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("C4 - Fruit - North West 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid E4": [
        SotcLocationData("Map Grid E4", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("E4 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("E4 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E4 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid F4": [
        SotcLocationData("Map Grid F4", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("F4 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("F4 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F4 - Lizard - South West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid G4": [
        SotcLocationData("Map Grid G4", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("G4 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("G4 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G4 - Fruit - North East", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid H4": [
        SotcLocationData("Map Grid H4", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("Bird Kill - Col. 5", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("H4 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid B5": [
        SotcLocationData("Map Grid B5", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("B5 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("B5 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("B5 - Fruit - East 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("B5 - Fruit - East 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid C5": [
        SotcLocationData("Map Grid C5", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("C5 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("C5 - Lizard - South East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("C5 - Fruit - South West 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("C5 - Fruit - South West 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("C5 - Fruit - East", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid D5": [
        SotcLocationData("Map Grid D5", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("D5 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("D5 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("D5 - Lizard - East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid E5": [
        SotcLocationData("Map Grid E5", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("E5 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("E5 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E5 - Lizard - North East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E5 - Fruit - Center 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("E5 - Fruit - Center 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("E5 - Fruit - East", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid F5": [
        SotcLocationData("Map Grid F5", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("Minotaur A Kill - Col. 1", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("F5 - Lizard - North", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F5 - Lizard - South", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E5 - Fruit - North", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid G5": [
        SotcLocationData("Map Grid G5", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("Kirin Kill - Col. 4", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("G5 - Lizard - East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G5 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid C6": [
        SotcLocationData("Map Grid C6", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("C6 - Lizard - North East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid D6": [
        SotcLocationData("Map Grid D6", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("Minotaur B Kill - Col. 6", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("D6 - Lizard - North", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("D6 - Lizard - North East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("D6 - Fruit - North East 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("D6 - Fruit - North East 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid E6": [
        SotcLocationData("Map Grid E6", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("Snake Kill - Col. 13", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("E6 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E6 - Lizard - South East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E6 - Lizard - North West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid F6": [
        SotcLocationData("Map Grid F6", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("F6 - Lizard - South East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F6 - Fruit - South East 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("F6 - Fruit - South East 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid G6": [
        SotcLocationData("Map Grid G6", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("G6 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("Yamori B Kill - Col. 8", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("G6 - Lizard - North West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G6 - Fruit - East", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid H6": [
        SotcLocationData("Map Grid H6", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("H6 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("H6 - Lizard - Center 1", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("H6 - Lizard - Center 2", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("H6 - Lizard - North East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("H6 - Lizard - South", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid D7": [
        SotcLocationData("Map Grid D7", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("D7 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("D7 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("D7 - Lizard - North", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("D7 - Fruit - North East 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("D7 - Fruit - North East 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid E7": [
        SotcLocationData("Map Grid E7", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("E7 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E7 - Lizard - East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E7 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("E7 - Fruit - West 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("E7 - Fruit - West 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
    "Grid F7": [
        SotcLocationData("Map Grid F7", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("F7 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("F7 - Lizard - Center 1", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F7 - Lizard - Center 2", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F7 - Lizard - North", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F7 - Lizard - North East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F7 - Lizard - South West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F7 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("F7 - Lizard - North West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid G7": [
        SotcLocationData("Map Grid G7", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("G7 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G7 - Lizard - North", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G7 - Lizard - North East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G7 - Lizard - South East", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G7 - Lizard - South West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G7 - Lizard - North West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid H7": [
        SotcLocationData("Map Grid H7", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("H7 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("H7 - Lizard - North West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid E8": [
        SotcLocationData("Map Grid E8", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("E8 - Lizard - North", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid F8": [
        SotcLocationData("Map Grid F8", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("F8 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("Evis Kill - Col. 16", "Sliver of Hope HP", SotcLocationCategory.BOSS_KILL),
        SotcLocationData("F8 - Lizard - Center", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
    ],
    "Grid G8": [
        SotcLocationData("Map Grid G8", "Sliver of Hope HP", SotcLocationCategory.GRID_LOCATION),
        SotcLocationData("G8 - Shrine", "Sliver of Hope HP", SotcLocationCategory.SHRINE),
        SotcLocationData("G8 - Lizard - West", "Sliver of Hope HP", SotcLocationCategory.LIZARD),
        SotcLocationData("G8 - Fruit - North East 1", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
        SotcLocationData("G8 - Fruit - North East 2", "Sliver of Hope HP", SotcLocationCategory.FRUIT),
    ],
}


def create_traversal_locations(options) -> List[SotcLocationData]:
    """Generate climb and ride distance check locations based on player options.

    Checks are placed at each multiple of the breakpoint value up to the total range.
    If the range does not divide evenly by the breakpoint, a final check is added at
    the exact range value. E.g. range=1000, breakpoints=300 → checks at 300, 600, 900, 1000.
    """
    locations: List[SotcLocationData] = []

    if options.climbsanity.value:
        climb_range = options.climbsanity_range.value
        climb_bp = options.climbsanity_break_points.value
        for i in range(1, climb_range // climb_bp + 1):
            locations.append(
                SotcLocationData(
                    f"Climbing Distance: {i * climb_bp}",
                    "Sliver of Hope HP",
                    SotcLocationCategory.CLIMB_DISTANCE,
                )
            )
        if climb_range % climb_bp != 0:
            locations.append(
                SotcLocationData(
                    f"Climbing Distance: {climb_range}",
                    "Sliver of Hope HP",
                    SotcLocationCategory.CLIMB_DISTANCE,
                )
            )

    if options.agrosanity.value:
        ride_range = options.agrosanity_range.value
        ride_bp = options.agrosanity_break_points.value
        for i in range(1, ride_range // ride_bp + 1):
            locations.append(
                SotcLocationData(
                    f"Riding Distance: {i * ride_bp}",
                    "Sliver of Hope HP",
                    SotcLocationCategory.RIDE_DISTANCE,
                )
            )
        if ride_range % ride_bp != 0:
            locations.append(
                SotcLocationData(
                    f"Riding Distance: {ride_range}",
                    "Sliver of Hope HP",
                    SotcLocationCategory.RIDE_DISTANCE,
                )
            )

    return locations


location_dictionary: Dict[str, SotcLocationData] = {}  #
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
