from .pokemon import *
from .gamesave import *
from .team import *
from . import pokedex

def loadGame(fileName):
	with open(fileName, "rb") as f:
		return GameSave.fromBytes(f.read())
