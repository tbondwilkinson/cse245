import argparse
import numpy as np
from decimal import Decimal
from PIL import Image
import math
import matplotlib.pyplot as plt
import random

def ferguson():
	global args
	blackTurnout = 0.16
	whiteTurnout = 0.16
	ferguson = np.genfromtxt(args.ferguson, delimiter=",", dtype='string')
	fergusonVoters = np.empty(ferguson.shape, dtype='object')
	for index, x in np.ndenumerate(ferguson):
		 fergusonVoters[index] = tuple([int(num) for num in x[1:-1].split(" ")])
	for whiteCandidates in xrange(3, 6):
		for blackCandidates in xrange(3, 6):
			blackSeats = 0
			print "Candidates: ", (whiteCandidates, blackCandidates)
			for iteraton in xrange(1000):
				candidates = np.zeros(whiteCandidates + blackCandidates)
				for x in np.nditer(fergusonVoters, flags=('refs_ok',)):
					x = x.item()
					whiteTurnoutRandom = np.random.beta(2, 2.0 / whiteTurnout - 2)
					blackTurnoutRandom = np.random.beta(2, 2.0 / blackTurnout - 2)
					for i in xrange(x[0]):
						if np.random.uniform() < whiteTurnoutRandom:
							if np.random.uniform() < .9:
								for candidate in random.sample(range(whiteCandidates), 3):
									candidates[candidate] += 1
							else:
								for candidate in random.sample(range(whiteCandidates, whiteCandidates + blackCandidates), 3):
									candidates[candidate] += 1
					for i in xrange(x[1]):
						if np.random.uniform() < blackTurnoutRandom:
							if np.random.uniform() < .9:
								for candidate in random.sample(range(whiteCandidates, whiteCandidates + blackCandidates), 3):
									candidates[candidate] += 1
							else:
								for candidate in random.sample(range(whiteCandidates), 3):
									candidates[candidate] += 1
				order = candidates.argsort()
				ranks = order.argsort()
				for i in xrange(whiteCandidates, len(ranks)):
					if ranks[i] - (whiteCandidates + blackCandidates - 4) > 0:
						blackSeats += 1
			print 'Seats over 1000 iterations: ', blackSeats
			blackSeats = 0


	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("ferguson", help="Csv file with voter population")
	args = parser.parse_args()
	ferguson()