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

# Rotors and reflectors used by the German Navy
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
	mapped = {'left':{}, 'right':{}}
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
		mapped[L2POS[a]] = L2POS[b]
		mapped[L2POS[b]] = L2POS[a]

	remaining = list(set(ALPHABET) - set(joined))

	for letter in remaining:
		mapped[L2POS[letter]] = L2POS[letter]

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

	for off, ring in zip(offsets, rings):
		if not isinstance(off, str) or not "A" <= off <= "Z":
			raise Exception(f"{off} is not a valid offset")
		if not isinstance(ring, str) or not "A" <= ring <= "Z":
			raise Exception(f"{ring} is not a valid offset")

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
	  --> Offsets: List of strings. Must have the same size than 'Rotors' and
					each component ranges between A and Z. Adds a initial offset
					on each rotor.
	  --> Rings: List of strings, similar to the Offsets. This option changes
	  				how wires are connected, not changing the order of the
	  				letters that appear at the top of the machine (offsets).
	"""
	def __init__(self, plugboard: str, rotors: list, offsets: list, rings: list):
		check_enigma_inputs(rotors, offsets, rings)
		self.plugboard = map_plugboard(plugboard)

	@staticmethod
	def _message2num(message):
		to_list = list(filter(lambda x: x.isalpha(), message.strip().upper()))

		# Convert to numbers - A:0, B:1, ..., Z:25
		to_list = [L2POS[i] for i in to_list]

		return to_list

	@staticmethod
	def _num2message(numbers):
		return "".join([POS2L[i] for i in numbers])

	def _enc_plugboard(self, message_num):
		"""
		Gets a message represented by a list of integers ranging from 0 to
		25 and applies a substituition cypher.
		"""
		return [self.plugboard[l] for l in message_num]

	def _rotor_right2left(self, rotor, offset, input_letter):
		"""
		Applies a substituition cypher done by the rotor from right to left

		input_letter -> integer that represents the letter
		rotor -> rotor string
		offset -> integer representing the offset (A:0, B:1, ...)
		"""


	def test(self):
		message = "e n i g m_a"
		processed = self._message2num(message)
		print(self._num2message(processed))
		print(processed)
		plug = self._enc_plugboard(processed)
		print(self._num2message(plug))


if __name__ == "__main__":
	enigma = Enigma("ab cd ef gh", ["I", "II", "III"], ["A", "A", "A"], ["A", "A", "A"])
	enigma.test()

