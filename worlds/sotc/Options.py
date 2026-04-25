import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions


class GoalOptions:
    KILL_ALL_COLOSSI = 1
    HUNT_ALL_LIZARDS = 2
    SOUL_SHARD_SEARCH = 3


class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""

    display_name = "Guaranteed Items"


class GoalOption(Choice):
    """Lets the user choose the completion goal
    Kill all Collosi - Beat every fight in the game
    Hunt All Lizards - Get Every Stamina Drop from the lizards (May Require LizardSanity? Not sure yet.)
    Soul Shard Search - Add a unique item to the pool to find and collect from locations"""

    display_name = "Completion Goal"
    default = GoalOptions.KILL_ALL_COLOSSI
    option_kill_all_colossi = GoalOptions.KILL_ALL_COLOSSI
    option_collect_all_lizards = GoalOptions.HUNT_ALL_LIZARDS
    option_soul_shard_search = GoalOptions.SOUL_SHARD_SEARCH


class ColossiQuantity(Range):
    """
    Number of Collosi you need to kill to open the goal. Bosses will be chosen at random based on how many you choose here
    """

    display_name = "Colossi in Game"
    range_start = 0
    range_end = 15
    default = 15


class LizardQuantity(Range):
    """
    If you've chosen Lizard hunt or, set the number of lizards you want to kill in the game.
    """

    display_name = "Lizard Quantity in locations"
    range_start = 0
    range_end = 74
    default = 70


class SoulShardQuantity(Range):
    """
    Soul Shards Available in a Soul Shard Game. You must have Soul Shard Search as your Goal
    """

    display_name = "Soul Shard Quantity"
    range_start = 1
    range_end = 50
    default = 8


class FruitSanityToggle(Toggle):
    """Fruits count as checks"""

    display_name = "FruitSanity"
    default = 1
    option_true = 1
    option_false = 0


class LizardSanityToggle(Toggle):
    """Lizards count as checks - REQUIRED FOR 'HUNT ALL LIZARDS'"""

    display_name = "LizardSanity"
    default = 1
    option_true = 1
    option_false = 0


class ShrineSanityToggle(Toggle):
    """Include interaction with all shrines as checks"""

    display_name = "ShrineSanity"
    default = 1
    option_true = 1
    option_false = 0


class GridSanityToggle(Toggle):
    """Include all accessable grid tiles on the map as a checks on entry into them"""

    display_name = "GridSanity"
    default = 1
    option_true = 1
    option_false = 0


class ClimbSanityToggle(Toggle):
    """Provide Checks for Time Spent Climbing"""

    display_name = "ClimbSanity"
    default = 1
    option_true = 1
    option_false = 0


class ClimbSanityRange(Range):
    """
    How much distance do you want to climb (ClimbSanity must be enabled)
    """

    display_name = "ClimbSanity Range in Meters"
    range_start = 1
    range_end = 5000
    default = 500


class ClimbSanityBreakPoints(Range):
    """
    How much distance do you want to climb for 1 check (ClimbSanity must be enabled)
    """

    display_name = "ClimbSanity Break Points"
    range_start = 1
    range_end = 5000
    default = 100


class AgroSanityToggle(Toggle):
    """Provide checks for time spent riding best girl"""

    display_name = "AgroSanity"
    default = 1
    option_true = 1
    option_false = 0


class AgroSanityRange(Range):
    """
    How much distance do you want to ride (AgroSanity must be enabled)
    """

    display_name = "AgroSanity Range in Meters"
    range_start = 1
    range_end = 50000
    default = 10000


class AgroSanityBreakPoints(Range):
    """
    How much distance do you want to ride for 1 check (AgroSanity must be enabled)
    """

    display_name = "AgroSanity Break Points"
    range_start = 1
    range_end = 50000
    default = 1000


class TrapToggle(Toggle):
    """
    Decides if you want traps in the pool or not. Traps include:
    Loose Reins: Fall off Agro if you happen to be on her
    Sweaty Palms: Slip from where you're climbing
    Tired: You move at a slower speed
    """

    display_name = "Trap Items"
    default = 1
    option_true = 1
    option_false = 0


class TrapPercentage(Range):
    """
    If Trap Toggle is on, decide how much of your junk item pool should be used for traps
    """

    display_name = "Trap Percentage in Pool"
    range_start = 1
    range_end = 100
    default = 5


class DeathLinkToggle(Toggle):
    """Sets if you want deathlink or not"""

    display_name = "Death Link"
    default = 0
    option_true = 1
    option_false = 0


@dataclass
class SotcOption(PerGameCommonOptions):
    goal: GoalOption
    colossi_quantity: ColossiQuantity
    soul_shard_quantity: SoulShardQuantity
    lizard_quantity: LizardQuantity
    fruitsanity: FruitSanityToggle
    lizardsanity: LizardSanityToggle
    shrinesanity: ShrineSanityToggle
    gridsanity: GridSanityToggle
    climbsanity: ClimbSanityToggle
    climbsanity_range: ClimbSanityRange
    climbsanity_break_points: ClimbSanityBreakPoints
    agrosanity: AgroSanityToggle
    agrosanity_range: AgroSanityRange
    agrosanity_break_points: AgroSanityBreakPoints
    trap_toggle: TrapToggle
    trap_percentage: TrapPercentage
    deathlink: DeathLink
    guaranteed_items: GuaranteedItemsOption
