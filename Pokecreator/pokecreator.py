#!/usr/bin/env python3

import sys
import argparse
import random

import poketypes

_s = lambda s: bytes(s, "ascii")

output_format = {
	"binary": lambda data: data,
	"hex": lambda data: _s("".join("%02x" % c for c in data) + "\n"),
	"c_array": lambda data: _s(", ".join("0x%02X" % c for c in data) + "\n"),
	"python": lambda data: _s(repr(poketypes.Pokemon.fromBytes(data)) + "\n")
}

class FindSpeciesInPokedex(argparse.Action):
	
	def __call__(self, parser, namespace, values, option_string=None):
		species = poketypes.pokedex.national[values]
		setattr(namespace, "species", species)
	
class FindSpeciesByName(argparse.Action):

	def __call__(self, parser, namespace, values, option_string=None):
		species = poketypes.pokemon.Species[values]
		setattr(namespace, "species", species)

class StoreMove(argparse.Action):

	def __call__(self, parser, namespace, values, option_string=None):
		if len(values) > 4:
			raise argparse.ArgumentTypeError("Max 4 moves allowed")
		moves = [poketypes.pokemon.Move[name] for name in values]
		moves += [poketypes.pokemon.Move.NONE] * (4 - len(moves))
		setattr(namespace, "moves", moves)

class StorePPUps(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if len(values) > 4:
			raise argparse.ArgumentTypeError("PP-ups for max 4 moves allowed")
		setattr(namespace, "pp_ups", values + [0] * (4 - len(values)))


def parseArguments():
	parser = argparse.ArgumentParser(
			description="Generate a pokemon that can be send e.g. to the PokeDuino.",
		)

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--species", "-s", type=str, 
			action=FindSpeciesByName,
			help="Species as a string.")
	group.add_argument("--pokedex", "-p", type=int,
			action=FindSpeciesInPokedex,
			help="Index number ")
	parser.add_argument("--level", "-l", type=int,
			default=5)
	parser.add_argument("--original-trainer", "-o", type=int, default=0)

	parser.add_argument("--moves", "-m", type=str,
			default=[poketypes.pokemon.Move.NONE] * 4,
			nargs='+',
			action=StoreMove)
	parser.add_argument("--pp-ups", "-pu", type=int,
			choices=range(4),
			nargs="+",
			default=[0] * 4,
			action=StorePPUps)

	parser.add_argument("--health-ev", "-hv", type=int, default=0)
	parser.add_argument("--attack-ev", "-av", type=int, default=0)
	parser.add_argument("--defense-ev", "-dv", type=int, default=0)
	parser.add_argument("--speed-ev", "-sv", type=int, default=0)
	parser.add_argument("--special-ev", "-cv", type=int, default=0)

	parser.add_argument("--individual-values", "-iv", type=lambda s: 0xffff if s == "max" else int(s, 16),
			default=int(random.random() * 0x10000),
			help="Hex representation of the pokemon's 16bit individual values vector or \"max\". Random value if not specified."
		)

	parser.add_argument("--output-format", "-f",
			choices=output_format.keys(),
			default="binary"
		)
	try:
		return parser.parse_args()
	except argparse.ArgumentTypeError as err:
		parser.error(err)

def createPokemon(args):
	pokemon = poketypes.Pokemon(
			species=args.species,
			level=args.level,
			hp_ev=args.health_ev,
			attack_ev=args.attack_ev,
			defense_ev=args.defense_ev,
			speed_ev=args.speed_ev,
			special_ev=args.special_ev,
			iv=args.individual_values,
			original_trainer=args.original_trainer
		)
	pokemon.move1, pokemon.move2, pokemon.move3, pokemon.move4 = args.moves
	pokemon.move1_pp.up, pokemon.move1_pp.up, pokemon.move1_pp.up, pokemon.move1_pp.up = args.pp_ups
	pokemon.heal()
	return pokemon

if __name__ == "__main__":
	args = parseArguments()
	pokemon = createPokemon(args)
	sys.stdout.buffer.write(output_format[args.output_format](pokemon.bytes()))
