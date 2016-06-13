# -*- coding: utf-8 -*-

# Shorthands and decoded strings
NULL       = "\0"
JUNK       = "<JUNK>"
TLC        = "⌜" # top left corner icon
TRC        = "⌝"
BLC        = "⌞"
BRC        = "⌟"
SPACE      = " "
PK         = "PK"
MN         = "MN"
POKEDOLLAR = "$"

# Encoded constants
ENDCHAR    = b'\x50'


class holdover(object):

	def __init__(self, s):
		self.s = s

	def __str__(self):
		return self.s

	def __repr__(self):
		return "holdover(%s)" % self.s

_ = holdover

def holdovers(*args):
	return list(map(holdover, args))


control_characters = [""] * 24

char_set = [
#       -0     -1     -2     -3     -4     -5     -6     -7     -8     -9     -A     -B     -C     -D     -E     -F
      NULL,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,    # 0-
      JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,    # 1-
      JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,    # 2-
      JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,    # 3-
      JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK] + control_characters +                                   \
                                                                                                           holdovers(   # 5-
       'A',   'B' ,  'C',   'D',   'E',   'F',   'G',   'H',   'I',   'V',   'S',   'L',   'M',   ':',  'ぃ',  'ぅ',    # 6-
       '‘',   '’',   '“',   '”',  '・',   '…',  'ぁ',  'ぇ',  'ぉ',   TLC,   '=',   TRC,  '||',   BLC,   BRC)+[SPACE,   # 7-
       'A',   'B',   'C',   'D',   'E',   'F',   'G',   'H',   'I',   'J',   'K',   'L',   'M',   'N',   'O',   'P',    # 8-
       'Q',   'R',   'S',   'T',   'U',   'V',   'W',   'X',   'Y',   'Z',   '(',   ')',   ':',   ';',   '[',   ']',    # 9-
       'a',   'b',   'c',   'd',   'e',   'f',   'g',   'h',   'i',   'j',   'k',   'l',   'm',   'n',   'o',   'p',    # A-
       'q',   'r',   's',   't',   'u',   'v',   'w',   'x',   'y',   'z',   'é', '\'d', '\'l', '\'s', '\'t', '\'v',    # B-
      JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,    # C-
      JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,  JUNK,    # D-
      '\'',    PK,    MN,   '-', '\'r', '\'m',   '?',   '!',   '.',_('ァ'),_('ゥ'),_('ェ'),'▷',   '▶',   '▼',   '♂',    # E-
POKEDOLLAR,   '×',   '.',   '/',   ',',   '♀',   '0',   '1',   '2',   '3',   '4',   '5',   '6',   '7',   '8',   '9']    # F-

def decode(data):
	return "".join(str(char_set[b]) for b in data)

def encode(s):
	return bytes(char_set.index(c) for c in s)

