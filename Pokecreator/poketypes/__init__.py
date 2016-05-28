from .pokemon import *
from .gamesave import *

import encoding

def loadGame(fileName):
	return GameSave.fromString(open(fileName).read())
