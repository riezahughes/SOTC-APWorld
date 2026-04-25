from rule_builder.rules import Has, HasAll, HasAllCounts, CanReachLocation, CanReachRegion
from rule_builder.field_resolvers import FromOption
from .Options import SoulShardQuantity
from .Locations import location_tables, SotcLocationCategory


def kill_all_colossi():
    return CanReachRegion("Game Clear")


def collect_all_shards():
    return HasAllCounts({"Soul Shard": FromOption(SoulShardQuantity)})


def hunt_all_lizards():
    lizard_count = sum(1 for region_locs in location_tables.values() for loc in region_locs if loc.category == SotcLocationCategory.LIZARD)
    return Has("Lizard Tail", lizard_count)
