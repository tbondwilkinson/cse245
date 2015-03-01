#!/usr/bin/env python
"""
Plotting
"""
import numpy as np
import matplotlib.pyplot as plt

# plt.plot([, .145, .15, .155, .16, .165, .17, .175, .18, .185, .19], [10, 58, 278, 566, 1084, 1830, 2455, 2687, 2940, 2979, 2991])
# plt.title('Black Seats and Turnout')
# plt.ylabel('Seats Won Over 1000 Iterations')
# plt.xlabel('Black Voter Turnout')

# plt.show()

N = 3
blackSeatsThree = (1170, 3000, 3000)
blackSeatsFour = (0, 1108, 3000)
blackSeatsFive = (0, 0, 1263)

ind = np.arange(N)  # the x locations for the groups
width = 0.20       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, blackSeatsThree, width, color='r')
rects2 = ax.bar(ind+width, blackSeatsFour, width, color='y')
rects3 = ax.bar(ind+width+width, blackSeatsFive, width, color='g')

# add some text for labels, title and axes ticks
ax.set_ylabel('Number of Black Seats Over 1000 Iterations')
ax.set_xlabel('Number of White Candidates')
ax.set_title('Black Seats For Different Candidate Numbers')
ax.set_xticklabels(('3', '4', '5'))
ax.set_xticks(ind + width + width / 2.0)
ax.set_ylim([0, 5000])

ax.legend((rects1[0], rects2[0], rects3[0]), ('3 Black Candidates', '4 Black Candidates', '5 Black Candidates') )

plt.show()