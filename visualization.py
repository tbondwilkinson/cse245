import argparse
import numpy as np
from decimal import Decimal
from PIL import Image
import matplotlib.pyplot as plt

def fergusonImage():
	global args
	ferguson = np.genfromtxt(args.ferguson, delimiter=",", dtype='string')
	fergusonVoters = np.empty(ferguson.shape, dtype='object')
	for index, x in np.ndenumerate(ferguson):
		 fergusonVoters[index] = tuple([int(num) for num in x[1:-1].split(" ")])
	fergusonImage = np.zeros((fergusonVoters.shape[0], fergusonVoters.shape[1], 3), dtype=np.uint8)
	for index, votes in np.ndenumerate(fergusonVoters):
		if votes[0] + votes[1] == 0:
			fergusonImage[index] = [200, 50, 50]
			continue
		percentage = float(votes[0] - votes[1]) / float(votes[0] + votes[1])
		fergusonImage[index] = int(127 + 128.0 * percentage)
	plt.imshow(fergusonImage, interpolation='nearest')
	plt.savefig(args.outImageFile)
	fergusonHistWhite = []
	fergusonHistBlack = []
	for index, votes in np.ndenumerate(fergusonVoters):
		if votes[0] + votes[1] == 0:
			continue
		squaredDiff = (float(votes[0] - votes[1]) / float(votes[0] + votes[1]))**1
		if votes[0] < votes[1]:
			fergusonHistBlack.append(squaredDiff)
		elif votes[0] > votes[1]:
			fergusonHistWhite.append(squaredDiff)
	plt.clf()
	plt.hist(fergusonHistBlack, bins=20, histtype='stepfilled', color='black', alpha=0.8, label="Black")
	plt.hist(fergusonHistWhite, bins=20, histtype='stepfilled', color='white', alpha=0.7, label='White')
	plt.title("Comparison of Segregation in Primarily Black and White Districts")
	plt.xlabel('Percent Difference')
	plt.legend()
	plt.gca().set_axis_bgcolor((.8, .8, .8))
	plt.savefig(args.outHistFile)
	print len(fergusonHistBlack)
	print len(fergusonHistWhite)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("ferguson", help="Ferguson csv file")
	parser.add_argument("outImageFile", help="Output image file")
	parser.add_argument("outHistFile", help="Output for histogram image file")
	args = parser.parse_args()
	fergusonImage()