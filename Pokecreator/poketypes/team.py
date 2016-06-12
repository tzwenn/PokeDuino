from .basic import *
from .pokemon import Pokemon

__all__ = ["Team"]

class Team(PokeStructure):

	TERMINATOR = 0xFF

	_fields_ = [
			("entries_used", ctypes.c_uint8),
			("species_list", Pokearray(7)),
			("pokemon_list", Pokemon * 6),
			("ot_names", Pokestring(11) * 6),
			("pokemon_names", Pokestring(11) * 6)
		]

	def nickname_at(self, index):
		"""Returns nickname of pokemon at given index, or None if it hasn't any"""
		name = self.pokemon_names[index].toString()
		# FIXME: Properly handle localization
		if name != self.pokemon_list[index].species.name.upper():
			return name
		return None # No nickname

	def __iter__(self):
		return (self[i] for i in range(self.entries_used))

	def add(self, pokemon, ot_name, nickname=None):
		if self.entries_used >= 6:
			raise IndexError("PokemonList cannot hold more than 6 pokemon")
		self.entries_used = max(0, self.entries_used + 1)
		index = self.entries_used - 1
		self.species_list[index] = pokemon.species.value
		self.species_list[index + 1] = self.TERMINATOR
		self.pokemon_list[index] = pokemon
		self.ot_names[index] = Pokestring(11).fromString(ot_name)
		# FIXME: Properly handle localization
		self.pokemon_names[index] = Pokestring(11).fromString(
				nickname if nickname is not None else pokemon.species.name.upper(),
				fillUp=True)

	def __getitem__(self, index):
		if index >= self.entries_used:
			raise IndexError("list index out of range")
		return self.pokemon_list[index], self.ot_names[index].toString(), self.nickname_at(index)
	
	def __init__(self, pokemon_ot_nickname_list=[]):
		super().__init__()
		self.species_list[0] = self.TERMINATOR
		for entry in pokemon_ot_nickname_list:
			self.add(*entry)

	def __repr__(self):
		return "%s.%s(%s)" % (__name__, self.__class__.__name__, repr(list(self)))
