from .basic import *

class Item(PokeStructure):

	_fields_ = [
		("index", ctypes.c_uint8),
		("count", ctypes.c_uint8)
	]

def ItemList(count):

	class ItemListObject(PokeStructure):
		_fields_ = [
			("count", ctypes.c_uint8),
			("entries", Item * count),
			("terminator", ctypes.c_uint8)
		]
		
	return ItemListObject
