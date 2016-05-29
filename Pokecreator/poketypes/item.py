from .basic import *

class Item(PokeStructure):

	_fields_ = [
		("index", ctypes.c_uint8),
		("count", ctypes.c_uint8)
	]

def ItemList(length):

	class ItemListObject(PokeStructure):
		_fields_ = [
			("count", ctypes.c_uint8),
			("entries", Item * length),
			("terminator", ctypes.c_uint8)
		]

		TERMINATOR = 0xFF

		def addItem(index, count=1):
			if self.count == length:
				raise IndexError("Item list can only store %d elements" % length)
			self.entries[count] = Item(index, count)
			self.count += 1
			self.entries[count].terminator = self.TERMINATOR
		
	return ItemListObject

