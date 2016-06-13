import ctypes

from . import encoding

class PokeMetaStructure(type(ctypes.BigEndianStructure)):

	def __new__(metacls, name, bases, dct):
		cls = super().__new__(metacls, name, bases, dct)
		for member, adapter_type in cls._adapters_:
			cls.buildProperty(member, adapter_type)
		return cls

	def buildProperty(cls, member, adapter_type):

		def get(self):
			return adapter_type(getattr(self, member))

		def set(self, value):
			if isinstance(value, adapter_type):
				setattr(self, member, value.value)
			else:
				setattr(self, member, value)
		if member.startswith("_"):
			property_name = member[1:]
		else:
			property_name = member + "_adapter"
		setattr(cls, property_name, 
				property(fget=get, fset=set, doc="%s adapter  to member %s" % (adapter_type.__name__, member)))

class PokeStructure(ctypes.BigEndianStructure, metaclass=PokeMetaStructure):

	_pack_ = 1
	_adapters_ = []

	@classmethod
	def fromBytes(cls, data):
		return cls.from_buffer_copy(data)

	def bytes(self):
		return ctypes.string_at(ctypes.byref(self), ctypes.sizeof(self))

def Pokearray(length):

	# okay, I learned. 
	# It's not possible to use a custom base class
	# in a ctypes.Structure field. Forget about it

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
	def fromString(cls, data, fillUp=False):
		encoded = encoding.encode(data) + encoding.ENDCHAR
		if fillUp:
			encoded = encoded.ljust(length, encoding.ENDCHAR)
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
