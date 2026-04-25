from rule_builder.rules import Has, HasAll, HasAllCounts, CanReachLocation, CanReachRegion
from rule_builder.field_resolvers import FromOption
from .Options import SoulShardQuantity
from .Locations import location_tables, SotcLocationCategory


def kill_all_colossi():
    return CanReachRegion("Game Clear")


def collect_all_shards():
    return HasAllCounts({"Soul Shard": FromOption(SoulShardQuantity)})


def hunt_all_lizards(lizard_max_count):
    return Has("Lizard Tail", int(lizard_max_count))
