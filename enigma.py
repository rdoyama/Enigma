##
##  Functions for encrypting/decrypting Enigma messages
##  
##	This code aims to simulate a Enigma M3 (1934) or
##	M4 (1942), both used by the German Navy supporting
##	up to four rotors and the ring configuration.
##


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

L2POS = {letter: i for i, letter in enumerate(ALPHABET)}
POS2L = {i: letter for i, letter in enumerate(ALPHABET)}

# Rotors used by the military
ROTORS = {
	"I":    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
	"II":   "AJDKSIRUXBLHWTMCQGZNPYFVOE",
	"III":  "BDFHJLCPRTXVZNYEIWGAKMUSQO",
	"IV":   "ESOVPZJAYQUIRHXLNFTGKDCMWB",
	"V":    "VZBRGITYUPSDNHLXAWMJQOFECK",
	"VI":   "JPGVOUMFYQBENHZRDKASXLICTW",
	"VII":  "NZJHGRCXMYSWBOUFAIVLPEKQDT",
	"VIII": "FKQHTLXOCBJSPDZRAMEWNIUYGV"
}


def rotor2dict(rotor_string):
	"""
	Converts a rotor string to a dictionary, where each key
	is mapped to the corresponding letter.
	"""
	mapped = {}
	if len(rotor_string) != 26 or not rotor_string.isalpha():
		raise ValueError(f"Bad rotor string: {rotor_string}")

	for n, letter in enumerate(ALPHABET):
		mapped[letter] = rotor_string[n]

	return mapped 


def map_plugboard(plugboard):
	"""
	Returns a dictionary that maps a given letter into another given the
	plugboard. Checks for errors and missing letters are also handled.
	"""
	mapped = {}
	pairs = plugboard.strip().upper().split(" ")
	joined = "".join(pairs)

	if len(joined) > 20:
		raise Exception("Too many pairs in the plugboard!")

	if len(set(joined)) != len(joined):
		raise Exception("Plugboard has letters mapped twice or more")

	for p in pairs:
		if len(p) != 2 or not p.isalpha():
			raise ValueError(f"Bad input pairs format: {p}")
		a, b = p
		mapped[a] = b
		mapped[b] = a

	remaining = list(set(ALPHABET) - set(joined))

	for letter in remaining:
		mapped[letter] = letter

	return mapped


def check_enigma_inputs(rotors, offsets):
	"""
	Checks if rotors and offsets provided are valid inputs
	"""
	size_rot = len(rotors)
	size_off = len(offsets)
	valid = [3, 4]

	if size_rot != size_off or size_rot not in valid or size_off not in valid:
		raise Exception("Rotors/Offsets have the wrong sizes")

	for rot in rotors:
		if not rot.isalpha() or rot.upper() not in ROTORS.keys():
			raise ValueError(f"{rot} is not a valid rotor!")

	for off in offsets:
		if not isinstance(off, int) or not 0 <= off <= 25:
			raise Exception(f"{off} is not a valid offset")

	return


class Enigma(object):
	"""
	This class handles encryption and decryption of messages, given a
	specific setup for the machine. Messages can only contain letters that
	are converted to upper case. Spaces, number, special characters, etc.
	are not supported, thus discarded.

	ARGUMENTS:
	  --> Plugboard: up to 10 groups mapping one letter into another (e.g.
					"ab df gh re ok")
	  --> Rotors: List of roman numerals (strings) representing the rotors ("I",
					"II", ..., "VIII"). Supports three or more rotors up to 4.
					The first element of this list corresponds to the left
					rotor and so on.
	  --> Offsets: List of integers. Must have the same size than 'Rotors' and
					each component ranges between 0 and 25
	"""
	def __init__(self, plugboard: str, rotors: list, offsets: list):
		check_enigma_inputs(rotors, offsets)
