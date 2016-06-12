import unittest
import os

from . import encoding, loadGame, item
from .gamesave import GameSave
from .basic import PokeStructure
from .pokemon import Pokemon, Species, experience

class TestEncoding(unittest.TestCase):

	def test_encode(self):
		self.assertEqual(encoding.encode("Test"), b"\x93\xa4\xb2\xb3")

	def test_decode(self):
		self.assertEqual(encoding.decode(b"\x93\xa4\xb2\xb3"), "Test")

	def test_encode_decode(self):
		import string
		alphanum = string.ascii_letters + string.digits
		self.assertEqual(encoding.decode(encoding.encode(alphanum)), alphanum)

class TestPokeStructure(unittest.TestCase):

	def setUp(self):

		import enum, ctypes

		class Fruit(enum.Enum):
			Apple, Banana, Citron = range(3)

		class TestStruct(PokeStructure):

			_fields_ = [
				("_fruit", ctypes.c_uint8),
			]
			
			_adapters_ = [
				("_fruit", Fruit)
			]

		self.Fruit = Fruit
		self.TestStruct = TestStruct

	def test_enum_property(self):
		obj = self.TestStruct()
		self.assertIsInstance(obj.fruit, self.Fruit)
		
		obj.fruit = self.Fruit.Apple
		self.assertEqual(obj.fruit, self.Fruit.Apple)
		self.assertEqual(obj._fruit, self.Fruit.Apple.value)

		obj.fruit = self.Fruit.Banana.value
		self.assertEqual(obj.fruit.name, "Banana")

	def test_item_enum(self):
		pokeball = item.Item(item.Index.PokeBall.value, 1)
		self.assertEqual(pokeball.index, item.Index.PokeBall)

class TestPokemon(unittest.TestCase):

	def test_xp_to_level_conversion(self):
		for xpClass in experience.ExperienceClass:
			for level in range(2, 101):
				self.assertEqual(level, experience.level_for_exp[xpClass](experience.exp_for_level[xpClass](level)))

class TestSpecies(unittest.TestCase):

	def test_normal_name(self):
		self.assertEqual(Species.Mew.name, "Mew")
		self.assertEqual(Species["Mew"], Species.Mew)
	
	def test_special_name(self):
		self.assertEqual(Species.Mr_Mime.name, "Mr. Mime")
		self.assertEqual(Species["Mr. Mime"], Species.Mr_Mime)

	def test_stats(self):
		"""According to example 1 from http://bulbapedia.bulbagarden.net/wiki/Individual_values#Usage"""
		mewtwo = Pokemon()
		mewtwo.species = Species.Mewtwo
		mewtwo.level = 70
		mewtwo.iv = 0b1110010110000110
		mewtwo.sanitize()
		self.assertEqual(mewtwo.max_hp, 234)
		self.assertEqual(mewtwo.attack, 178)
		self.assertEqual(mewtwo.defense, 138)
		self.assertEqual(mewtwo.speed, 198)
		self.assertEqual(mewtwo.special, 229)

class TestGameSave(unittest.TestCase):

	batterySaveFileName = os.path.join(os.path.dirname(__file__), "..", "testdata.sav")

	def setUp(self):
		self.save = loadGame(self.batterySaveFileName)

	def test_player_name(self):
		self.assertEqual(self.save.player_name.toString(), "Player")

	def test_rival_name(self):
		self.assertEqual(self.save.rival_name.toString(), "Rival")

	def test_calc_checksum(self):
		self.assertEqual(self.save._calcChecksum(), self.save.checksum)
	
	def test_item_list(self):
		firstItem = self.save.pocket_item_list.entries[0]
		self.assertEqual(firstItem.index, item.Index.Potion)

	def test_second_pokemon_in_team(self):
		pokemon, ot, nickname = self.save.team[1]
		self.assertEqual(pokemon.species.value, self.save.team.species_list[1])
		self.assertEqual(pokemon.species, Species.Rattata)
		self.assertEqual(ot, "Trainer")
		self.assertEqual(nickname, "SQUEAK")

if __name__ == "__main__":
	unittest.main()

