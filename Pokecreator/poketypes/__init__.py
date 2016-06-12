from .pokemon import *
from .gamesave import *
from .teamlist import *

def loadGame(fileName):
	with open(fileName, "rb") as f:
		return GameSave.fromBytes(f.read())
