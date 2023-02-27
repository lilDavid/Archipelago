import typing
import string

from . import JewelPieces


name_format = string.Template("$level $check")
boss_format = string.Template("Defeat $boss")


class Boss(typing.NamedTuple):
    name: str

    def defeat(self):
        return boss_format.substitute(boss=self.name)


class Level(typing.NamedTuple):
    name: str
    jewels: JewelPieces
    keyzer: str
    cd_box: str
    fullhealth: str

    @classmethod
    def named(cls, name):
        return Level(
            name,
            JewelPieces(
                *(
                    name_format.substitute(level=name, check=f"Jewel Piece Box ({j})")
                    for j in JewelPieces.locations
                )
            ),
            name_format.substitute(level=name, check="Keyzer"),
            name_format.substitute(level=name, check="CD Box"),
            name_format.substitute(level=name, check="Full Health Item Box"),
        )
    
    def default_locations(self):
        return [*self.jewels, self.cd_box, self.fullhealth]


map = "Pyramid map"

# Entry Passage
entry_passage = "Entry Passage"
hall_of_hieroglyphs = Level.named("Hall of Heiroglyphs")
spoiled_rotten = Boss("Spoiled Rotten")

# Emerald Passage
emerald_passage = "Emerald Passage"
palm_tree_paradise = Level.named("Palm Tree Paradise")
wildflower_fields = Level.named("Wildflower Fields")
mystic_lake = Level.named("Mystic Lake")
monsoon_jungle = Level.named("Monsoon Jungle")
cractus = Boss("Cractus")

# Ruby Passage
ruby_passage = "Ruby Passage"
curious_factory = Level.named("The Curious Factory")
toxic_landfill = Level.named("The Toxic Landfill")
forty_below_fridge = Level.named("40 Below Fridge")
pinball_zone = Level.named("Pinball Zone")
cuckoo_condor = Boss("Cuckoo Condor")

# Topaz Passage
topaz_passage = "Topaz Passage"
toy_block_tower = Level.named("Toy Block Tower")
big_board = Level.named("The Big Board")
doodle_woods = Level.named("Doodle Woods")
domino_row = Level.named("Dominow Row")
aerodent = Boss("Aerodent")

# Sapphire Passage
sapphire_passage = "Sapphire Passage"
crescent_moon_village = Level.named("Crescent Moon Village")
arabian_night = Level.named("Arabian Night")
fiery_cavern = Level.named("Fiery Cavern")
hotel_horror = Level.named("Hotel Horror")
catbat = Boss("Catbat")

# Golden Pyramid
golden_pyramid = "Golden Pyramid"
golden_passage = Level.named("Golden Passage")
golden_diva = Boss("Golden Diva")
