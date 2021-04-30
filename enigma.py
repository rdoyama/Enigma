##
##  Functions for encrypt/decrypt
##  Enigma messages
##


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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


class Enigma:
	"""
	--> Plugboard: up to 10 groups mapping one letter into another (e.g.
					"ab df gh re ok")
	--> Rotors: String in Roman Numerals
	"""
	def __init__(self, plugboard, rotor1, rotor2, rotor3, rotor4=None, rotor5=None):
		pass
