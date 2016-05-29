from .pokemon import *
from .gamesave import *

def loadGame(fileName):
	with open(fileName, "rb") as f:
		return GameSave.fromBytes(f.read())
