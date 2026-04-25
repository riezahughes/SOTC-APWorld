from worlds.generic.Rules import set_rule, add_rule
from rule_builder.rules import Has, HasAll
from BaseClasses import CollectionState, Iterable


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
