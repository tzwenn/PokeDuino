import enum
import math

from .species import Species

__all__ = ["ExperienceClass", "exp_for_level", "level_for_exp", "class_for_species"]

class ExperienceClass(enum.Enum):
	Fast, \
	MediumFast, \
	MediumSlow, \
	Slow = range(4)

exp_for_level = {
	ExperienceClass.Fast: lambda n: (4 * n ** 3) // 5,
	ExperienceClass.MediumFast: lambda n: n ** 3,
	ExperienceClass.MediumSlow: lambda n: (6 * n ** 3) // 5 - 15 * n ** 2 + 100*n - 140,
	ExperienceClass.Slow: lambda n: (5 * n ** 3) // 4
}

def _findlevel_factory(xpClass):
	
	l2xp = exp_for_level[xpClass]

	def binsearch(xp, start, end):
		if start + 1 >= end:
			return start
		mid = (start + end) // 2
		if xp >= l2xp(mid):
			return binsearch(xp, mid, end)
		else:
			return binsearch(xp, start, mid)

	return lambda xp: max(0, min(100, binsearch(xp, 0, 101)))

level_for_exp = {xpClass: _findlevel_factory(xpClass) for xpClass in ExperienceClass}

# level_for_exp = {
# 	ExperienceClass.Fast: lambda x: (5 * x / 4) ** (1.0 / 3),
# 	ExperienceClass.MediumFast: lambda x: x ** (1.0 / 3),
# 	ExperienceClass.MediumSlow: lambda x: 25.0/6 - (25 * 5 ** (2./3))/(2*(-1855 + 18*x + 2*math.sqrt(1387600 - 16695*x + 81*x**2))**(1./3)) + (5**(1./3)*(-1855 + 18*x + 2*math.sqrt(1387600 - 16695*x + 81*x**2))**(1./3))/6,
# 	ExperienceClass.Slow: lambda x: (4 * x / 5) ** (1.0 / 3),
# }

class_for_species = {
	Species.Bulbasaur: ExperienceClass.MediumSlow,
	Species.Ivysaur: ExperienceClass.MediumSlow,
	Species.Venusaur: ExperienceClass.MediumSlow,
	Species.Charmander: ExperienceClass.MediumSlow,
	Species.Charmeleon: ExperienceClass.MediumSlow,
	Species.Charizard: ExperienceClass.MediumSlow,
	Species.Squirtle: ExperienceClass.MediumSlow,
	Species.Wartortle: ExperienceClass.MediumSlow,
	Species.Blastoise: ExperienceClass.MediumSlow,
	Species.Caterpie: ExperienceClass.MediumFast,
	Species.Metapod: ExperienceClass.MediumFast,
	Species.Butterfree: ExperienceClass.MediumFast,
	Species.Weedle: ExperienceClass.MediumFast,
	Species.Kakuna: ExperienceClass.MediumFast,
	Species.Beedrill: ExperienceClass.MediumFast,
	Species.Pidgey: ExperienceClass.MediumSlow,
	Species.Pidgeotto: ExperienceClass.MediumSlow,
	Species.Pidgeot: ExperienceClass.MediumSlow,
	Species.Rattata: ExperienceClass.MediumFast,
	Species.Raticate: ExperienceClass.MediumFast,
	Species.Spearow: ExperienceClass.MediumFast,
	Species.Fearow: ExperienceClass.MediumFast,
	Species.Ekans: ExperienceClass.MediumFast,
	Species.Arbok: ExperienceClass.MediumFast,
	Species.Pikachu: ExperienceClass.MediumFast,
	Species.Raichu: ExperienceClass.MediumFast,
	Species.Sandshrew: ExperienceClass.MediumFast,
	Species.Sandslash: ExperienceClass.MediumFast,
	Species.Nidoran_f: ExperienceClass.MediumSlow,
	Species.Nidorina: ExperienceClass.MediumSlow,
	Species.Nidoqueen: ExperienceClass.MediumSlow,
	Species.Nidoran_m: ExperienceClass.MediumSlow,
	Species.Nidorino: ExperienceClass.MediumSlow,
	Species.Nidoking: ExperienceClass.MediumSlow,
	Species.Clefairy: ExperienceClass.Fast,
	Species.Clefable: ExperienceClass.Fast,
	Species.Vulpix: ExperienceClass.MediumFast,
	Species.Ninetales: ExperienceClass.MediumFast,
	Species.Jigglypuff: ExperienceClass.Fast,
	Species.Wigglytuff: ExperienceClass.Fast,
	Species.Zubat: ExperienceClass.MediumFast,
	Species.Golbat: ExperienceClass.MediumFast,
	Species.Oddish: ExperienceClass.MediumSlow,
	Species.Gloom: ExperienceClass.MediumSlow,
	Species.Vileplume: ExperienceClass.MediumSlow,
	Species.Paras: ExperienceClass.MediumFast,
	Species.Parasect: ExperienceClass.MediumFast,
	Species.Venonat: ExperienceClass.MediumFast,
	Species.Venomoth: ExperienceClass.MediumFast,
	Species.Diglett: ExperienceClass.MediumFast,
	Species.Dugtrio: ExperienceClass.MediumFast,
	Species.Meowth: ExperienceClass.MediumFast,
	Species.Persian: ExperienceClass.MediumFast,
	Species.Psyduck: ExperienceClass.MediumFast,
	Species.Golduck: ExperienceClass.MediumFast,
	Species.Mankey: ExperienceClass.MediumFast,
	Species.Primeape: ExperienceClass.MediumFast,
	Species.Growlithe: ExperienceClass.Slow,
	Species.Arcanine: ExperienceClass.Slow,
	Species.Poliwag: ExperienceClass.MediumSlow,
	Species.Poliwhirl: ExperienceClass.MediumSlow,
	Species.Poliwrath: ExperienceClass.MediumSlow,
	Species.Abra: ExperienceClass.MediumSlow,
	Species.Kadabra: ExperienceClass.MediumSlow,
	Species.Alakazam: ExperienceClass.MediumSlow,
	Species.Machop: ExperienceClass.MediumSlow,
	Species.Machoke: ExperienceClass.MediumSlow,
	Species.Machamp: ExperienceClass.MediumSlow,
	Species.Bellsprout: ExperienceClass.MediumSlow,
	Species.Weepinbell: ExperienceClass.MediumSlow,
	Species.Victreebel: ExperienceClass.MediumSlow,
	Species.Tentacool: ExperienceClass.Slow,
	Species.Tentacruel: ExperienceClass.Slow,
	Species.Geodude: ExperienceClass.MediumSlow,
	Species.Graveler: ExperienceClass.MediumSlow,
	Species.Golem: ExperienceClass.MediumSlow,
	Species.Ponyta: ExperienceClass.MediumFast,
	Species.Rapidash: ExperienceClass.MediumFast,
	Species.Slowpoke: ExperienceClass.MediumFast,
	Species.Slowbro: ExperienceClass.MediumFast,
	Species.Magnemite: ExperienceClass.MediumFast,
	Species.Magneton: ExperienceClass.MediumFast,
	Species.Farfetchd: ExperienceClass.MediumFast,
	Species.Doduo: ExperienceClass.MediumFast,
	Species.Dodrio: ExperienceClass.MediumFast,
	Species.Seel: ExperienceClass.MediumFast,
	Species.Dewgong: ExperienceClass.MediumFast,
	Species.Grimer: ExperienceClass.MediumFast,
	Species.Muk: ExperienceClass.MediumFast,
	Species.Shellder: ExperienceClass.Slow,
	Species.Cloyster: ExperienceClass.Slow,
	Species.Gastly: ExperienceClass.MediumSlow,
	Species.Haunter: ExperienceClass.MediumSlow,
	Species.Gengar: ExperienceClass.MediumSlow,
	Species.Onix: ExperienceClass.MediumFast,
	Species.Drowzee: ExperienceClass.MediumFast,
	Species.Hypno: ExperienceClass.MediumFast,
	Species.Krabby: ExperienceClass.MediumFast,
	Species.Kingler: ExperienceClass.MediumFast,
	Species.Voltorb: ExperienceClass.MediumFast,
	Species.Electrode: ExperienceClass.MediumFast,
	Species.Exeggcute: ExperienceClass.Slow,
	Species.Exeggutor: ExperienceClass.Slow,
	Species.Cubone: ExperienceClass.MediumFast,
	Species.Marowak: ExperienceClass.MediumFast,
	Species.Hitmonlee: ExperienceClass.MediumFast,
	Species.Hitmonchan: ExperienceClass.MediumFast,
	Species.Lickitung: ExperienceClass.MediumFast,
	Species.Koffing: ExperienceClass.MediumFast,
	Species.Weezing: ExperienceClass.MediumFast,
	Species.Rhyhorn: ExperienceClass.Slow,
	Species.Rhydon: ExperienceClass.Slow,
	Species.Chansey: ExperienceClass.Fast,
	Species.Tangela: ExperienceClass.MediumFast,
	Species.Kangaskhan: ExperienceClass.MediumFast,
	Species.Horsea: ExperienceClass.MediumFast,
	Species.Seadra: ExperienceClass.MediumFast,
	Species.Goldeen: ExperienceClass.MediumFast,
	Species.Seaking: ExperienceClass.MediumFast,
	Species.Staryu: ExperienceClass.Slow,
	Species.Starmie: ExperienceClass.Slow,
	Species.Mr_Mime: ExperienceClass.MediumFast,
	Species.Scyther: ExperienceClass.MediumFast,
	Species.Jynx: ExperienceClass.MediumFast,
	Species.Electabuzz: ExperienceClass.MediumFast,
	Species.Magmar: ExperienceClass.MediumFast,
	Species.Pinsir: ExperienceClass.Slow,
	Species.Tauros: ExperienceClass.Slow,
	Species.Magikarp: ExperienceClass.Slow,
	Species.Gyarados: ExperienceClass.Slow,
	Species.Lapras: ExperienceClass.Slow,
	Species.Ditto: ExperienceClass.MediumFast,
	Species.Eevee: ExperienceClass.MediumFast,
	Species.Vaporeon: ExperienceClass.MediumFast,
	Species.Jolteon: ExperienceClass.MediumFast,
	Species.Flareon: ExperienceClass.MediumFast,
	Species.Porygon: ExperienceClass.MediumFast,
	Species.Omanyte: ExperienceClass.MediumFast,
	Species.Omastar: ExperienceClass.MediumFast,
	Species.Kabuto: ExperienceClass.MediumFast,
	Species.Kabutops: ExperienceClass.MediumFast,
	Species.Aerodactyl: ExperienceClass.Slow,
	Species.Snorlax: ExperienceClass.Slow,
	Species.Articuno: ExperienceClass.Slow,
	Species.Zapdos: ExperienceClass.Slow,
	Species.Moltres: ExperienceClass.Slow,
	Species.Dratini: ExperienceClass.Slow,
	Species.Dragonair: ExperienceClass.Slow,
	Species.Dragonite: ExperienceClass.Slow,
	Species.Mewtwo: ExperienceClass.Slow,
	Species.Mew: ExperienceClass.MediumSlow
}
