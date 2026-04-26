from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification, CollectionState
from Options import Toggle, OptionError

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule

from .Items import SotcItem, SotcItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool
from .Locations import SotcLocation, SotcLocationCategory, SotcLocationData, location_tables, location_dictionary, create_traversal_locations
from .Options import (
    SotcOption,
    GoalOptions,
    SoulShardQuantity,
    LizardSanityToggle,
    FruitSanityToggle,
    ShrineSanityToggle,
    GridSanityToggle,
    ClimbSanityToggle,
    ClimbSanityRange,
    ClimbSanityBreakPoints,
    AgroSanityToggle,
    AgroSanityRange,
    AgroSanityBreakPoints,
    GuaranteedItemsOption,
)

from .Rules import set_boss_progression

from .VictoryConditions import kill_all_colossi, collect_all_shards, hunt_all_lizards


class SotcWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Shadow of the Colossus randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["RiezaHughes"],
    )

    tutorials = [setup_en]


class SotcWorld(World):
    """
    Sotc is a game about saving the princess that was, in fact, in another castle.
    """

    game: str = "Shadow of the Colossus"
    explicit_indirect_conditions = False
    options_dataclass = SotcOption
    options: SotcOption
    topology_present: bool = True
    web = SotcWeb()
    data_version = 0
    base_id = 1230000
    enabled_location_categories: Set[SotcLocationCategory]
    required_client_version = (0, 5, 0)
    item_name_to_id = SotcItem.get_name_to_id()
    location_name_to_id = SotcLocation.get_name_to_id()
    item_name_groups = {}
    item_descriptions = item_descriptions

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()

    def generate_early(self):
        self.enabled_location_categories.add(SotcLocationCategory.FILLER)
        self.enabled_location_categories.add(SotcLocationCategory.PROGRESSION)
        self.enabled_location_categories.add(SotcLocationCategory.BOSS_KILL)
        self.enabled_location_categories.add(SotcLocationCategory.CLIMB_DISTANCE)
        self.enabled_location_categories.add(SotcLocationCategory.RIDE_DISTANCE)
        self.enabled_location_categories.add(SotcLocationCategory.GRID_LOCATION)
        self.enabled_location_categories.add(SotcLocationCategory.FRUIT)
        self.enabled_location_categories.add(SotcLocationCategory.LIZARD)
        self.enabled_location_categories.add(SotcLocationCategory.SHRINE)

    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}

        list_of_regions = [
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
            "Grid A4",
            "Grid B4",
            "Grid C4",
            "Grid D4",
            "Grid E4",
            "Grid F4",
            "Grid G4",
            "Grid H4",
            "Grid A5",
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
            "Boss D1",
            "Boss F1",
            "Boss G1",
            "Boss C2",
            "Boss E2",
            "Boss G2",
            "Boss D3",
            "Boss F3",
            "Boss B4",
            "Boss H4",
            "Boss F5",
            "Boss G5",
            "Boss D6",
            "Boss E6",
            "Boss G6",
            "Boss F8",
        ]

        regions["Traversal"] = self.create_region("Traversal", create_traversal_locations(self.options))

        regions["Menu"] = self.create_region("Menu", [])
        regions["Game Clear"] = self.create_region("Game Clear", [])

        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in list_of_regions})

        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        create_connection("Menu", "Traversal")
        create_connection("Traversal", "Grid F4")  # Game Starting Position

        # C1 Connections
        create_connection("Grid C1", "Grid D1")
        create_connection("Grid C1", "Grid D2")
        create_connection("Grid C1", "Grid C2")

        # D1 Connections
        create_connection("Grid D1", "Grid C1")
        create_connection("Grid D1", "Grid D2")
        create_connection("Grid D1", "Grid E1")
        create_connection("Grid D1", "Boss D1")

        # E1 Connections
        create_connection("Grid E1", "Grid D1")
        create_connection("Grid E1", "Grid F1")

        # F1 Connections
        create_connection("Grid F1", "Grid F0")
        create_connection("Grid F1", "Grid E1")
        create_connection("Grid F1", "Grid F2")
        create_connection("Grid F1", "Grid G1")
        create_connection("Grid F1", "Boss F1")

        # G1 Connections
        create_connection("Grid G1", "Grid F1")
        create_connection("Grid G1", "Boss G1")

        # C2 Connections
        create_connection("Grid C2", "Grid C1")
        create_connection("Grid C2", "Boss C2")

        # D2 Connections
        create_connection("Grid D2", "Grid C1")
        create_connection("Grid D2", "Grid D1")
        create_connection("Grid D2", "Grid E2")
        create_connection("Grid D2", "Grid E3")
        create_connection("Grid D2", "Grid D3")

        # E2 Connections
        create_connection("Grid E2", "Grid D2")
        create_connection("Grid E2", "Grid E3")
        create_connection("Grid E2", "Boss E2")

        # F2 Connections
        create_connection("Grid F2", "Grid F1")
        create_connection("Grid F2", "Grid F3")

        # G2 Connections
        create_connection("Grid G2", "Grid G3")
        create_connection("Grid G2", "Boss G2")

        # B3 Connections
        create_connection("Grid B3", "Grid B4")
        create_connection("Grid B3", "Grid C3")

        # C3 Connections
        create_connection("Grid C3", "Grid B3")
        create_connection("Grid C3", "Grid C4")
        create_connection("Grid C3", "Grid D3")

        # D3 Connections
        create_connection("Grid D3", "Grid D2")
        create_connection("Grid D3", "Grid C3")
        create_connection("Grid D3", "Grid E3")
        create_connection("Grid D3", "Grid D4")
        create_connection("Grid D3", "Boss D3")

        # E3 Connections
        create_connection("Grid E3", "Grid D2")
        create_connection("Grid E3", "Grid D3")
        create_connection("Grid E3", "Grid F3")
        create_connection("Grid E3", "Grid E4")

        # F3 Connections
        create_connection("Grid F3", "Grid E3")
        create_connection("Grid F3", "Grid F2")
        create_connection("Grid F3", "Grid F4")
        create_connection("Grid F3", "Grid G3")
        create_connection("Grid F3", "Boss F3")

        # G3 Connections
        create_connection("Grid G3", "Grid G2")
        create_connection("Grid G3", "Grid F3")
        create_connection("Grid G3", "Grid G4")

        # A4 Connections
        create_connection("Grid A4", "Grid B4")
        create_connection("Grid A4", "Grid A5")

        # B4 Connections
        create_connection("Grid B4", "Grid C4")
        create_connection("Grid B4", "Grid A4")
        create_connection("Grid B4", "Grid B3")
        create_connection("Grid B4", "Boss B4")

        # C4 Connection
        create_connection("Grid C4", "Grid B4")
        create_connection("Grid C4", "Grid C3")
        create_connection("Grid C4", "Grid D4")

        # D4 Connection
        create_connection("Grid D4", "Grid C4")
        create_connection("Grid D4", "Grid E4")
        create_connection("Grid D4", "Grid D3")

        # E4 Connection
        create_connection("Grid E4", "Grid D4")
        create_connection("Grid E4", "Grid E3")
        create_connection("Grid E4", "Grid F4")
        create_connection("Grid E4", "Grid E5")

        # F4 Connection
        create_connection("Grid F4", "Grid E4")
        create_connection("Grid F4", "Grid F5")
        create_connection("Grid F4", "Grid G4")
        create_connection("Grid F4", "Grid F3")

        # G4 Connection
        create_connection("Grid G4", "Grid F4")
        create_connection("Grid G4", "Grid G3")
        create_connection("Grid G4", "Grid G5")
        create_connection("Grid G4", "Grid H4")

        # H4 Connection
        create_connection("Grid H4", "Grid G4")
        create_connection("Grid H4", "Boss H4")

        # A5 Connections
        create_connection("Grid A5", "Grid A4")
        create_connection("Grid A5", "Grid B5")

        # B5 Connections
        create_connection("Grid B5", "Grid A5")
        create_connection("Grid B5", "Grid C5")

        # C5 Connections
        create_connection("Grid C5", "Grid B5")
        create_connection("Grid C5", "Grid C6")
        create_connection("Grid C5", "Grid D5")

        # D5 Connections
        create_connection("Grid D5", "Grid C5")
        create_connection("Grid D5", "Grid D6")
        create_connection("Grid D5", "Grid E5")

        # E5 Connections
        create_connection("Grid E5", "Grid D5")
        create_connection("Grid E5", "Grid F5")
        create_connection("Grid E5", "Grid E6")

        # F5 Connections
        create_connection("Grid F5", "Grid E5")
        create_connection("Grid F5", "Grid G5")
        create_connection("Grid F5", "Grid F4")
        create_connection("Grid F5", "Grid F6")
        create_connection("Grid F5", "Boss F5")

        # G5 Connections
        create_connection("Grid G5", "Grid F5")
        create_connection("Grid G5", "Grid G6")
        create_connection("Grid G5", "Grid G4")
        create_connection("Grid G5", "Boss G5")

        # C6 Connections
        create_connection("Grid C6", "Grid C5")
        create_connection("Grid C6", "Grid D5")
        create_connection("Grid C6", "Grid D6")

        # D6 Connections
        create_connection("Grid D6", "Grid C6")
        create_connection("Grid D6", "Grid D5")
        create_connection("Grid D6", "Grid D7")
        create_connection("Grid D6", "Grid E6")
        create_connection("Grid D6", "Boss D6")

        # E6 Connections
        create_connection("Grid E6", "Grid E5")
        create_connection("Grid E6", "Grid E7")
        create_connection("Grid E6", "Grid D6")
        create_connection("Grid E6", "Grid F6")
        create_connection("Grid E6", "Boss E6")

        # F6 Connections
        create_connection("Grid F6", "Grid F5")
        create_connection("Grid F6", "Grid F7")
        create_connection("Grid F6", "Grid E6")
        create_connection("Grid F6", "Grid G6")

        # G6 Connections
        create_connection("Grid G6", "Grid G5")
        create_connection("Grid G6", "Grid G7")
        create_connection("Grid G6", "Grid F6")
        create_connection("Grid G6", "Grid H6")
        create_connection("Grid G6", "Boss G6")

        # H6 Connections
        create_connection("Grid H6", "Grid H7")
        create_connection("Grid H6", "Grid G6")

        # D7 Connections
        create_connection("Grid D7", "Grid D6")
        create_connection("Grid D7", "Grid E7")

        # E7 Connections
        create_connection("Grid E7", "Grid D7")
        create_connection("Grid E7", "Grid E6")
        create_connection("Grid E7", "Grid F7")
        create_connection("Grid E7", "Grid E8")

        # F7 Connections
        create_connection("Grid F7", "Grid E7")
        create_connection("Grid F7", "Grid F6")
        create_connection("Grid F7", "Grid F8")
        create_connection("Grid F7", "Grid G7")

        # G7 Connections
        create_connection("Grid G7", "Grid G6")
        create_connection("Grid G7", "Grid G8")
        create_connection("Grid G7", "Grid E7")
        create_connection("Grid G7", "Grid H7")

        # H7 Connections
        create_connection("Grid H7", "Grid G7")
        create_connection("Grid H7", "Grid H6")

        # E8 Connections
        create_connection("Grid E8", "Grid E7")

        # F8 connections
        create_connection("Grid F8", "Grid F7")
        create_connection("Grid F8", "Boss F8")

        create_connection("Boss F8", "Game Clear")

        # G8 Connections
        create_connection("Grid G8", "Grid G7")

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
            skip_regular_location = False
            if self.options.agrosanity.value == AgroSanityToggle.option_false and "Riding Distance" in location.name:
                continue
            if self.options.climbsanity.value == ClimbSanityToggle.option_false and "Climbing Distance" in location.name:
                continue
            if self.options.gridsanity.value == GridSanityToggle.option_false and "Map Grid" in location.name:
                continue
            if self.options.lizardsanity.value == LizardSanityToggle.option_false and "Lizard" in location.name:
                if self.options.goal == GoalOptions.HUNT_ALL_LIZARDS:
                    skip_regular_location = True
                else:
                    continue
            if self.options.fruitsanity.value == FruitSanityToggle.option_false and "Fruit" in location.name:
                continue
            if self.options.shrinesanity.value == ShrineSanityToggle.option_false and "Shrine" in location.name:
                continue
            if not skip_regular_location:
                if location.category in self.enabled_location_categories:
                    new_location = SotcLocation(
                        self.player,
                        location.name,
                        location.category,
                        location.default_item,
                        self.location_name_to_id[location.name],
                        new_region,
                    )
                else:
                    event_item = self.create_item(location.default_item)
                    new_location = SotcLocation(self.player, location.name, location.category, location.default_item, None, new_region)
                    event_item.code = None

                    if isinstance(event_item, SotcItem):
                        new_location.place_locked_item(event_item)
                new_region.locations.append(new_location)
            if location.category == SotcLocationCategory.LIZARD and self.options.goal == GoalOptions.HUNT_ALL_LIZARDS:
                event_loc = SotcLocation(self.player, f"{location.name} - Tail", SotcLocationCategory.LIZARD, "Lizard Tail", None, new_region)
                event_item = Item("Lizard Tail", ItemClassification.progression, None, self.player)
                event_loc.place_locked_item(event_item)
                new_region.locations.append(event_loc)

        self.multiworld.regions.append(new_region)
        return new_region

    def create_items(self):
        randomized_location_count = 0
        for location in self.multiworld.get_locations(self.player):
            if not location.locked and location.address is not None:
                randomized_location_count += 1

        print(f"Requesting itempool size for randomized locations: {randomized_location_count}")

        if self.options.goal.value == GoalOptions.SOUL_SHARD_SEARCH and self.options.soul_shard_quantity.value > randomized_location_count:
            raise OptionError(
                f"soul_shard_quantity ({self.options.soul_shard_quantity.value}) exceeds the total number of "
                f"available locations ({randomized_location_count}). Reduce soul_shard_quantity or enable "
                f"more sanity checks."
            )

        # Call BuildItemPool to get a list of item NAMES (strings)
        item_names_to_add = BuildItemPool(randomized_location_count, self)

        generated_items: List[Item] = []

        for item_name in item_names_to_add:
            new_item = self.create_item(item_name)
            generated_items.append(new_item)

        print(f"Created item pool size: {len(generated_items)}")

        self.multiworld.itempool.extend(generated_items)

    def create_item(self, name: str) -> Item:
        item_data = item_dictionary(self.options).get(name)

        if not item_data:
            # Fallback for unknown items. This indicates a data inconsistency.
            print(f"Warning: Attempted to create unknown item: {name}. Falling back to filler.")
            return SotcItem(name, ItemClassification.filler, None, self.player, self.options)

        # Determine the Archipelago ItemClassification based on SotcItemData.
        item_classification: ItemClassification

        if (
            item_data.category == SotcItemCategory.STAMINA_UP
            or item_data.category == SotcItemCategory.HP_UP
            or item_data.category == SotcItemCategory.BOSS_SIGIL
            or item_data.category == SotcItemCategory.SOUL_SHARD
        ):
            item_classification = ItemClassification.progression
        if item_data.category == SotcItemCategory.PASSIVE_ABILITY or item_data.category == SotcItemCategory.EQUIPMENT:
            item_classification = ItemClassification.useful
        elif item_data.category == SotcItemCategory.TRAP:
            item_classification = ItemClassification.trap
        else:  # Default for FILLER or other categories not explicitly useful/progression
            item_classification = ItemClassification.filler

        return SotcItem(name, item_classification, SotcItem.get_name_to_id()[name], self.player, self.options)

    def get_filler_item_name(self) -> str:
        return "Gil (50)"  # this clearly needs looked into

    def set_rules(self) -> None:
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                set_rule(location, lambda state: True)

        if self.options.goal.value == GoalOptions.KILL_ALL_COLOSSI:
            self.set_completion_rule(kill_all_colossi())
        elif self.options.goal.value == GoalOptions.SOUL_SHARD_SEARCH:
            self.set_completion_rule(collect_all_shards())
        elif self.options.goal.value == GoalOptions.HUNT_ALL_LIZARDS:
            self.set_completion_rule(hunt_all_lizards(self.options.lizard_quantity.value))

        set_boss_progression(self)

        # from Utils import visualize_regions

        # state = self.multiworld.get_all_state(False)
        # state.update_reachable_regions(self.player)
        # visualize_regions(
        #     self.get_region("Menu"), "vs_layout.puml", show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player]
        # )

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        name_to_sotc_code = {item.name: item.sotc_code for item in item_dictionary(self.options).values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():
            if location.item is not None:
                if location.item.player == self.player:
                    # we are the receiver of the item
                    items_id.append(location.item.code)
                    items_address.append(name_to_sotc_code[location.item.name])

            if location.player == self.player and location.address is not None:
                # we are the sender of the location check (skip events)
                locations_address.append(item_dictionary(self.options)[location.default_item_name].sotc_code)
                locations_id.append(location.address)
                if location.item is not None:
                    if location.item.player == self.player:
                        locations_target.append(name_to_sotc_code[location.item.name])
                    else:
                        locations_target.append(0)

        slot_data = {
            "options": {
                "goal": self.options.goal.value,
                "colossi_quantity": self.options.colossi_quantity.value,
                "soul_shard_quantity": self.options.soul_shard_quantity.value,
                "lizard_quantity": self.options.lizard_quantity.value,
                "fruitsanity": self.options.fruitsanity.value,
                "lizardsanity": self.options.lizardsanity.value,
                "gridsanity": self.options.gridsanity.value,
                "climbsanity": self.options.climbsanity.value,
                "climbsanity_range": self.options.climbsanity_range.value,
                "climbsanity_break_points": self.options.climbsanity_break_points.value,
                "agrosanity": self.options.agrosanity.value,
                "argosanity_range": self.options.agrosanity_range.value,
                "argosanity_break_points": self.options.agrosanity_break_points.value,
                "trap_toggle": self.options.trap_toggle.value,
                "trap_percentage": self.options.trap_percentage.value,
                "deathlink": self.options.deathlink.value,
                "guaranteed_items": self.options.guaranteed_items.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address,
        }

        return slot_data
