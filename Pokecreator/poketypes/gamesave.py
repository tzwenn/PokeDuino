from .basic import *
from pokemon import Pokemon

__all__ = ["GameSave"]

class PokemonList(PokeStructure):

	_fields_ = [
			("entries_used", ctypes.c_uint8),
			("species_list", Pokearray(7)),
			("pokemon_list", Pokemon * 6),
			("ot_names", Pokearray(66)),
			("pokemon_names", Pokearray(66))
		]

PokemonBox = Pokearray(1122)

class GameSaveGenI(PokeStructure):

	"""Pokemon game save structure as Generation I according to
	http://bulbapedia.bulbagarden.net/wiki/Save_data_structure_in_Generation_I#Pok.C3.A9mon_lists"""

	_fields_ = [
			("player_name", Pokearray(11)),
			("pokedex_owned", Pokearray(19)),
			("pokedex_seen", Pokearray(19)),
			("pocket_item_list", Pokearray(42)),
			("money", Pokearray(3)),
			("rival_name", Pokearray(11)),
			("options", ctypes.c_uint8),
			("badges", ctypes.c_uint8),
			("player_id", ctypes.c_uint16),
			("pikachu_friendship", ctypes.c_uint8),
			("pc_item_list", Pokearray(102)),
			("current_pc_box", ctypes.c_uint8),
			("casino_coins", ctypes.c_uint16),
			("time_played", ctypes.c_uint32),
			("pokemon_list", PokemonList),
			("current_box", PokemonBox),
			("checksum", ctypes.c_uint8),
			("pc_box_1", PokemonBox),
			("pc_box_2", PokemonBox),
			("pc_box_3", PokemonBox),
			("pc_box_4", PokemonBox),
			("pc_box_5", PokemonBox),
			("pc_box_6", PokemonBox),
			("pc_box_7", PokemonBox),
			("pc_box_8", PokemonBox),
			("pc_box_9", PokemonBox),
			("pc_box_10", PokemonBox),
			("pc_box_11", PokemonBox),
			("pc_box_12", PokemonBox)
		]

GameSave = GameSaveGenI
