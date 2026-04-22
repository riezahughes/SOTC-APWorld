from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState, Iterable


def has_key_required(self, key: str, state: CollectionState):
    return state.has(key, self.player)


def has_sigil_required(self, sigil, state: CollectionState):
    return state.has(sigil, self.player)


def has_rood_inverse(self, state):
    return state.has("Rood Inverse", self.player)


def is_boss_defeated(self, boss: str, state: CollectionState):  # can used later
    return state.has("Boss: " + boss, self.player, 1)


# def set_boss_progression(self):


# def set_soul_shards_endgame_rule(self):
#     """Requires all Soul Shard Pieces (configured via blood_sin_quantity) to win."""
#     total = self.options.blood_sin_quantity.value
#     set_rule(
#         self.get_entrance("The Atrium -> Dome"),
#         lambda state, n=total: state.has("Soul Shard", self.player, n),
#     )
