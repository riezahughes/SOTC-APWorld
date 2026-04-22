from enum import IntEnum
from typing import NamedTuple, List, Optional, cast
from BaseClasses import Item, ItemClassification
from .Options import GridSanityToggle


class SotcItemCategory(IntEnum):
    FILLER = 0
    SKIP = 1
    HP_UP = 2
    STAMINA_UP = 3
    BOSS_TOME = 4
    SOUL_SHARD = 5


class SotcItemData(NamedTuple):
    name: str
    category: SotcItemCategory
    progression: bool
    quantity: Optional[int] = 1
    sotc_code: Optional[int] = None


class SotcItem(Item):
    game: str = "Shadow of the Colossus"
    category: SotcItemCategory
    v_code: Optional[int]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int, options):
        super().__init__(name, classification, code, player)

        item_data = item_dictionary(options).get(name)
        if item_data:
            self.sotc_code = item_data.sotc_code
            self.category = item_data.category
        else:
            self.sotc_code = None
            self.category = SotcItemCategory.FILLER  # Fallback for unknown items

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 9201000

        result = {item_data.name: (base_id + item_data.sotc_code) for item_data in _all_items if item_data.sotc_code is not None}

        # # Provides codes for optional items. This is just an example if needed
        # result["Teleport"] = 9910000
        # result["Rood Inverse"] = 9920000
        # result["Blood Sin Piece"] = 9930000

        return result


key_item_names = {}


items: List[SotcItemData] = [
    SotcItemData("Soul Shard", SotcItemCategory.SOUL_SHARD, True),  # needs ripped out and logic put somewhere else, but for now it's here as an item.
    SotcItemData("Progressive Stamina Capacity", SotcItemCategory.STAMINA_UP, True),
]

# Convert raw list of tuples into MedievilItemData NamedTuple instances
_all_items = [SotcItemData(row[0], row[1], row[2], row[3]) for row in items]


item_descriptions = {
    # Optional: Add detailed descriptions for items here
    # "Gold (50)": "A small pouch of gold coins."
}


# Create a dictionary for quick lookup of item data by name
def item_dictionary(options) -> dict[str, SotcItemData]:
    return {item_data.name: item_data for item_data in _all_items}


def BuildItemPool(count: int, self) -> List[str]:
    item_pool_names: List[str] = []

    if hasattr(self.options, "guaranteed_items") and self.options.guaranteed_items.value:
        for item_name in self.options.guaranteed_items.value:
            if item_name in item_dictionary(self.options):
                item_pool_names.append(item_name)

    # Add Mcguffins equal to the configured quantity — Vagrant Story Example for if needed
    # blood_sin_total = self.options.blood_sin_quantity.value
    # for _ in range(blood_sin_total):
    #     if len(item_pool_names) < count:
    #         item_pool_names.append("Blood Sin Piece")

    # optional item example
    # item_list_choice = (
    #     _vanilla_items.copy()
    #     if hasattr(self.options, "item_drop_option") and self.options.item_drop_option.value == ItemPoolDropOptions.VANILLA
    #     else _all_items.copy()
    # )

    # Add Progression (Keys/Sigils/Grimoires/Gems) — quantity copies of each
    progression_items = [
        item.name
        for item in _all_items
        if item.category in [SotcItemCategory.BOSS_TOME, SotcItemCategory.STAMINA_UP]
        for _ in range(item.quantity or 1)
    ]

    # optional item addition
    # if teleport_item is not None:
    #     item_list_choice.append(teleport_item)
    #     progression_items.append(teleport_item.name)

    for name in progression_items:
        if len(item_pool_names) < count:
            item_pool_names.append(name)

    # Fill the remaining slots with Recovery/Stats — expanded by quantity for weighted selection
    filler_candidates = [item.name for item in _all_items if item.category in [SotcItemCategory.FILLER] for _ in range(item.quantity or 1)]

    # Fill until we hit the requested 'count'
    while len(item_pool_names) < count:
        if filler_candidates:
            # Using choice here allows recovery items to repeat if the pool is very large
            item_pool_names.append(self.multiworld.random.choice(filler_candidates))
        else:
            # Extreme fallback if even recovery items are missing
            item_pool_names.append("Cure Bulb")
            if len(item_pool_names) >= count:
                break

    self.multiworld.random.shuffle(item_pool_names)
    return item_pool_names
