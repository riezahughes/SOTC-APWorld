from worlds.generic.Rules import set_rule, add_rule
from rule_builder.rules import Has, HasAll
from BaseClasses import CollectionState, Iterable


def set_boss_progression(self):
    self.set_rule(self.get_entrance("Grid D1 -> Boss D1"), Has("Sigil of the First Awakening"))
    self.set_rule(self.get_entrance("Grid F1 -> Boss F1"), Has("Sigil of Burdened Earth"))
    self.set_rule(self.get_entrance("Grid G1 -> Boss G1"), Has("Sigil of the Fallen Oath"))
    self.set_rule(self.get_entrance("Grid C2 -> Boss C2"), Has("Sigil of Veiled Fear"))
    self.set_rule(self.get_entrance("Grid E2 -> Boss E2"), Has("Sigil of the Skybound Silence"))
    self.set_rule(self.get_entrance("Grid G2 -> Boss G2"), Has("Sigil of the Hollow Shrine"))
    self.set_rule(self.get_entrance("Grid D3 -> Boss D3"), Has("Sigil of the Sunken Pulse"))
    self.set_rule(self.get_entrance("Grid F3 -> Boss F3"), Has("Sigil of the Watching Walls"))
    self.set_rule(self.get_entrance("Grid B4 -> Boss B4"), Has("Sigil of the Sealed Core"))
    self.set_rule(self.get_entrance("Grid H4 -> Boss H4"), Has("Sigil of the Devouring Wind"))
    self.set_rule(self.get_entrance("Grid F5 -> Boss F5"), Has("Sigil of the Broken Courage"))
    self.set_rule(self.get_entrance("Grid G5 -> Boss G5"), Has("Sigil of the Drowned Throne"))
    self.set_rule(self.get_entrance("Grid D6 -> Boss D6"), Has("Sigil of Endless Horizon"))
    self.set_rule(self.get_entrance("Grid E6 -> Boss E6"), Has("Sigil of Ruined Pride"))
    self.set_rule(self.get_entrance("Grid G6 -> Boss G6"), Has("Sigil of the Bound Colossus"))
    self.set_rule(
        self.get_entrance("Grid F8 -> Boss F8"),
        HasAll(*self.chosen_sigils).resolve(self),
    )
