##
##	Module with functions to crack the Enigma Machine (M3)
##	using brute force + Index of Coincidence (IoC)
##

from utils import process_text
from utils import IoC
from utils import message2num
from utils import num2message
from utils import print_output
from utils import ALPHABET

from enigma import Enigma

from itertools import permutations
from itertools import product

from argparse import ArgumentParser as parser

import multiprocessing
import time
import progressbar
import bisect


class Configuration(object):
	"""
	Class to define a specific Enigma Machine configuration and
	store the calculated IoC for a specific decrypted text.
	
	The comparison operators between Configuration objects
	works accordingly to the values of the attribute iofc,
	and are meant to be used only to select those configurations
	that outputs the highest Index of Coincidence.
	"""
	def __init__(self, plugboard=None, rotors=None, reflector=None,
						offsets=None, rings=None, ioc=0.0):
		self.plugboard = plugboard
		self.rotors    = rotors
		self.reflector = reflector
		self.offsets   = offsets
		self.rings     = rings
		self.ioc       = ioc

	def __str__(self):
		name = "Enigma Configuration\n"
		rots = f"Rotors: {', '.join(self.rotors)}\n"
		refl = f"Reflector: {self.reflector}\n"
		offs = f"Offsets: {self.offsets}\n"
		ring = f"Rings: {self.rings}"
		iofc = f"Index of Coincidence: {self.ioc:.5f}\n"
		return name + rots + refl + offs + ring + iofc

	def __lt__(self, other):
		return self.ioc < other.ioc

	def __gt__(self, other):
		return self.ioc > other.ioc

	def __le__(self, other):
		return self.ioc <= other.ioc

	def __ge__(self, other):
		return self.ioc >= other.ioc

	def __eq__(self, other):
		return self.ioc == other.ioc

	def __ne__(self, other):
		return self.ioc != other.ioc


def aux_get_offset(params):
	return get_offsets(*params)


def get_offsets(enc_txt, enigma, rotors, n, *args):
	"""
	Given an Enigma Machine with a specific reflector, returns
	the offsets that maximizes the IoC
	"""
	print(f"Finding offsets for rotors = {', '.join(rotors)}")

	best = [Configuration()] * n

	# Test every offset configuration
	for off in product(ALPHABET, repeat=3):
		offsets, rots = "".join(off), list(rotors)

		enigma.set(rotors=rots, offsets=offsets)
		decrypted = enigma.encrypt(enc_txt)

		ioc = IoC(decrypted)
		cfg = Configuration(rotors=rots, offsets=offsets,
							reflector=enigma.refl_name, ioc=ioc)

		bisect.insort_left(best, cfg)
		best.pop(0)

	return best


def get_best_rot_off(enc_txt, possible_rotors=["I", "II", "III"],
						reflector="B", n=5, n_cpu=4):
	"""
	enc_txt: encrypted text - only uppercase letters
	possible_rotors: list of rotors that will be tested (see utils module)
	reflector: reflector to be used (see utils module)
	n: number of configurations that will be returned

	Returns a list of n Configurations that output the highest
	IoC values
	"""
	pool = multiprocessing.Pool(processes=n_cpu)

	args = [[enc_txt, Enigma(reflector=reflector), list(i), n] for \
						i in permutations(possible_rotors, 3)]

	best = pool.map(aux_get_offset, args)

	best = [j for i in best for j in i]
		
	return sorted(best)[-n:]


if __name__ == "__main__":
	enigma = Enigma(plugboard="bq cr di hj kp",
					rotors=["II", "III", "I"],
					reflector="B",
					offsets="RHD",
					rings="AAA")

	print(enigma)

	txt = "The index of coincidence is useful both in the analysis of natural-"+\
			"language plaintext and in the analysis of ciphertext (cryptanalys"+\
			"is). Even when only ciphertext is available for testing and plain"+\
			"text letter identities are disguised, coincidences in ciphertext "+\
			"can be caused by coincidences in the underlying plaintext. This t"+\
			"echnique is used to cryptanalyze the Vigenère cipher, for example"+\
			". For a repeating-key polyalphabetic cipher arranged into a matri"+\
			"x, the coincidence rate within each column will usually be highes"+\
			"t when the width of the matrix is a multiple of the key length, a"+\
			"nd this fact can be used to determine the key length, which is th"+\
			"e first step in cracking the system. Coincidence counting can hel"+\
			"p determine when two texts are written in the same language using"+\
			" the same alphabet. (This technique has been used to examine the "+\
			"purported Bible code). The causal coincidence count for such text"+\
			"s will be distinctly higher than the accidental coincidence count"+\
			" for texts in different languages, or texts using different alpha"+\
			"bets, or gibberish texts."

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

	cfgs = get_best_rot_off(enc, n=10, n_cpu=6)

	for cfg in cfgs:
		print(cfg)

