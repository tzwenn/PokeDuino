import unittest
import os

import encoding
from .gamesave import GameSave

class TestEncoding(unittest.TestCase):

	def test_encode(self):
		self.assertEqual(encoding.encode("Test"), "\x93\xa4\xb2\xb3")

	def test_decode(self):
		self.assertEqual(encoding.decode("\x93\xa4\xb2\xb3"), "Test")

	def test_encode_decode(self):
		import string
		alphanum = string.letters + string.digits
		self.assertEqual(encoding.decode(encoding.encode(alphanum)), alphanum)

class TestGameSave(unittest.TestCase):

	batterySaveFileName = os.path.join(os.path.dirname(__file__), "..", "testdata.sav")

	def setUp(self):
		self.save = GameSave.fromString(open(self.batterySaveFileName).read())

	def test_player_name(self):
		self.assertEqual(self.save.player_name.toString(), "Player")

	def test_rival_name(self):
		self.assertEqual(self.save.rival_name.toString(), "Rival")

if __name__ == "__main__":
	unittest.main()
	
