import typing

from BaseClasses import MultiWorld, Region, Entrance

from .Locations import WarioLand4Location
from .Locations import all_locations
from .Names import LocationName
from .Names import ItemName


def create_regions(world: MultiWorld, player: int):
    menu_region = create_region(world, player, "Menu")
    map_region = create_region(world, player, LocationName.map)

    entry_passage = create_region(world, player, LocationName.entry_passage)
    hall_of_hieroglyphs = create_region(
        world,
        player,
        LocationName.hall_of_hieroglyphs.name,
        [*LocationName.hall_of_hieroglyphs.jewels, LocationName.hall_of_hieroglyphs.fullhealth],
    )
    spoiled_rotten = create_region(
        world,
        player,
        LocationName.spoiled_rotten.name,
        (LocationName.spoiled_rotten.defeat(),),
    )

    emerald_passage = create_region(world, player, LocationName.emerald_passage)
    palm_tree_paradise = create_region(
        world,
        player,
        LocationName.palm_tree_paradise.name,
        LocationName.palm_tree_paradise.default_locations(),
    )
    wildflower_fields = create_region(
        world,
        player,
        LocationName.wildflower_fields.name,
        LocationName.wildflower_fields.default_locations(),
    )
    mystic_lake = create_region(
        world,
        player,
        LocationName.mystic_lake.name,
        LocationName.mystic_lake.default_locations(),
    )
    monsoon_jungle = create_region(
        world,
        player,
        LocationName.monsoon_jungle.name,
        LocationName.monsoon_jungle.default_locations(),
    )
    cractus = create_region(
        world,
        player,
        LocationName.cractus.name,
        (LocationName.cractus.defeat(),),
    )

    ruby_passage = create_region(world, player, LocationName.ruby_passage)
    curious_factory = create_region(
        world,
        player,
        LocationName.curious_factory.name,
        LocationName.curious_factory.default_locations(),
    )
    toxic_landfill = create_region(
        world,
        player,
        LocationName.toxic_landfill.name,
        LocationName.toxic_landfill.default_locations(),
    )
    forty_below_fridge = create_region(
        world,
        player,
        LocationName.forty_below_fridge.name,
        LocationName.forty_below_fridge.default_locations(),
    )
    pinball_zone = create_region(
        world,
        player,
        LocationName.pinball_zone.name,
        LocationName.pinball_zone.default_locations(),
    )
    cuckoo_condor = create_region(
        world,
        player,
        LocationName.cuckoo_condor.name,
        (LocationName.cuckoo_condor.defeat(),),
    )

    topaz_passage = create_region(world, player, LocationName.topaz_passage)
    toy_block_tower = create_region(
        world,
        player,
        LocationName.toy_block_tower.name,
        LocationName.toy_block_tower.default_locations(),
    )
    big_board = create_region(
        world,
        player,
        LocationName.big_board.name,
        LocationName.big_board.default_locations(),
    )
    doodle_woods = create_region(
        world,
        player,
        LocationName.doodle_woods.name,
        LocationName.doodle_woods.default_locations(),
    )
    domino_row = create_region(
        world,
        player,
        LocationName.domino_row.name,
        LocationName.domino_row.default_locations(),
    )
    aerodent = create_region(
        world,
        player,
        LocationName.aerodent.name,
        (LocationName.aerodent.defeat(),),
    )

    sapphire_passage = create_region(world, player, LocationName.sapphire_passage)
    crescent_moon_village = create_region(
        world,
        player,
        LocationName.crescent_moon_village.name,
        LocationName.crescent_moon_village.default_locations(),
    )
    arabian_night = create_region(
        world,
        player,
        LocationName.arabian_night.name,
        LocationName.arabian_night.default_locations(),
    )
    fiery_cavern = create_region(
        world,
        player,
        LocationName.fiery_cavern.name,
        LocationName.fiery_cavern.default_locations(),
    )
    hotel_horror = create_region(
        world,
        player,
        LocationName.hotel_horror.name,
        LocationName.hotel_horror.default_locations(),
    )
    catbat = create_region(
        world,
        player,
        LocationName.catbat.name,
        (LocationName.catbat.defeat(),),
    )

    golden_pyramid = create_region(world, player, LocationName.golden_pyramid)
    golden_passage = create_region(
        world,
        player,
        LocationName.golden_passage.name,
        LocationName.golden_passage.jewels,
    )
    golden_diva = create_region(
        world,
        player,
        LocationName.golden_diva.name,
        (LocationName.golden_diva.defeat(),),
    )

    world.regions += [
        menu_region,
        map_region,
        entry_passage,
        hall_of_hieroglyphs,
        spoiled_rotten,
        emerald_passage,
        palm_tree_paradise,
        wildflower_fields,
        mystic_lake,
        monsoon_jungle,
        cractus,
        ruby_passage,
        curious_factory,
        toxic_landfill,
        forty_below_fridge,
        pinball_zone,
        cuckoo_condor,
        topaz_passage,
        toy_block_tower,
        big_board,
        doodle_woods,
        domino_row,
        aerodent,
        sapphire_passage,
        crescent_moon_village,
        arabian_night,
        fiery_cavern,
        hotel_horror,
        catbat,
        golden_pyramid,
        golden_passage,
        golden_diva,
    ]


def connect_regions(world, player):
    names: typing.Dict[str, int] = {}

    connect(world, player, names, "Menu", LocationName.entry_passage)
    connect(world, player, names, LocationName.entry_passage, LocationName.hall_of_hieroglyphs.name)
    connect(world, player, names, LocationName.hall_of_hieroglyphs.name, LocationName.spoiled_rotten.name,
        lambda state: all(state.has(piece, player) for piece in ItemName.entry_passage_jewel))
    connect(world, player, names, LocationName.spoiled_rotten.name, LocationName.map)

    connect(world, player, names, LocationName.map, LocationName.emerald_passage)
    connect(world, player, names, LocationName.emerald_passage, LocationName.palm_tree_paradise.name)
    connect(world, player, names, LocationName.palm_tree_paradise.name, LocationName.wildflower_fields.name)
    connect(world, player, names, LocationName.wildflower_fields.name, LocationName.mystic_lake.name)
    connect(world, player, names, LocationName.mystic_lake.name, LocationName.monsoon_jungle.name)
    connect(world, player, names, LocationName.monsoon_jungle.name, LocationName.cractus.name,
        lambda state: all(state.has(piece, player, 4) for piece in ItemName.emerald_passage_jewel))

    connect(world, player, names, LocationName.map, LocationName.ruby_passage)
    connect(world, player, names, LocationName.ruby_passage, LocationName.curious_factory.name)
    connect(world, player, names, LocationName.curious_factory.name, LocationName.toxic_landfill.name)
    connect(world, player, names, LocationName.toxic_landfill.name, LocationName.forty_below_fridge.name)
    connect(world, player, names, LocationName.forty_below_fridge.name, LocationName.pinball_zone.name)
    connect(world, player, names, LocationName.pinball_zone.name, LocationName.cuckoo_condor.name,
        lambda state: all(state.has(piece, player, 4) for piece in ItemName.ruby_passage_jewel))

    connect(world, player, names, LocationName.map, LocationName.topaz_passage)
    connect(world, player, names, LocationName.topaz_passage, LocationName.toy_block_tower.name)
    connect(world, player, names, LocationName.toy_block_tower.name, LocationName.big_board.name)
    connect(world, player, names, LocationName.big_board.name, LocationName.doodle_woods.name)
    connect(world, player, names, LocationName.doodle_woods.name, LocationName.domino_row.name)
    connect(world, player, names, LocationName.domino_row.name, LocationName.aerodent.name,
        lambda state: all(state.has(piece, player, 4) for piece in ItemName.topaz_passage_jewel))

    connect(world, player, names, LocationName.map, LocationName.sapphire_passage)
    connect(world, player, names, LocationName.sapphire_passage, LocationName.crescent_moon_village.name)
    connect(world, player, names, LocationName.crescent_moon_village.name, LocationName.arabian_night.name)
    connect(world, player, names, LocationName.arabian_night.name, LocationName.fiery_cavern.name)
    connect(world, player, names, LocationName.fiery_cavern.name, LocationName.hotel_horror.name)
    connect(world, player, names, LocationName.hotel_horror.name, LocationName.catbat.name,
        lambda state: all(state.has(piece, player, 4) for piece in ItemName.sapphire_passage_jewel))

    connect(world, player, names, LocationName.map, LocationName.golden_pyramid,
        lambda state: (state.has(ItemName.defeated_boss, player, 5)))
    connect(world, player, names, LocationName.golden_pyramid, LocationName.golden_passage.name)
    connect(world, player, names, LocationName.golden_passage.name, LocationName.golden_diva.name,
        lambda state: all(state.has(piece, player) for piece in ItemName.golden_pyramid_jewel))


def create_region(
    world: MultiWorld, player: int, name: str, locations: typing.Sequence[str] = ()
):
    region = Region(name, player, world)
    for location in locations:
        id = all_locations[location]
        region.locations.append(WarioLand4Location(player, location, id, region))
    return region


def connect(
    world: MultiWorld,
    player: int,
    used_names: typing.Dict[str, int],
    source: str,
    target: str,
    rule: typing.Optional[typing.Callable] = None,
):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])
    
    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule
    
    source_region.exits.append(connection)
    connection.connect(target_region)
