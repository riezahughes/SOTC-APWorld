from enum import IntEnum
from typing import NamedTuple, List, Optional, cast
from BaseClasses import Item, ItemClassification
from .Options import GridSanityToggle


class SotcItemCategory(IntEnum):
    FILLER = 0
    SKIP = 1
    HP_UP = 2
    STAMINA_UP = 3
    BOSS_SIGIL = 4
    SOUL_SHARD = 5
    LIZARD_TAIL = 6
    TRAP = 7


class SotcItemData(NamedTuple):
    name: str
    category: SotcItemCategory
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

        return {item_data.name: base_id + i + 1 for i, item_data in enumerate(_all_items)}


key_item_names = {}

# 1 Minotaur A — Sigil of the First Awakening
# 2 Mammoth — Sigil of Burdened Earth
# 3 Knight — Sigil of the Fallen Oath
# 4 Kirin — Sigil of Veiled Fear
# 5 Bird — Sigil of the Skybound Silence
# 6 Minotaur B — Sigil of the Hollow Shrine
# 7 Eel — Sigil of the Sunken Pulse
# 8 Yamori B — Sigil of the Watching Walls
# 9 Kame — Sigil of the Sealed Core
# 10 Narga — Sigil of the Devouring Wind
# 11 Leo — Sigil of the Broken Courage
# 12 Poseidon — Sigil of the Drowned Throne
# 13 Snake — Sigil of Endless Horizon
# 14 Cerberus — Sigil of Ruined Pride
# 15 Minotaur C — Sigil of the Bound Colossus
# 16 Evis — Sigil of the Final Blasphemy

items: List[SotcItemData] = [
    SotcItemData("Sliver of Hope HP", SotcItemCategory.FILLER),
    SotcItemData("Sliver of Courage Stamina", SotcItemCategory.FILLER),
    SotcItemData("Soul Shard", SotcItemCategory.SOUL_SHARD),
    SotcItemData("Lizard Tail", SotcItemCategory.LIZARD_TAIL),
    SotcItemData("Progressive Stamina Capacity", SotcItemCategory.STAMINA_UP),
    SotcItemData("Progressive Health Capacity", SotcItemCategory.HP_UP),
    SotcItemData("Sigil of the First Awakening", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of Burdened Earth", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Fallen Oath", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of Veiled Fear", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Skybound Silence", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Hollow Shrine", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Sunken Pulse", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Watching Walls", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Sealed Core", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Devouring Wind", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Broken Courage", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Drowned Throne", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of Endless Horizon", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of Ruined Pride", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Bound Colossus", SotcItemCategory.BOSS_SIGIL),
    SotcItemData("Sigil of the Final Blasphemy", SotcItemCategory.BOSS_SIGIL),
    SotcItemData(
        "Trap: Loose Reins",
        SotcItemCategory.TRAP,
    ),
    SotcItemData(
        "Trap: Sweaty Palms",
        SotcItemCategory.TRAP,
    ),
    SotcItemData(
        "Trap: Tired",
        SotcItemCategory.TRAP,
    ),
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

    # Pick a random subset of sigils based on colossi_count
    all_sigils = [item.name for item in _all_items if item.category == SotcItemCategory.BOSS_SIGIL]
    colossi_quantity = self.options.colossi_quantity.value
    chosen_sigils = self.multiworld.random.sample(all_sigils, min(colossi_quantity, len(all_sigils)))
    self.chosen_sigils = chosen_sigils

    # Add Soul Shards based on the soul_shard_quantity option
    soul_shards = ["Soul Shard"] * self.options.soul_shard_quantity.value

    # Add non-sigil progression items (stamina, hp) as normal
    progression_items = [
        item.name for item in _all_items if item.category in [SotcItemCategory.STAMINA_UP, SotcItemCategory.HP_UP] for _ in range(item.quantity or 1)
    ]

    for name in chosen_sigils + soul_shards + progression_items:
        if len(item_pool_names) < count:
            item_pool_names.append(name)

    # Fill the remaining slots with filler and optional traps
    filler_candidates = [item.name for item in _all_items if item.category == SotcItemCategory.FILLER for _ in range(item.quantity or 1)]
    trap_candidates = [item.name for item in _all_items if item.category == SotcItemCategory.TRAP]

    remaining = count - len(item_pool_names)
    if self.options.trap_toggle.value and trap_candidates:
        trap_count = round(remaining * (self.options.trap_percentage.value / 100))
        trap_names = [self.multiworld.random.choice(trap_candidates) for _ in range(trap_count)]
        filler_names = [
            self.multiworld.random.choice(filler_candidates) if filler_candidates else "Sliver of Hope HP" for _ in range(remaining - trap_count)
        ]
        item_pool_names.extend(trap_names + filler_names)
    else:
        while len(item_pool_names) < count:
            item_pool_names.append(self.multiworld.random.choice(filler_candidates) if filler_candidates else "Sliver of Hope HP")

    self.multiworld.random.shuffle(item_pool_names)
    return item_pool_names
