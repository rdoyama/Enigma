##
## Useful Functions and variables
##


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Letter to integer position (0-based) and vice-versa
L2POS = {letter: i for i, letter in enumerate(ALPHABET)}
POS2L = {i: letter for i, letter in enumerate(ALPHABET)}

# Rotors and reflectors used by the German Navy. Only the most common
# reflectors are implemented
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

REFLECTORS = {
	"A": "EJMZALYXVBWFCRQUONTSPIKHGD",
	"B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
	"C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}

# Turning points for each rotor. If the rotor steps from any of these
# letters to the next, the next rotor advances
TURNS = {
	"I":    ["Q"],
	"II":   ["E"],
	"III":  ["V"],
	"IV":   ["J"],
	"V":    ["Z"],
	"VI":   ["Z", "M"],
	"VII":  ["Z", "M"],
	"VIII": ["Z", "M"]
}


def map_plugboard(plugboard):
	"""
	Returns a dictionary that maps a given letter into another given the
	plugboard. Checks for errors and missing letters are also handled.
	"""
	if plugboard is None:
		return {i:i for i in range(len(ALPHABET))}
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


def check_enigma_inputs(rotors, reflector, offsets, rings):
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

	if reflector.upper() not in REFLECTORS.keys():
		raise ValueError(f"{reflector} is not a valid reflector")

	for off, ring in zip(offsets, rings):
		if not isinstance(off, str) or not "A" <= off <= "Z":
			raise Exception(f"{off} is not a valid offset")
		if not isinstance(ring, str) or not "A" <= ring <= "Z":
			raise Exception(f"{ring} is not a valid offset")

	return


def get_rotors(rotors):
	"""
	Receives a list of strings with roman numerals denoting the
	rotors and return a list of lists, each one with the numbers
	representing the position of the letters in the alphabet
	"""
	rts = []
	for r in rotors:
		rts.append([L2POS[l] for l in ROTORS[r]])

	return rts


def get_reflector(reflector):
	"""
	Receives a string with the name of the reflector and returns
	a dictionary where each key is mapped to its corresponding
	letter
	"""
	mapped = {}
	for i, letter in enumerate(ALPHABET):
		mapped[L2POS[letter]] = L2POS[REFLECTORS[reflector][i]]

	return mapped


def message2num(message):
	to_list = list(filter(lambda x: x.isalpha(), message.strip().upper()))

	# Convert to numbers - A:0, B:1, ..., Z:25
	to_list = [L2POS[i] for i in to_list]

	return to_list

def num2message(numbers):
	return "".join([POS2L[i] for i in numbers])


def print_output(string, wlen=5, max_cols=5):
	"""
	Prints the input string in a more readable format,
	where each row has up to max_cols words of wlen letters
	"""
	sz = len(string)
	r = sz % wlen
	nwords = (sz // wlen) + 1 if r != 0 else sz // wlen
	start = nwords

	while nwords:
		last = min(nwords, max_cols)
		for i in range(last):
			s, e = (start - nwords) * wlen, (start - nwords + 1) * wlen
			if i == last - 1:
				print(string[s:e])
			else:
				print(string[s:e], end="  ")
			nwords -= 1