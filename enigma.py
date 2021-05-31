##
##  Class for encrypting/decrypting Enigma messages
##  
##	This code aims to simulate a Enigma M3 (1934) or
##	M4 (1942), both used by the German Navy supporting
##	up to four rotors and the ring configuration + plugboard.
##
##	Check the outputs at https://cryptii.com/pipes/enigma-machine
##

from utils import ALPHABET, L2POS, POS2L
from utils import ROTORS, REFLECTORS, TURNS

from utils import map_plugboard
from utils import check_enigma_inputs
from utils import get_rotors
from utils import get_reflector
from utils import print_output
from utils import message2num
from utils import num2message


class Enigma(object):
	"""
	This class handles encryption and decryption of messages, given a
	specific setup for the machine. Messages can contain any latin
	ans special characters, although, during the encryption process,
	special characters and spaces will be ignored and accents will
	be removed.

	Supports both M3 and M4 "Shark" versions of Enigma. The latter
	only works with thin reflectors and the fourth rotor must be Beta
	or Gamma.

	ARGUMENTS:
	  --> Plugboard: up to 10 groups mapping one letter into another (e.g.
					"ab df gh re ok"). Defaults to no plugboard (= None)
	  --> Rotors: List of roman numerals (strings) representing the rotors ("I",
					"II", ..., "VIII"). Supports three or more rotors up to 4.
					The first element of this list corresponds to the left
					rotor and so on. Defaults to ["I", "II", "III"]
	  --> Reflector: Reflector name as a String. Supports "A", "B" and "C".
	  				Defaults to "B"
 	  --> Offsets: String. Must have the same size than 'Rotors' and
					each component ranges between A and Z. Adds a initial offset
					on each rotor. Default is "AAA"
	  --> Rings: String, similar to the Offsets. This option changes
	  				how wires are connected, not changing the order of the
	  				letters that appear at the top of the machine (offsets).
	  				Defaults to "AAA"
	"""
	def __init__(self, plugboard: str=None, rotors: list=["I", "II", "III"],
						reflector: str="B", offsets: list="AAA",
						rings: list="AAA", *args, **kwargs):
		check_enigma_inputs(rotors, reflector, offsets, rings)
		self.plugboard = map_plugboard(plugboard)
		self.rotors    = get_rotors(rotors)
		self.reflector = get_reflector(reflector)
		self.offsets   = [L2POS[letter] for letter in offsets]
		self.rings     = [L2POS[letter] for letter in rings]

		self.n_rotors  = len(rotors)
		self.refl_name = reflector
		self.rotors_n  = [r.strip().upper() for r in rotors]

		self.start_off = self.offsets.copy()

		self.dble_turn = False

	def __str__(self):
		mode = "M3" if self.n_rotors == 3 else "M4 Shark"
		name = f"Enigma {mode}\n"
		rots = f" - Rotors (left -> right): {', '.join(self.rotors_n)}\n"
		refl = f" - Reflector: {self.refl_name}\n"
		offs = f" - Initial Rotor Settings: {''.join([POS2L[i] for i in self.offsets])}\n"
		plug = [POS2L[h] + POS2L[k] for h, k in self.plugboard.items() if h != k]
		plug = ' '.join(list(set(["".join(sorted(i)) for i in plug])))
		plug = f" - Plugboard: {'None' if plug == '' else plug}\n"
		ring = f" - Ring Configuration: {''.join([POS2L[i] for i in self.rings])}\n"
		return name + rots + refl + offs + plug + ring

	def set(self, plugboard=None, rotors=None, reflector=None, offsets=None,
						rings=None):
		"""
		Changes the Enigma Machine configuration. This method does not check
		if the arguments are valid, so be careful.
		"""
		if plugboard is not None:
			self.plugboard = map(plugboard)
		if rotors is not None:
			self.rotors    = get_rotors(rotors)
			self.n_rotors  = len(rotors)
			self.rotors_n  = [r.strip().upper() for r in rotors]
		if reflector is not None:
			self.reflector = get_reflector(reflector)
			self.refl_name = reflector
		if offsets is not None:
			self.offsets   = [L2POS[letter] for letter in offsets]
		if rings is not None:
			self.rings     = [L2POS[letter] for letter in rings]

	def reset(self):
		"""
		Resets the machine to the starting configuration, so it can be
		used to decrypt the messages
		"""
		self.offsets = self.start_off.copy()

	def _enc_plugboard(self, message_num):
		"""
		Gets a message represented by a list of integers ranging from 0 to
		25 and applies a substituition cypher.
		"""
		return [self.plugboard[l] for l in message_num]
	
	def _turn_rotors(self):
		"""
		Always turns the right (fast) rotor and accounts to multiple
		rotations - when the letter shown by the second rotor from the right
		is the notch letter.
		"""
		if self.dble_turn:
			self.offsets[-2] = (self.offsets[-2] + 1) % len(ALPHABET)
			self.offsets[-3] = (self.offsets[-3] + 1) % len(ALPHABET)
			self.dble_turn = False

		for i in range(-1, -4, -1):
			if POS2L[self.offsets[i]] not in TURNS[self.rotors_n[i]]:
				self.offsets[i] = (self.offsets[i] + 1) % len(ALPHABET)
				if i == -2 and POS2L[self.offsets[i]] in TURNS[self.rotors_n[i]]:
					self.dble_turn = True
				break

			self.offsets[i] = (self.offsets[i] + 1) % len(ALPHABET)

	@staticmethod
	def _rotor_right2left(rotor, input_letter, offset, ring):
		"""
		Applies a substituition cypher done by the rotor from right to left

		input_letter -> integer that represents the letter
		rotor -> rotor as a list of integers
		offset -> integer representing the offset (A:0, B:1, ...)
		ring -> ring integer
		"""
		alpha_size = len(ALPHABET)
		return (rotor[(input_letter + offset - ring) % alpha_size] - offset +\
					ring) % alpha_size

	@staticmethod
	def _reflect(reflector, input_letter):
		"""
		Given a reflector dictionary and an integer representation of the
		input letter, returns the reflected letter as an integer
		"""
		return reflector[input_letter]

	@staticmethod
	def _rotor_left2right(rotor, input_letter, offset, ring):
		"""
		Applies a substituition cypher done by the rotor from left to right

		input_letter -> integer that represents the letter
		rotor -> rotor as a list of integers
		offset -> integer representing the offset (A:0, B:1, ...)
		ring -> ring integer
		"""
		letter = (input_letter + offset - ring) % len(ALPHABET)
		return (rotor.index(letter) - offset + ring) % len(ALPHABET)

	def _forward(self, letter):
		"""
		Executes a forward pass through all the rotors from right to left
		Returns the encrypted letter as an integer
		"""
		self._turn_rotors()
		l = letter
		for i in range(-1, -self.n_rotors - 1, -1):
			l = self._rotor_right2left(self.rotors[i], l, self.offsets[i],
									self.rings[i])
		return l

	def _backwards(self, letter):
		"""
		Given the letter returned by the reflector, executes a backward pass,
		cyphering the input letter in all rotors from left to right
		Returns the output letter as an integer
		"""
		l = letter
		for i in range(self.n_rotors):
			l = self._rotor_left2right(self.rotors[i], l, self.offsets[i],
									self.rings[i])
		return l

	def encrypt(self, text):
		"""
		Pre-process text, executes a forward, reflection and backward pass and
		outputs the encrypted text as a string of capital letters
		"""
		clean_text = message2num(text)
		encrypted = []
		plug = self._enc_plugboard(clean_text)

		for letter in plug:
			l = self._forward(letter)
			l = self._reflect(self.reflector, l)
			l = self._backwards(l)
			encrypted.append(l)

		encrypted = self._enc_plugboard(encrypted)
		encrypted = "".join(POS2L[l] for l in encrypted)

		return encrypted

	def decrypt(self, text):
		"""
		Decrypts text. The configuration should be the same as the initial
		configuration used by the machine for encryption. Use the reset
		method to reset the offsets if necessary.
		"""
		if self.offsets != self.start_off:
			raise Exception("Current offset != starting offset. Use the reset"+\
							" method before decrypting.")
		return self.encrypt(text)


if __name__ == "__main__":
	enigma = Enigma(plugboard="bq cr di ej kw mt os px uz gh",
					rotors=["Gamma", "V", "II", "III"],
					reflector="B_thin",
					offsets="GKDT",
					rings="HAAA")

	print(enigma)

	txt = "By 1930, the Reichswehr had suggested that the Navy adopt their"+\
			" machine, citing the benefits of increased security (with the"+\
			" plugboard) and easier interservice communications.[49] The"+\
			" Reichsmarine eventually agreed and in 1934[50] brought into"+\
			" service the Navy version of the Army Enigma, designated"+\
			" Funkschlüssel ' or M3. While the Army used only three rotors at"+\
			" that time, the Navy specified a choice of three from a possible five"

	enc = enigma.encrypt(txt)

	print(f"Input text:")
	print(txt + '\n')

	print(f"Formatted text:")
	print(num2message(message2num(txt)), '\n')

	print("Encrypted")
	print_output(enc, 4, 6)

	print()

	print("Resetting\n")
	enigma.reset()

	print("Decrypted")
	print_output(enigma.decrypt(enc), 4, 6)

