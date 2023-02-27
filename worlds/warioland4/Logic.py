from worlds.AutoWorld import LogicMixin

from .Names import JewelPieces

class WarioLand4Logic(LogicMixin):
	def wl4_has_full_jewels(self, player: int, jewel: JewelPieces, count: int):
		return all(self.has(piece, player, count) for piece in jewel)
