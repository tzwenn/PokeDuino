from .basic import *
from .pokemon import Pokemon
from .teamlist import TeamList
from .item import ItemList

__all__ = ["GameSave"]

PokemonBox = Pokearray(1122)

class GameSaveGenI(PokeStructure):

	"""Pokemon game save structure as Generation I according to
	http://bulbapedia.bulbagarden.net/wiki/Save_data_structure_in_Generation_I#Pok.C3.A9mon_lists"""

	_fields_ = [
				PaddingBytes(0x2598),
			("player_name", Pokestring(11)),
			("pokedex_owned", Pokearray(19)),
			("pokedex_seen", Pokearray(19)),
			("pocket_item_list", ItemList(20)),
			("money", Pokearray(3)),
			("rival_name", Pokestring(11)),
			("options", ctypes.c_uint8),
			("badges", ctypes.c_uint8),
				PaddingBytes(2),
			("player_id", ctypes.c_uint16),
				PaddingBytes(277),
			("pikachu_friendship", ctypes.c_uint8),
				PaddingBytes(201),
			("pc_item_list", ItemList(50)),
			("current_pc_box", ctypes.c_uint8),
				PaddingBytes(3),
			("casino_coins", ctypes.c_uint16),
				PaddingBytes(1180),
			("time_played", ctypes.c_uint32),
				PaddingBytes(570),
			("team", TeamList),
			("current_box", PokemonBox),
				PaddingBytes(1),
			("checksum", ctypes.c_uint8),
				PaddingBytes(2780),
			("pc_box_1", PokemonBox),
			("pc_box_2", PokemonBox),
			("pc_box_3", PokemonBox),
			("pc_box_4", PokemonBox),
			("pc_box_5", PokemonBox),
			("pc_box_6", PokemonBox),
				PaddingBytes(1460),
			("pc_box_7", PokemonBox),
			("pc_box_8", PokemonBox),
			("pc_box_9", PokemonBox),
			("pc_box_10", PokemonBox),
			("pc_box_11", PokemonBox),
			("pc_box_12", PokemonBox),
				PaddingBytes(1460)
		]

	def _calcChecksum(self):
		sum = 0
		for b in PokeStructure.bytes(self)[0x2598:0x3522 + 1]:
			sum += b
			sum &= 0xFF
		return ~sum & 0xFF

	def bytes(self):
		self.checksum = self._calcChecksum()
		return PokeStructure.bytes(self)

	def save(self, fileName):
		open(fileName, "wb").write(self.bytes())

GameSave = GameSaveGenI

