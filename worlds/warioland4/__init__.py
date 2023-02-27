import typing

from BaseClasses import Item, ItemClassification

from .Items import WarioLand4Item, item_table
from .Options import wario_land_4_options
from .Regions import connect_regions, create_regions
from .Locations import all_locations, setup_locations
from .Names import ItemName, LocationName
from worlds.AutoWorld import WebWorld, World


class WarioLand4World(World):
    game: str = "Wario Land 4"
    option_definitions = wario_land_4_options
    topology_present = True

    data_version = 0

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    def generate_basic(self) -> None:
        itempool: typing.List[WarioLand4Item] = []

        connect_regions(self.multiworld, self.player)

        #print(self.multiworld.get_locations())

        diamond_pieces = 18 * 4
        cds = 16
        full_health_items = 17
        total_required_locations = diamond_pieces + cds + full_health_items

        for item, data in Items.box_table.items():
            for _ in range(data.quantity):
                itempool.append(self.create_item(item))

        junk_count = total_required_locations - len(itempool)
        assert junk_count == 0, f"Mismatch location counts: {junk_count} empty checks"

        self.multiworld.get_location(
            LocationName.golden_diva.defeat(), self.player
        ).place_locked_item(self.create_event(ItemName.victory))

        boss_location_names = [
            LocationName.spoiled_rotten.defeat(),
            LocationName.cractus.defeat(),
            LocationName.cuckoo_condor.defeat(),
            LocationName.aerodent.defeat(),
            LocationName.catbat.defeat(),
        ]
        for location_name in boss_location_names:
            self.multiworld.get_location(location_name, self.player).place_locked_item(
                self.create_event(ItemName.defeated_boss)
            )

        self.multiworld.itempool += itempool
    
    def generate_output(self, output_directory: str):
        # TODO
        ...

    def create_regions(self):
        location_table = setup_locations(self.multiworld, self.player)
        create_regions(self.multiworld, self.player)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = WarioLand4Item(name, classification, data.code, self.player)

        return created_item
    
    def create_event(self, name: str):
        return WarioLand4Item(name, ItemClassification.progression, None, self.player)
