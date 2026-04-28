from worlds.generic.Rules import set_rule, add_rule
from rule_builder.rules import Has, HasAll
from BaseClasses import CollectionState, Iterable

# Maps each boss kill location to the sigil required to enter that boss region.
# Used to prevent a boss kill location from rewarding the sigil needed to access it.
boss_kill_to_access_sigil = {
    "Eel Kill - Col. 7": "Sigil of the First Awakening",
    "Leo Kill - Col. 11": "Sigil of Burdened Earth",
    "Minotaur C Kill - Col. 15": "Sigil of the Fallen Oath",
    "Cerberus Kill - Col. 14": "Sigil of Veiled Fear",
    "Knight Kill - Col. 3": "Sigil of the Skybound Silence",
    "Poseidon Kill - Col. 12": "Sigil of the Hollow Shrine",
    "Kame Kill - Col. 9": "Sigil of the Sunken Pulse",
    "Mammoth Kill - Col. 2": "Sigil of the Watching Walls",
    "Narga Kill - Col. 10": "Sigil of the Sealed Core",
    "Bird Kill - Col. 5": "Sigil of the Devouring Wind",
    "Mintaur A Kill - Col. 1": "Sigil of the Broken Courage",
    "Kirin Kill - Col. 4": "Sigil of the Drowned Throne",
    "Minotaur B Kill - Col. 6": "Sigil of Endless Horizon",
    "Snake Kill - Col. 13": "Sigil of Ruined Pride",
    "Yamori B Kill - Col. 8": "Sigil of the Bound Colossus",
    "Evis Kill - Col. 16": None,
}


def set_boss_progression(self):
    boss_sigil_map = {
        "Grid D1 -> Boss D1": "Sigil of the First Awakening",
        "Grid F1 -> Boss F1": "Sigil of Burdened Earth",
        "Grid G1 -> Boss G1": "Sigil of the Fallen Oath",
        "Grid C2 -> Boss C2": "Sigil of Veiled Fear",
        "Grid E2 -> Boss E2": "Sigil of the Skybound Silence",
        "Grid G2 -> Boss G2": "Sigil of the Hollow Shrine",
        "Grid D3 -> Boss D3": "Sigil of the Sunken Pulse",
        "Grid F3 -> Boss F3": "Sigil of the Watching Walls",
        "Grid B4 -> Boss B4": "Sigil of the Sealed Core",
        "Grid H4 -> Boss H4": "Sigil of the Devouring Wind",
        "Grid F5 -> Boss F5": "Sigil of the Broken Courage",
        "Grid G5 -> Boss G5": "Sigil of the Drowned Throne",
        "Grid D6 -> Boss D6": "Sigil of Endless Horizon",
        "Grid E6 -> Boss E6": "Sigil of Ruined Pride",
        "Grid G6 -> Boss G6": "Sigil of the Bound Colossus",
    }
    chosen = set(self.chosen_sigils)
    for entrance, sigil in boss_sigil_map.items():
        if sigil in chosen:
            self.set_rule(self.get_entrance(entrance), Has(sigil))
    if self.chosen_sigils:
        self.set_rule(
            self.get_entrance("Grid F7 -> Grid F8"),
            HasAll(*self.chosen_sigils),
        )
