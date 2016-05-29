import ctypes

from . import encoding

class PokeStructure(ctypes.BigEndianStructure):

	_pack_ = 1

	@classmethod
	def fromBytes(cls, data):
		return cls.from_buffer_copy(data)

	def bytes(self):
		return ctypes.string_at(ctypes.byref(self), ctypes.sizeof(self))

def Pokearray(length):

	@classmethod
	def fromBytes(cls, data):
		return cls(*data)

	def asBytes(self):
		return bytes(iter(self))

	t = ctypes.c_uint8 * length
	t.fromBytes = fromBytes
	t.bytes = asBytes
	return t

def Pokestring(length):

	@classmethod
	def fromString(cls, data):
		encoded = encoding.encode(data) + encoding.ENDCHAR
		return cls(*encoded[:length])

	def toString(self):
		encoded = self.bytes().partition(encoding.ENDCHAR)[0]
		return encoding.decode(encoded)

	t = Pokearray(length)
	t.fromString = fromString
	t.toString = toString
	return t

def PaddingBytes(length):
	return ("padding", Pokearray(length))
