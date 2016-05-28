import ctypes

class PokeStructure(ctypes.BigEndianStructure):

	_pack_ = 1

	@classmethod
	def fromString(cls, data):
		return cls.from_buffer(ctypes.create_string_buffer(data, len(data)))


def Pokearray(length):
	return ctypes.c_char * length

