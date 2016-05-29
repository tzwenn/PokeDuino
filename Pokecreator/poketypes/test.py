import unittest
import os

from . import encoding, loadGame
from .gamesave import GameSave

class TestEncoding(unittest.TestCase):

	def test_encode(self):
		self.assertEqual(encoding.encode("Test"), b"\x93\xa4\xb2\xb3")

	def test_decode(self):
		self.assertEqual(encoding.decode(b"\x93\xa4\xb2\xb3"), "Test")

	def test_encode_decode(self):
		import string
		alphanum = string.ascii_letters + string.digits
		self.assertEqual(encoding.decode(encoding.encode(alphanum)), alphanum)

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

if __name__ == "__main__":
	unittest.main()
	
