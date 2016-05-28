import ctypes

import encoding

class PokeStructure(ctypes.BigEndianStructure):

	_pack_ = 1

	@classmethod
	def fromString(cls, data):
		return cls.from_buffer(ctypes.create_string_buffer(data, len(data)))

	def toString(self):
		return ctypes.string_at(ctypes.byref(self), ctypes.sizeof(self))

def Pokearray(length):

	@classmethod
	def fromString(cls, data):
		return cls(*map(ord, data))

	def toString(self):
		return "".join(map(chr, self))

	t = ctypes.c_uint8 * length
	t.fromString = fromString
	t.toString = toString
	return t

def Pokestring(length):

	@classmethod
	def fromString(cls, data):
		encoded = encoding.encode(data) + encoding.ENDCHAR
		return cls(*map(ord, encoded[:length]))

	def toString(self):
		encoded = "".join(map(chr, self)).partition(encoding.ENDCHAR)[0]
		return encoding.decode(encoded)

	def bytes(self):
		return "".join(map(chr, self))

	t = ctypes.c_uint8 * length
	t.fromString = fromString
	t.toString = toString
	t.bytes = bytes
	return t
	

def PaddingBytes(length):
	return ("padding", Pokearray(length))
