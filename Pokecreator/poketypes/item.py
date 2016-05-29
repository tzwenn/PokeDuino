import enum

from .basic import *

class Index(enum.Enum):
	Nothing, \
	MasterBall, \
	UltraBall, \
	GreatBall, \
	PokeBall, \
	TownMap, \
	Bicycle, \
	unobtainable0x7, \
	SafariBall, \
	Pokedex, \
	MoonStone, \
	Antidote, \
	BurnHeal, \
	IceHeal, \
	Awakening, \
	ParlyzHeal, \
	FullRestore, \
	MaxPotion, \
	HyperPotion, \
	SuperPotion, \
	Potion, \
	BoulderBadge, \
	CascadeBadge, \
	ThunderBadge, \
	RainbowBadge, \
	SoulBadge, \
	MarshBadge, \
	VolcanoBadge, \
	EarthBadge, \
	EscapeRope, \
	Repel, \
	OldAmber, \
	FireStone, \
	ThunderStone, \
	WaterStone, \
	HPUp, \
	Protein, \
	Iron, \
	Carbos, \
	Calcium, \
	RareCandy, \
	DomeFossil, \
	HelixFossil, \
	SecretKey, \
	unobtainable0x2c, \
	BikeVoucher, \
	XAccuracy, \
	LeafStone, \
	CardKey, \
	Nugget, \
	glicht_PPUp, \
	PokeDoll, \
	FullHeal, \
	Revive, \
	MaxRevive, \
	GuardSpec, \
	SuperRepel, \
	MaxRepel, \
	DireHit, \
	Coin, \
	FreshWater, \
	SodaPop, \
	Lemonade, \
	SS_Ticket, \
	GoldTeeth, \
	XAttack, \
	XDefend, \
	XSpeed, \
	XSpecial, \
	CoinCase, \
	OaksParcel, \
	Itemfinder, \
	SilphScope, \
	PokeFlute, \
	LiftKey, \
	ExpAll, \
	OldRod, \
	GoodRod, \
	SuperRod, \
	PPUp, \
	Ether, \
	MaxEther, \
	Elixer, \
	MaxElixer = range(84)

	HM01, \
	HM02, \
	HM03, \
	HM04, \
	HM05, \
	TM01, \
	TM02, \
	TM03, \
	TM04, \
	TM05, \
	TM06, \
	TM07, \
	TM08, \
	TM09, \
	TM10, \
	TM11, \
	TM12, \
	TM13, \
	TM14, \
	TM15, \
	TM16, \
	TM17, \
	TM18, \
	TM19, \
	TM20, \
	TM21, \
	TM22, \
	TM23, \
	TM24, \
	TM25, \
	TM26, \
	TM27, \
	TM28, \
	TM29, \
	TM30, \
	TM31, \
	TM32, \
	TM33, \
	TM34, \
	TM35, \
	TM36, \
	TM37, \
	TM38, \
	TM39, \
	TM40, \
	TM41, \
	TM42, \
	TM43, \
	TM44, \
	TM45, \
	TM46, \
	TM47, \
	TM48, \
	TM49, \
	TM50, \
	TM51, \
	TM52, \
	TM53, \
	TM54, \
	TM55 = range(196, 256)

class Item(PokeStructure):

	_fields_ = [
		("_index", ctypes.c_uint8),
		("count", ctypes.c_uint8)
	]

	_enum_properties_ = [
		("_index", Index)
	]

	def __init__(self, index, count):
		self.index = index
		self.count = count

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

