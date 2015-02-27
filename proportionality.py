import argparse
import numpy as np
from decimal import Decimal
from PIL import Image
import math
import matplotlib.pyplot as plt

def proportionality():
	global args
	dataset = np.genfromtxt(args.dataset, delimiter=",", skip_header=1, dtype=int)
	districtDataset = np.genfromtxt(args.dataset2, delimiter=",", skip_header=1, dtype=float)
	districtStates = np.vectorize(lambda s: s[1:-1])(np.genfromtxt(args.dataset2, delimiter=",", skip_header=1, usecols=(1), dtype='string'))
	stateStrings = np.vectorize(lambda s: s[1:-1])(np.genfromtxt(args.dataset, delimiter=",", skip_header=1, usecols=(0), dtype='string'))
	population = np.genfromtxt(args.dataset, delimiter=",", skip_header=1, usecols=(1), dtype=int)
	for i in xrange(stateStrings.shape[0]):
		if population[i] < 0:
			stateStrings[i] = ""
	seatCount = dataset[:,2:4]
	voteCount = dataset[:,4:6]
	stateDistrictVariance = [0.0, 0.0]
	stateVariances = []
	currentState = 0
	totalVotes = float(np.sum(voteCount[currentState]))
	republicanStateVote = voteCount[currentState, 0]
	democraticStateVote = voteCount[currentState, 1]
	numberOfDistricts = 0.0
	for i in xrange(districtDataset.shape[0]):
		if districtStates[i] == 'S':
			stateDistrictVariance[0] /= numberOfDistricts
			stateDistrictVariance[1] /= numberOfDistricts
			stateVariances.append(math.sqrt(stateDistrictVariance[0] + stateDistrictVariance[1]))
			stateDistrictVariance = [0.0, 0.0]
			numberOfDistricts = 0.0
			currentState += 1
			if currentState < voteCount.shape[0]:
				totalVotes = float(np.sum(voteCount[currentState]))
				republicanStateVote = voteCount[currentState, 0]
				democraticStateVote = voteCount[currentState, 1]
			continue
		if republicanStateVote != 0 and districtDataset[i, 2] != 0:
			stateDistrictVariance[0] += (districtDataset[i, 2] / 100.0 - republicanStateVote / totalVotes)**2
		if democraticStateVote != 0 and districtDataset[i, 4] != 0:
			stateDistrictVariance[1] += (districtDataset[i, 4] / 100.0 - democraticStateVote / totalVotes)**2
		numberOfDistricts += 1

	
	seatVariances = np.zeros(seatCount.shape[0], dtype=float)
	for i in xrange(seatVariances.shape[0]):
		totalSeats = np.sum(seatCount[i])
		totalVotes = np.sum(voteCount[i])
		if totalVotes == 0 or totalSeats == 0:
			continue
		seatVariances[i] = math.sqrt(((voteCount[i, 0] / float(totalVotes) * totalSeats - seatCount[i, 0])/totalSeats)**2 + ((voteCount[i, 1] / float(totalVotes) * totalSeats - seatCount[i, 1])/totalSeats)**2)
	seatVariancesSmall = [seatVariances[i] for i in xrange(50) if stateStrings[i] != ""]
	stateVariancesSmall = [stateVariances[i] for i in xrange(50) if stateStrings[i] != ""]
	stateStringsSmall = [stateString for stateString in stateStrings if stateString != ""]
	stateVariances, seatVariances, stateStrings = (list(t) for t in zip(*sorted(zip(stateVariances, seatVariances, stateStrings))))
	plt.plot(stateVariances, seatVariances, 'o')
	i = 0
	for xy in zip(stateVariancesSmall, seatVariancesSmall):
		plt.annotate(stateStringsSmall[i], xy=(xy[0] + 0.01, xy[1]), xytext=(0, 0), textcoords='offset points')
		i += 1
	z = np.polyfit(stateVariances, seatVariances, 1)
	p = np.poly1d(z)
	plt.plot(stateVariances, p(stateVariances),"r-")
	plt.xlabel('Standard Deviation of District Vote Share vs State Vote Share')
	plt.ylabel('Standard Deviation of State Vote Share vs Seat Allocation')
	plt.show()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset", help="Csv file with seats and votes")
	parser.add_argument("dataset2", help="Csv file with district votes")
	args = parser.parse_args()
	proportionality()