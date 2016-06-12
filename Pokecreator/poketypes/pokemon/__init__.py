import struct
import math

from ..basic import *
from .species import Species
from .moves import Move
from .types import Type
from .status import StatusField

from . import experience
from . import basestats
from . import moves

__all__ = ["Pokemon"]

class IV(object):

	"""Individual values (read-only) according to
	http://bulbapedia.bulbagarden.net/wiki/Individual_values#Generation_I_and_II"""

	def __init__(self, uint16):
		self._attack  = (uint16 >> 12) & 0xF
		self._defense = (uint16 >>  8) & 0xF
		self._speed   = (uint16 >>  4) & 0xF
		self._special =  uint16        & 0xF
		self._hp = (self.attack & 1) << 3 | (self.defense & 1) << 2 | (self.speed & 1) << 1 | (self.special & 1)

	@property
	def attack(self):
		return self._attack

	@property
	def defense(self):
		return self._defense

	@property
	def speed(self):
		return self._speed

	@property
	def special(self):
		return self._special

	@property
	def hp(self):
		return self._hp

	@property
	def value(self):
		return self.attack << 12 | self.defense << 8 | self.speed << 4 | self.special

	def __str__(self):
		return "%s(attack: %d, defense: %d, speed: %d, special: %d, hp: %d)" % \
			(self.__class__.__name__, self.attack, self.defense, self.speed, self.special, self.hp)

class PP(PokeStructure):

	_fields_ = [
		("up", ctypes.c_uint8, 2),
		("pp", ctypes.c_uint8, 6)
	]

class PokemonGenI(PokeStructure):

	"""Pokemon data structure of Generation I according to
    http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_in_Generation_I"""

	_fields_ = [
			("_species", ctypes.c_uint8),
			("hp", ctypes.c_uint16),
			("level0", ctypes.c_uint8),
			("_status", ctypes.c_uint8),
			("_type1", ctypes.c_uint8),
			("_type2", ctypes.c_uint8),
			("catch_rate", ctypes.c_uint8),
			("_move1", ctypes.c_uint8),
			("_move2", ctypes.c_uint8),
			("_move3", ctypes.c_uint8),
			("_move4", ctypes.c_uint8),
			("original_trainer", ctypes.c_uint16),
			("_xp", Pokearray(3)),
			("hp_ev", ctypes.c_uint16),
			("attack_ev", ctypes.c_uint16),
			("defense_ev", ctypes.c_uint16),
			("speed_ev", ctypes.c_uint16),
			("special_ev", ctypes.c_uint16),
			("_iv", ctypes.c_uint16),
			("move1_pp", PP),
			("move2_pp", PP),
			("move3_pp", PP),
			("move4_pp", PP),
			("level", ctypes.c_uint8),
			("max_hp", ctypes.c_uint16),
			("attack", ctypes.c_uint16),
			("defense", ctypes.c_uint16),
			("speed", ctypes.c_uint16),
			("special", ctypes.c_uint16)
		]

	_adapters_ = [
			("_species", Species),
			("_status", StatusField),
			("_type1", Type),
			("_type2", Type),
			("_move1", Move),
			("_move2", Move),
			("_move3", Move),
			("_move4", Move),
			("_iv", IV)
		]

	@property
	def xp(self):
		return struct.unpack(">I", b'\0' + self._xp.bytes())[0]

	@xp.setter
	def xp(self, value):
		self._xp = Pokearray(3).fromBytes(struct.pack(">I", value)[1:])

	####################

	def __repr__(self):
		return "%s.%s(species=%s, level=%d)" % (__name__, self.__class__.__name__, self.species, self.level)

	####################

	@property
	def basestats(self):
		return basestats.basestats_from_species[self.species]

	def _calc_stat_main_term(self, base, iv, ev):
		return int(((base + iv) * 2 + int(math.sqrt(ev) / 4)) * self.level / 100.0)

	def _calc_hp(self):
		return self._calc_stat_main_term(self.basestats.hp, self.iv.hp, self.hp_ev) + self.level + 10

	def _calc_stat(self, stat_name):
		return self._calc_stat_main_term(getattr(self.basestats, stat_name), getattr(self.iv, stat_name), getattr(self, stat_name + "_ev")) + 5

	####################

	def sanitize_xp(self):
		"""Adjust xp according to level"""
		xpClass = experience.class_for_species[self.species]
		if self.level != experience.level_for_exp[xpClass](self.xp):
			self.xp = experience.exp_for_level[xpClass](self.level)

	def sanitize_types(self):
		self.type1, self.type2 = types.type_for_species[self.species]

	def sanitize_hp(self):
		self.max_hp = self._calc_hp()
		self.hp = min(self.hp, self.max_hp)

	def sanitize_stats(self):
		self.attack = self._calc_stat("attack")
		self.defense = self._calc_stat("defense")
		self.speed = self._calc_stat("speed")
		self.special = self._calc_stat("special")

	def sanitize_pp(self):
		self.move1_pp.pp = moves.pp_for_move[self.move1]
		self.move2_pp.pp = moves.pp_for_move[self.move2]
		self.move3_pp.pp = moves.pp_for_move[self.move3]
		self.move4_pp.pp = moves.pp_for_move[self.move4]

	def sanitize(self):
		"""Adjust xp, types, hp, stats, pp to the values the game
		   had calculated from species, level and moves"""
		self.sanitize_xp()
		self.sanitize_types()
		self.sanitize_hp()
		self.sanitize_stats()
		self.sanitize_pp()
		self.level0 = self.level

	def heal(self):
		"""Pokecenter! (and sanitize)"""
		self.sanitize()
		self.hp = self.max_hp
		self.status = 0

		

Pokemon = PokemonGenI
