from rule_builder.rules import Has, HasAll, HasAllCounts, CanReachLocation
from rule_builder.field_resolvers import FromOption
from .Options import SoulShardQuantity


def kill_all_colossi():
    return CanReachLocation("Game End: Credits")


def collect_all_shards():
    return HasAllCounts({"Soul Shard": FromOption(SoulShardQuantity)})


def collect_all_lizards():
    return HasAllCounts({"Soul Shard": FromOption(SoulShardQuantity)})
