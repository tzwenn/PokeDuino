import ctypes

from . import encoding

class PokeMetaStructure(type(ctypes.BigEndianStructure)):

	def __new__(metacls, name, bases, dct):
		cls = super().__new__(metacls, name, bases, dct)
		for name, enumcls in cls._enum_properties_:
			cls.buildProperty(name, enumcls)
		return cls

	def buildProperty(cls, name, enumcls):

		def get(self):
			return enumcls(getattr(self, name))

		def set(self, value):
			if isinstance(value, enumcls):
				setattr(self, name, value.value)
			else:
				setattr(self, name, value)

		if name.startswith("_"):
			property_name = name[1:]
		else:
			property_name = name + "_enum"
		setattr(cls, property_name, 
				property(fget=get, fset=set, doc="Enum proxy to member %s" % name))

class PokeStructure(ctypes.BigEndianStructure, metaclass=PokeMetaStructure):

	_pack_ = 1
	_enum_properties_ = []

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
