import enum
from .species import Species

class Type(enum.Enum):
	Normal = 0x00
	Fighting = 0x01
	Flying = 0x02
	Poison = 0x03
	Ground = 0x04
	Rock = 0x05
	Bug = 0x07
	Ghost = 0x08
	Fire = 0x14
	Water = 0x15
	Grass = 0x16
	Electric = 0x17
	Psychic = 0x18
	Ice = 0x19
	Dragon = 0x1A

type_for_species = {
	Species.Bulbasaur: (Type.Grass, Type.Poison),
	Species.Ivysaur: (Type.Grass, Type.Poison),
	Species.Venusaur: (Type.Grass, Type.Poison),
	Species.Charmander: (Type.Fire, Type.Fire),
	Species.Charmeleon: (Type.Fire, Type.Fire),
	Species.Charizard: (Type.Fire, Type.Flying),
	Species.Squirtle: (Type.Water, Type.Water),
	Species.Wartortle: (Type.Water, Type.Water),
	Species.Blastoise: (Type.Water, Type.Water),
	Species.Caterpie: (Type.Bug, Type.Bug),
	Species.Metapod: (Type.Bug, Type.Bug),
	Species.Butterfree: (Type.Bug, Type.Flying),
	Species.Weedle: (Type.Bug, Type.Poison),
	Species.Kakuna: (Type.Bug, Type.Poison),
	Species.Beedrill: (Type.Bug, Type.Poison),
	Species.Pidgey: (Type.Normal, Type.Flying),
	Species.Pidgeotto: (Type.Normal, Type.Flying),
	Species.Pidgeot: (Type.Normal, Type.Flying),
	Species.Rattata: (Type.Normal, Type.Normal),
	Species.Raticate: (Type.Normal, Type.Normal),
	Species.Spearow: (Type.Normal, Type.Flying),
	Species.Fearow: (Type.Normal, Type.Flying),
	Species.Ekans: (Type.Poison, Type.Poison),
	Species.Arbok: (Type.Poison, Type.Poison),
	Species.Pikachu: (Type.Electric, Type.Electric),
	Species.Raichu: (Type.Electric, Type.Electric),
	Species.Sandshrew: (Type.Ground, Type.Ground),
	Species.Sandslash: (Type.Ground, Type.Ground),
	Species.Nidoran_f: (Type.Poison, Type.Poison),
	Species.Nidorina: (Type.Poison, Type.Poison),
	Species.Nidoqueen: (Type.Poison, Type.Ground),
	Species.Nidoran_m: (Type.Poison, Type.Poison),
	Species.Nidorino: (Type.Poison, Type.Poison),
	Species.Nidoking: (Type.Poison, Type.Ground),
	Species.Clefairy: (Type.Normal, Type.Normal),
	Species.Clefable: (Type.Normal, Type.Normal),
	Species.Vulpix: (Type.Fire, Type.Fire),
	Species.Ninetales: (Type.Fire, Type.Fire),
	Species.Jigglypuff: (Type.Normal, Type.Normal),
	Species.Wigglytuff: (Type.Normal, Type.Normal),
	Species.Zubat: (Type.Poison, Type.Flying),
	Species.Golbat: (Type.Poison, Type.Flying),
	Species.Oddish: (Type.Grass, Type.Poison),
	Species.Gloom: (Type.Grass, Type.Poison),
	Species.Vileplume: (Type.Grass, Type.Poison),
	Species.Paras: (Type.Bug, Type.Grass),
	Species.Parasect: (Type.Bug, Type.Grass),
	Species.Venonat: (Type.Bug, Type.Poison),
	Species.Venomoth: (Type.Bug, Type.Poison),
	Species.Diglett: (Type.Ground, Type.Ground),
	Species.Dugtrio: (Type.Ground, Type.Ground),
	Species.Meowth: (Type.Normal, Type.Normal),
	Species.Persian: (Type.Normal, Type.Normal),
	Species.Psyduck: (Type.Water, Type.Water),
	Species.Golduck: (Type.Water, Type.Water),
	Species.Mankey: (Type.Fighting, Type.Fighting),
	Species.Primeape: (Type.Fighting, Type.Fighting),
	Species.Growlithe: (Type.Fire, Type.Fire),
	Species.Arcanine: (Type.Fire, Type.Fire),
	Species.Poliwag: (Type.Water, Type.Water),
	Species.Poliwhirl: (Type.Water, Type.Water),
	Species.Poliwrath: (Type.Water, Type.Fighting),
	Species.Abra: (Type.Psychic, Type.Psychic),
	Species.Kadabra: (Type.Psychic, Type.Psychic),
	Species.Alakazam: (Type.Psychic, Type.Psychic),
	Species.Machop: (Type.Fighting, Type.Fighting),
	Species.Machoke: (Type.Fighting, Type.Fighting),
	Species.Machamp: (Type.Fighting, Type.Fighting),
	Species.Bellsprout: (Type.Grass, Type.Poison),
	Species.Weepinbell: (Type.Grass, Type.Poison),
	Species.Victreebel: (Type.Grass, Type.Poison),
	Species.Tentacool: (Type.Water, Type.Poison),
	Species.Tentacruel: (Type.Water, Type.Poison),
	Species.Geodude: (Type.Rock, Type.Ground),
	Species.Graveler: (Type.Rock, Type.Ground),
	Species.Golem: (Type.Rock, Type.Ground),
	Species.Ponyta: (Type.Fire, Type.Fire),
	Species.Rapidash: (Type.Fire, Type.Fire),
	Species.Slowpoke: (Type.Water, Type.Psychic),
	Species.Slowbro: (Type.Water, Type.Psychic),
	Species.Magnemite: (Type.Electric, Type.Electric),
	Species.Magneton: (Type.Electric, Type.Electric),
	Species.Farfetchd: (Type.Normal, Type.Flying),
	Species.Doduo: (Type.Normal, Type.Flying),
	Species.Dodrio: (Type.Normal, Type.Flying),
	Species.Seel: (Type.Water, Type.Water),
	Species.Dewgong: (Type.Water, Type.Ice),
	Species.Grimer: (Type.Poison, Type.Poison),
	Species.Muk: (Type.Poison, Type.Poison),
	Species.Shellder: (Type.Water, Type.Water),
	Species.Cloyster: (Type.Water, Type.Ice),
	Species.Gastly: (Type.Ghost, Type.Poison),
	Species.Haunter: (Type.Ghost, Type.Poison),
	Species.Gengar: (Type.Ghost, Type.Poison),
	Species.Onix: (Type.Rock, Type.Ground),
	Species.Drowzee: (Type.Psychic, Type.Psychic),
	Species.Hypno: (Type.Psychic, Type.Psychic),
	Species.Krabby: (Type.Water, Type.Water),
	Species.Kingler: (Type.Water, Type.Water),
	Species.Voltorb: (Type.Electric, Type.Electric),
	Species.Electrode: (Type.Electric, Type.Electric),
	Species.Exeggcute: (Type.Grass, Type.Psychic),
	Species.Exeggutor: (Type.Grass, Type.Psychic),
	Species.Cubone: (Type.Ground, Type.Ground),
	Species.Marowak: (Type.Ground, Type.Ground),
	Species.Hitmonlee: (Type.Fighting, Type.Fighting),
	Species.Hitmonchan: (Type.Fighting, Type.Fighting),
	Species.Lickitung: (Type.Normal, Type.Normal),
	Species.Koffing: (Type.Poison, Type.Poison),
	Species.Weezing: (Type.Poison, Type.Poison),
	Species.Rhyhorn: (Type.Ground, Type.Rock),
	Species.Rhydon: (Type.Ground, Type.Rock),
	Species.Chansey: (Type.Normal, Type.Normal),
	Species.Tangela: (Type.Grass, Type.Grass),
	Species.Kangaskhan: (Type.Normal, Type.Normal),
	Species.Horsea: (Type.Water, Type.Water),
	Species.Seadra: (Type.Water, Type.Water),
	Species.Goldeen: (Type.Water, Type.Water),
	Species.Seaking: (Type.Water, Type.Water),
	Species.Staryu: (Type.Water, Type.Water),
	Species.Starmie: (Type.Water, Type.Psychic),
	Species.Mr_Mime: (Type.Psychic, Type.Psychic),
	Species.Scyther: (Type.Bug, Type.Flying),
	Species.Jynx: (Type.Ice, Type.Psychic),
	Species.Electabuzz: (Type.Electric, Type.Electric),
	Species.Magmar: (Type.Fire, Type.Fire),
	Species.Pinsir: (Type.Bug, Type.Bug),
	Species.Tauros: (Type.Normal, Type.Normal),
	Species.Magikarp: (Type.Water, Type.Water),
	Species.Gyarados: (Type.Water, Type.Flying),
	Species.Lapras: (Type.Water, Type.Ice),
	Species.Ditto: (Type.Normal, Type.Normal),
	Species.Eevee: (Type.Normal, Type.Normal),
	Species.Vaporeon: (Type.Water, Type.Water),
	Species.Jolteon: (Type.Electric, Type.Electric),
	Species.Flareon: (Type.Fire, Type.Fire),
	Species.Porygon: (Type.Normal, Type.Normal),
	Species.Omanyte: (Type.Rock, Type.Water),
	Species.Omastar: (Type.Rock, Type.Water),
	Species.Kabuto: (Type.Rock, Type.Water),
	Species.Kabutops: (Type.Rock, Type.Water),
	Species.Aerodactyl: (Type.Rock, Type.Flying),
	Species.Snorlax: (Type.Normal, Type.Normal),
	Species.Articuno: (Type.Ice, Type.Flying),
	Species.Zapdos: (Type.Electric, Type.Flying),
	Species.Moltres: (Type.Fire, Type.Flying),
	Species.Dratini: (Type.Dragon, Type.Dragon),
	Species.Dragonair: (Type.Dragon, Type.Dragon),
	Species.Dragonite: (Type.Dragon, Type.Flying),
	Species.Mewtwo: (Type.Psychic, Type.Psychic),
	Species.Mew: (Type.Psychic, Type.Psychic)
}
