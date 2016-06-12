#!/usr/bin/env python3

import sys
import enum
import argparse
import serial

import poketypes

def connect(dev, baud, callback):
	"""Connects as slave to the game link proxy on arduino
	callback is called when a new byte is received and shall be answered"""
	con = serial.Serial(dev, baud)
	data = 0
	try:
		while True:
			con.write(bytes([data]))
			data = callback(con.read(1)[0])
	finally:
		con.close()

##################

class ConnectionState(enum.Enum):
	NotConnected, Ack, TradeCenter, Colosseum =  range(4)

class TradeState(enum.Enum):
	Init, Ready, SeenFirstWait, Random, WaitingToSend, SendingData, \
	SendingPatch, Pending, Confirmation, Done = range(10)

Master = 0x01
Slave = 0x02
Connected = 0x60
Waiting = 0x7F

TradeEntry, ColosseumEntry, CancelEntry = 0xD0, 0xD1, 0xD2
selected = lambda i: i | 4

class TradeData(poketypes.basic.PokeStructure):

	_fields_ = [
			("trainer_name", poketypes.basic.Pokestring(11)),
			("team", poketypes.Team),
			poketypes.basic.PaddingBytes(3)
	]

class PokemonSession(object):

	def __init__(self, trainer_name, team, receivePokemonHook=None, replaceTeamUponReceive=True):
		self.c_state = ConnectionState.NotConnected
		self.t_state = TradeState.Init
		self.__buildStateTransitions()

		self.receivePokemonHook = receivePokemonHook
		self.replaceTeamUponReceive = replaceTeamUponReceive
		self.trainer_name = trainer_name
		self.__buildSendData(team)

		self.trade_receive = bytes()
		self.trade_pokemon_idx = None
		self.trade_counter = 0

	def __buildStateTransitions(self):
		# Simple Mealy machine lookup:
		# [state](input) -> (output, new_state)
		self.handle_c_state = {
			ConnectionState.NotConnected: self.handleNotConnected,
			ConnectionState.Ack: self.handleAck,
			ConnectionState.TradeCenter: self.handleTradeCenter,
			ConnectionState.Colosseum: self.handleColosseum
		}

		self.handle_t_state = {
			TradeState.Init: self.handleT_Init,
			TradeState.Ready: self.handleT_Ready,
			TradeState.SeenFirstWait: self.handleT_SeenFirstWait,
			TradeState.Random: self.handleT_Random,
			TradeState.WaitingToSend: self.handleT_WaitingToSend,
			TradeState.SendingData: self.handleT_SendingData,
			TradeState.SendingPatch: self.handleT_SendingPatch,
			TradeState.Pending: self.handleT_Pending,
			TradeState.Confirmation: self.handleT_Confirmation,
			TradeState.Done: self.handleT_Done
		}

	def __buildSendData(self, team):
		self.trade_send = TradeData(trainer_name=poketypes.basic.Pokestring(11).fromString(self.trainer_name),
		                  team=team).bytes()

	def _saverecv(self, byte):
		self.trade_receive += bytes([byte])

	##################################################

	def __call__(self, data):
		try:
			output, new_state = self.handle_c_state[self.c_state](data)
		except TypeError:
			output, new_state = data, self.c_state
		self.c_state = new_state
		return output

	def handleNotConnected(self, data):
		if data == Master:
			return Slave, ConnectionState.NotConnected
		elif data == 0:
			return 0, ConnectionState.NotConnected
		elif data == Connected:
			return Connected, ConnectionState.Ack

	def handleAck(self, data):
		if data == Connected:
			return Connected, ConnectionState.Ack
		elif data == selected(TradeEntry):
			return 0, ConnectionState.TradeCenter
		elif data == selected(ColosseumEntry):
			return 0, ConnectionState.Colosseum
		elif data in [Master, selected(CancelEntry)]:
			return selected(CancelEntry), ConnectionState.NotConnected
		else:
			return data, ConnectionState.Ack

	def handleColosseum(self, data):
		return data, ConnectionState.Colosseum

	##################################################

	def handleTradeCenter(self, data):
		try:
			output, new_state = self.handle_t_state[self.t_state](data)
		except TypeError:
			output, new_state = data, self.t_state
		self.t_state = new_state
		return output, ConnectionState.TradeCenter

	def handleT_Init(self, data):
		if data == 0: return 0, TradeState.Ready

	def handleT_Ready(self, data):
		if data == 0xFD: return 0xFD, TradeState.SeenFirstWait

	def handleT_SeenFirstWait(self, data):
		if data != 0xFD: return data, TradeState.Random

	def handleT_Random(self, data):
		if data == 0xFD: return data, TradeState.WaitingToSend

	def handleT_WaitingToSend(self, data):
		self.trade_counter = 0
		self.trade_receive = bytes()
		if data != 0xFD:
			self._saverecv(data)
			return self.trade_send[self.trade_counter], TradeState.SendingData

	def handleT_SendingData(self, data):
		self._saverecv(data)
		self.trade_counter += 1
		out = self.trade_send[self.trade_counter]
		next_state = (TradeState.SendingPatch if self.trade_counter >= len(self.trade_send) - 1 else TradeState.SendingData)
		return out, next_state

	def handleT_SendingPatch(self, data):
		if data == 0xFD:
			self.trade_counter = 0
			return 0xFD, TradeState.SendingPatch
		else:
			self.trade_counter += 1
			return data, (TradeState.SendingPatch if self.trade_counter < 197 else TradeState.Pending)

	def handleT_Pending(self, data):
		if data == 0:
			return 0, TradeState.Confirmation
		elif data & 0x60 == 0x60:
			if data == 0x6f:
				return 0x6f, TradeState.Ready
			else:
				self.trade_pokemon_idx = data - 0x60
				# Trade my first pokemon
				return 0x60, TradeState.Pending

	def handleT_Confirmation(self, data):
		if data == 0x61:
			self.trade_pokemon_idx = None
			return 0x61, TradeState.Pending
		elif data & 0x60 == 0x60:
			self.__received_pokemon()
			return data, TradeState.Done

	def handleT_Done(self, data):
		if data == 0:
			return 0, TradeState.Init

	##################################################

	def __received_pokemon(self):
		recvdata = TradeData.fromBytes(self.trade_receive)
		pokemon, ot_name, nickname = recvdata.team[self.trade_pokemon_idx]
		if self.replaceTeamUponReceive:
			self.__buildSendData(poketypes.Team([recvdata.team[self.trade_pokemon_idx]]))
		if self.receivePokemonHook is not None:
			self.receivePokemonHook(pokemon, ot_name, nickname)


def receivedPokemonHandler(pokemon, ot_name, nickname):
	sys.stdout.buffer.write(pokemon.bytes())
	print("Pushed a %s %sfrom %s to stdout" % \
			(pokemon.species.name, "(called %s) " % nickname if nickname else "", ot_name),
			file=sys.stderr)


def parseArguments():
	parser = argparse.ArgumentParser(
			formatter_class=argparse.ArgumentDefaultsHelpFormatter,
			description="Trade a pokemon read from stdin over a arduino proxy. Received pokemon are printed to stdout"
		)

	parser.add_argument("--baudrate", "-b", type=int,
			default=115200,
			help="Baudrate of the serial connection")
	parser.add_argument("--device", "-d", type=str,
			default="/dev/tty.usbmodemfa131",
			help="Device name of the serial port")

	parser.add_argument("--trainer", "-t", type=str,
			default="POKEDUINO",
			help="The simulated gameboys player name")
	parser.add_argument("--otname", "-o", type=str,
			help="Original trainer name of the send pokemon (copies from --trainer if not specified)")
	parser.add_argument("--nickname", "-n", type=str,
			help="Nickname of the send pokemon")

	try:
		args = parser.parse_args()
	except argparse.ArgumentTypeError as err:
		parser.error(err)

	if args.otname is None:
		args.otname = args.trainer

	return args


if __name__ == "__main__":
	args = parseArguments()

	pokemon = poketypes.Pokemon.fromBytes(sys.stdin.buffer.read())

	team = poketypes.Team([(pokemon, args.otname, args.nickname)])
	session = PokemonSession(args.trainer, team, receivedPokemonHandler)

	connect(args.device, args.baudrate, session)

