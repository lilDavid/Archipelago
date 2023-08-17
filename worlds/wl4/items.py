from __future__ import annotations

from typing import Any, Iterable, NamedTuple, Tuple

from BaseClasses import Item
from BaseClasses import ItemClassification as IC

from .data import ap_id_offset
from .types import Box, ItemType, Passage


# Items are encoded as 8-bit numbers as follows:
#                   | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
# Jewel pieces:     | 0   0   0 |  passage  | qdrnt |
# CD:               | 0   0   1 |  passage  | level |
#
# Junk items:       | 0   1   0   0 |     type      |
# AP item:          | 1   1   1   1   0   0   0   0 |
#
# For jewel pieces:
#  - passage = 0-5 for entry/emerald/ruby/topaz/sapphire/golden
#  - qdrnt = quadrant, increasing counterclockwise from top left
#
# For CDs:
#  - passage = 0-5 same as jewel pieces, but only 1-4 has a CD
#  - level = increasing as the level goes deeper
#
# Type for junk items:
#  - 0 = Full health item
#  - 1 = Wario form trap
#  - 2 = Single heart recovery
#  - 3 = Single heart damage


def ap_id_from_wl4_data(data: ItemData):
    cat, itemid, _ = data
    if cat == ItemType.EVENT or itemid == None:
        return None
    if cat == ItemType.JEWEL:
        passage, quad = itemid
        return ap_id_offset | (passage << 2) | quad
    elif cat == ItemType.CD:
        passage, level = itemid
        return ap_id_offset | (1 << 5) | (passage << 2) | level
    elif cat == ItemType.ITEM:
        return ap_id_offset | (1 << 6) | itemid
    else:
        raise ValueError(f'Unexpected WL4 item type: {data[0]}')


def wl4_data_from_ap_id(ap_id) -> Tuple[str, ItemData]:
    val = ap_id - ap_id_offset
    if val >> 5 == 0:
        passage = (val & 0x1C) >> 2
        quad = val & 3
        return tuple(filter(lambda d: d[0] == quad and d[1] == passage, item_table.items()))
    elif val >> 5 == 1:
        passage = (val & 0x1C) >> 2
        level = val & 3
        return tuple(filter(lambda d: d[0] == ItemType.CD and d[1] == (passage, level), item_table.items()))
    elif val >> 4 == 4:
        item = val & 0xF
        return tuple(filter(lambda d: d[0] == ItemType.ITEM and d[1] == item, item_table.items()))
    else:
        raise ValueError(f'Could not find WL4 item ID: {ap_id}')


class WL4Item(Item):
    game: str = 'Wario Land 4'
    type: ItemType

    def __init__(self, name, player, data, force_non_progression):
        type, id, prog = data
        if force_non_progression:
            prog = IC.filler
        super(WL4Item, self).__init__(name, prog, ap_id_from_wl4_data(data), player)
        self.type = type
        if type in (ItemType.JEWEL, ItemType.CD):
            self.passage, self.level = id
        else:
            self.passage = self.level = None


class ItemData(NamedTuple):
    type: ItemType
    id: Any
    prog: IC

    def passage(self):
        return self.id[0]

    def box(self):
        if self.type == ItemType.CD:
            return Box.CD
        else:
            return self.id[1]


item_table = {
    # Item name                                  Item type        ID                                 Progression
    'Top Right Entry Jewel Piece':      ItemData(ItemType.JEWEL, (Passage.ENTRY,    Box.JEWEL_NE),  IC.progression),
    'Top Right Emerald Piece':          ItemData(ItemType.JEWEL, (Passage.EMERALD,  Box.JEWEL_NE),  IC.progression),
    'Top Right Ruby Piece':             ItemData(ItemType.JEWEL, (Passage.RUBY,     Box.JEWEL_NE),  IC.progression),
    'Top Right Topaz Piece':            ItemData(ItemType.JEWEL, (Passage.TOPAZ,    Box.JEWEL_NE),  IC.progression),
    'Top Right Sapphire Piece':         ItemData(ItemType.JEWEL, (Passage.SAPPHIRE, Box.JEWEL_NE),  IC.progression),
    'Top Right Golden Jewel Piece':     ItemData(ItemType.JEWEL, (Passage.GOLDEN,   Box.JEWEL_NE),  IC.progression),
    'Bottom Right Entry Jewel Piece':   ItemData(ItemType.JEWEL, (Passage.ENTRY,    Box.JEWEL_SE),  IC.progression),
    'Bottom Right Emerald Piece':       ItemData(ItemType.JEWEL, (Passage.EMERALD,  Box.JEWEL_SE),  IC.progression),
    'Bottom Right Ruby Piece':          ItemData(ItemType.JEWEL, (Passage.RUBY,     Box.JEWEL_SE),  IC.progression),
    'Bottom Right Topaz Piece':         ItemData(ItemType.JEWEL, (Passage.TOPAZ,    Box.JEWEL_SE),  IC.progression),
    'Bottom Right Sapphire Piece':      ItemData(ItemType.JEWEL, (Passage.SAPPHIRE, Box.JEWEL_SE),  IC.progression),
    'Bottom Right Golden Jewel Piece':  ItemData(ItemType.JEWEL, (Passage.GOLDEN,   Box.JEWEL_SE),  IC.progression),
    'Bottom Left Entry Jewel Piece':    ItemData(ItemType.JEWEL, (Passage.ENTRY,    Box.JEWEL_SW),  IC.progression),
    'Bottom Left Emerald Piece':        ItemData(ItemType.JEWEL, (Passage.EMERALD,  Box.JEWEL_SW),  IC.progression),
    'Bottom Left Ruby Piece':           ItemData(ItemType.JEWEL, (Passage.RUBY,     Box.JEWEL_SW),  IC.progression),
    'Bottom Left Topaz Piece':          ItemData(ItemType.JEWEL, (Passage.TOPAZ,    Box.JEWEL_SW),  IC.progression),
    'Bottom Left Sapphire Piece':       ItemData(ItemType.JEWEL, (Passage.SAPPHIRE, Box.JEWEL_SW),  IC.progression),
    'Bottom Left Golden Jewel Piece':   ItemData(ItemType.JEWEL, (Passage.GOLDEN,   Box.JEWEL_SW),  IC.progression),
    'Top Left Entry Jewel Piece':       ItemData(ItemType.JEWEL, (Passage.ENTRY,    Box.JEWEL_NW),  IC.progression),
    'Top Left Emerald Piece':           ItemData(ItemType.JEWEL, (Passage.EMERALD,  Box.JEWEL_NW),  IC.progression),
    'Top Left Ruby Piece':              ItemData(ItemType.JEWEL, (Passage.RUBY,     Box.JEWEL_NW),  IC.progression),
    'Top Left Topaz Piece':             ItemData(ItemType.JEWEL, (Passage.TOPAZ,    Box.JEWEL_NW),  IC.progression),
    'Top Left Sapphire Piece':          ItemData(ItemType.JEWEL, (Passage.SAPPHIRE, Box.JEWEL_NW),  IC.progression),
    'Top Left Golden Jewel Piece':      ItemData(ItemType.JEWEL, (Passage.GOLDEN,   Box.JEWEL_NW),  IC.progression),
    'About that Shepherd CD':           ItemData(ItemType.CD,    (Passage.EMERALD,  0),             IC.filler),
    'Things that Never Change CD':      ItemData(ItemType.CD,    (Passage.EMERALD,  1),             IC.filler),
    "Tomorrow's Blood Pressure CD":     ItemData(ItemType.CD,    (Passage.EMERALD,  2),             IC.filler),
    'Beyond the Headrush CD':           ItemData(ItemType.CD,    (Passage.EMERALD,  3),             IC.filler),
    'Driftwood & the Island Dog CD':    ItemData(ItemType.CD,    (Passage.RUBY,     0),             IC.filler),
    "The Judge's Feet CD":              ItemData(ItemType.CD,    (Passage.RUBY,     1),             IC.filler),
    "The Moon's Lamppost CD":           ItemData(ItemType.CD,    (Passage.RUBY,     2),             IC.filler),
    'Soft Shell CD':                    ItemData(ItemType.CD,    (Passage.RUBY,     3),             IC.filler),
    'So Sleepy CD':                     ItemData(ItemType.CD,    (Passage.TOPAZ,    0),             IC.filler),
    'The Short Futon CD':               ItemData(ItemType.CD,    (Passage.TOPAZ,    1),             IC.filler),
    'Avocado Song CD':                  ItemData(ItemType.CD,    (Passage.TOPAZ,    2),             IC.filler),
    'Mr. Fly CD':                       ItemData(ItemType.CD,    (Passage.TOPAZ,    3),             IC.filler),
    "Yesterday's Words CD":             ItemData(ItemType.CD,    (Passage.SAPPHIRE, 0),             IC.filler),
    'The Errand CD':                    ItemData(ItemType.CD,    (Passage.SAPPHIRE, 1),             IC.filler),
    'You and Your Shoes CD':            ItemData(ItemType.CD,    (Passage.SAPPHIRE, 2),             IC.filler),
    'Mr. Ether & Planaria CD':          ItemData(ItemType.CD,    (Passage.SAPPHIRE, 3),             IC.filler),
    'Full Health Item':                 ItemData(ItemType.ITEM,  0x40,                              IC.useful),
    'Wario Form Trap':                  ItemData(ItemType.ITEM,  0x41,                              IC.trap),
    'Heart':                            ItemData(ItemType.ITEM,  0x42,                              IC.filler),
    'Lightning Trap':                   ItemData(ItemType.ITEM,  0x43,                              IC.trap),
    'Entry Passage Clear':              ItemData(ItemType.EVENT, None,                              IC.progression),
    'Emerald Passage Clear':            ItemData(ItemType.EVENT, None,                              IC.progression),
    'Ruby Passage Clear':               ItemData(ItemType.EVENT, None,                              IC.progression),
    'Topaz Passage Clear':              ItemData(ItemType.EVENT, None,                              IC.progression),
    'Sapphire Passage Clear':           ItemData(ItemType.EVENT, None,                              IC.progression),
    'Escape the Pyramid':               ItemData(ItemType.EVENT, None,                              IC.progression),
}


def filter_items(*, type: ItemType = None, passage: Passage = None) -> Iterable[Tuple[str, ItemData]]:
    items = item_table.items()
    if type != None:
        items = filter(lambda i: i[1].type == type, items)
    if passage != None:
        items = filter(lambda i: i[1].passage() == passage, items)
    return items


def filter_item_names(*, type: ItemType = None, passage: Passage = None) -> Iterable[str]:
    return map(lambda entry: entry[0], filter_items(type=type, passage=passage))