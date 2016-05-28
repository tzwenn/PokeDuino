import ctypes

class PokeStructure(ctypes.BigEndianStructure):

	_pack_ = 1

	@classmethod
	def fromString(cls, data):
		return cls.from_buffer(ctypes.create_string_buffer(data, len(data)))


def Pokearray(length):

	from types import MethodType
	def asBytes(self):
		return "".join(map(chr, self))

	t = ctypes.c_uint8 * length
	t.bytes = asBytes

	return t

