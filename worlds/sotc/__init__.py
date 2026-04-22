# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification, CollectionState
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule

from .Items import SotcItem, SotcItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool
from .Locations import SotcLocation, SotcLocationCategory, SotcLocationData, location_tables, location_dictionary
from .Options import (
    SotcOption,
    SoulShardQuantity,
    GridSanityToggle,
    ClimbSanityToggle,
    ClimbSanityRange,
    ClimbSanityBreakPoints,
    AgroSanityToggle,
    AgroSanityRange,
    AgroSanityBreakPoints,
    GuaranteedItemsOption,
)

# from .Rules import (
#     set_vanilla_key_item_progression,
#     set_vanilla_boss_progression,
#     set_open_progression,
#     set_time_trial_rules,
#     set_chain_unlock_rules,
#     set_break_art_rules,
#     set_blood_sin_endgame_rule,
#     set_one_way_door_rules,
#     set_vanilla_break_art_prerequisite,
# )
from .VictoryConditions import kill_all_colossi


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

    game: str = "Vagrant Story"
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

        regions["Menu"] = self.create_region("Menu", [])
        regions["Prologue"] = self.create_region("Prologue", location_tables["Prologue"])
        regions["Ashley"] = self.create_region("Ashley", location_tables["Ashley"])
        regions["Credits"] = self.create_region("Credits", location_tables["Credits"])

        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        def create_room_connections(from_region: str, to_region: str, connection_name: str):
            connection = Entrance(self.player, connection_name, regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        create_connection("Menu", "Ashley")
        create_connection("Ashley", "Menu")

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
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

        self.multiworld.regions.append(new_region)
        return new_region

    def create_items(self):
        randomized_location_count = 0
        for location in self.multiworld.get_locations(self.player):
            if not location.locked and location.address is not None:
                randomized_location_count += 1

        print(f"Requesting itempool size for randomized locations: {randomized_location_count}")

        # Call BuildItemPool to get a list of item NAMES (strings)
        item_names_to_add = BuildItemPool(randomized_location_count, self)

        generated_items: List[Item] = []

        for item_name in item_names_to_add:
            new_item = self.create_item(item_name)
            generated_items.append(new_item)

        print(f"Created item pool size: {len(generated_items)}")

        # Add the generated SotcItem objects to the multiworld's item pool
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
            item_data.progression
            or item_data.category == SotcItemCategory.STAMINA_UP
            or item_data.category == SotcItemCategory.BOSS_TOME
            or item_data.category == SotcItemCategory.SOUL_SHARD
        ):
            item_classification = ItemClassification.progression
        # elif (
        #     item_data.category == SotcItemCategory.
        #     or item_data.category == SotcItemCategory.CHAIN_ABILITY
        #     or item_data.category == SotcItemCategory.DEFENCE_ABILITY
        # ):
        #     item_classification = ItemClassification.useful
        else:  # Default for FILLER or other categories not explicitly useful/progression
            item_classification = ItemClassification.filler

        return SotcItem(name, item_classification, SotcItem.get_name_to_id()[name], self.player, self.options)

    def get_filler_item_name(self) -> str:
        return "Gil (50)"  # this clearly needs looked into

    def set_rules(self) -> None:
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                set_rule(location, lambda state: True)

        # from Utils import visualize_regions

        # state = self.multiworld.get_all_state(False)
        # state.update_reachable_regions(self.player)
        # visualize_regions(
        #     self.get_region("Menu"), "vs_layout.puml", show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player]
        # )

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        name_to_vagrant_story_code = {item.name: item.sotc_code for item in item_dictionary(self.options).values()}
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
                    items_address.append(name_to_vagrant_story_code[location.item.name])

            if location.player == self.player:
                # we are the sender of the location check
                locations_address.append(item_dictionary(self.options)[location_dictionary[location.name].default_item].sotc_code)
                locations_id.append(location.address)
                if location.item is not None:
                    if location.item.player == self.player:
                        locations_target.append(name_to_vagrant_story_code[location.item.name])
                    else:
                        locations_target.append(0)

        slot_data = {
            "options": {
                "goal": self.options.goal.value,
                "soul_shard_quantity": self.options.soul_shard_quantity.value,
                "gridsanity": self.options.gridsanity.value,
                "climbsanity": self.options.climbsanity.value,
                "climbsanity_range": self.options.climbsanity_range.value,
                "climbsanity_break_points": self.options.climbsanity_break_points.value,
                "agrosanity": self.options.agrosanity.value,
                "argosanity_range": self.options.agrosanity_range.value,
                "argosanity_break_points": self.options.agrosanity_break_points.value,
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
