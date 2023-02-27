import typing
import string

from . import JewelPieces


name_format = string.Template("$item ($location)")


class Level(typing.NamedTuple):
    keyzer: str
    cd: typing.Optional[str]

    @classmethod
    def named(cls, name, cd_title=None):
        return Level(
            name_format.substitute(item="Keyzer", location=name),
            name_format.substitute(item="CD", location=cd_title),
        )


def jewel_pieces(passage: str) -> JewelPieces:
	return JewelPieces(
		*(
			name_format.substitute(item=f"{j} Jewel Piece", location=passage)
			for j in JewelPieces.locations
		)
	)


# Entry Passage
hall_of_hieroglyphs = Level.named("Hall of Heiroglyphs")

# Emerald Passage
palm_tree_paradise = Level.named("Palm Tree Paradise", "About that Shepherd")
wildflower_fields = Level.named("Wildflower Fields", "Things That Never Change")
mystic_lake = Level.named("Mystic Lake", "Tomorrow's Blood Pressure")
monsoon_jungle = Level.named("Monsoon Jungle", "Beyond the Headrush")

# Ruby Passage
curious_factory = Level.named("The Curious Factory", "Driftwood & the Island Dog")
toxic_landfill = Level.named("The Toxic Landfill", "The Judge's Feet")
forty_below_fridge = Level.named("40 Below Fridge", "The Moon's Lamppost")
pinball_zone = Level.named("Pinball Zone", "Soft Shell")

# Topaz Passage
toy_block_tower = Level.named("Toy Block Tower", "So Sleepy")
big_board = Level.named("The Big Board", "The Short Futon")
doodle_woods = Level.named("Doodle Woods", "Avocado Song")
domino_row = Level.named("Dominow Row", "Mr. Fly")

# Sapphire Passage
crescent_moon_village = Level.named("Crescent Moon Village", "Yesterday's Words")
arabian_night = Level.named("Arabian Night", "The Errand")
fiery_cavern = Level.named("Fiery Cavern", "You and Your Shoes")
hotel_horror = Level.named("Hotel Horror", "Mr. Ether & Planaria")

# Golden Pyramid
golden_passage = Level.named("Golden Passage")

# Jewel Pieces
entry_passage_jewel = jewel_pieces("Entry Passage")
emerald_passage_jewel = jewel_pieces("Emerald Passage")
ruby_passage_jewel = jewel_pieces("Ruby Passage")
topaz_passage_jewel = jewel_pieces("Topaz Passage")
sapphire_passage_jewel = jewel_pieces("Sapphire Passage")
golden_pyramid_jewel = jewel_pieces("Golden Pyramid")

# Junk/traps from The Big Board
health = "Heart"
wario_form = "Status Trap"
lightning = "Lightning Trap"

# Other items
defeated_boss = "Defeated Boss"
full_health = "Full Health Item"
victory = "Defeated Golden Diva"
