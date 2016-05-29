import struct

from .basic import *

__all__ = ["Pokemon"]

class PokemonGenI(PokeStructure):

	"""Pokemon data structure of Generation I according to
    http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_in_Generation_I"""

	_fields_ = [
			("species", ctypes.c_uint8),
			("hp", ctypes.c_uint16),
			("level0", ctypes.c_uint8),
			("status", ctypes.c_uint8),
			("type1", ctypes.c_uint8),
			("type2", ctypes.c_uint8),
			("catch_rate", ctypes.c_uint8),
			("move1", ctypes.c_uint8),
			("move2", ctypes.c_uint8),
			("move3", ctypes.c_uint8),
			("move4", ctypes.c_uint8),
			("original_trainer", ctypes.c_uint16),
			("_xp", Pokearray(3)),
			("hp_ev", ctypes.c_uint16),
			("attack_ev", ctypes.c_uint16),
			("defense_ev", ctypes.c_uint16),
			("speed_ev", ctypes.c_uint16),
			("special_ev", ctypes.c_uint16),
			("iv", ctypes.c_uint16),
			("move1_pp", ctypes.c_uint8),
			("move2_pp", ctypes.c_uint8),
			("move3_pp", ctypes.c_uint8),
			("move4_pp", ctypes.c_uint8),
			("level", ctypes.c_uint8),
			("max_hp", ctypes.c_uint16),
			("attack", ctypes.c_uint16),
			("defense", ctypes.c_uint16),
			("speed", ctypes.c_uint16),
			("special", ctypes.c_uint16)
		]

	@property
	def xp(self):
		return struct.unpack(">I", b'\0' + self._xp.bytes())[0]

	@xp.setter
	def xp(self, value):
		self._xp = Pokearray(3).fromBytes(struct.pack(">I", value)[1:])

Pokemon = PokemonGenI
