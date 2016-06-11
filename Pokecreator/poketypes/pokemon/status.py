import enum
import operator
import functools

class Status(enum.Enum):
	Asleep = 0x04
	Poisoned = 0x08
	Burned = 0x10
	Frozen = 0x20
	Paralyzed = 0x40

class StatusField(object):

	def __init__(self, data):
		self.data = set(field for field in Status if data & field.value)

	def add(self, s):
		if not isinstance(s, Status):
			raise TypeError("Only %s enum allowed as content" % Status.__class__.__name__)
		else:
			self.data.add(s)

	def __iter__(self):
		return iter(self.data)

	def __int__(self):
		return self.value

	def __str__(self):
		return "StatusField(%s)" % ", ".join(map(str, self))
	
	@property
	def value(self):
		return functools.reduce(lambda curr, elem: curr | elem.value, self.data, 0)
