import random as rm
import graph as G

# Initialize graph of cities as adjacency matrix
'''
graphofcities = [[0, 2, 2, 5, 7],
                 [2, 0, 4, 1, 2],
                 [2, 4, 0, 1, 3],
                 [5, 1, 1, 0, 2],
                 [7, 2, 3, 2, 0]]
                 # Optimum tour: 0-1-4-3-2-0 cost: 9

'''
'''
graphofcities = [[0, 10, 24,  7,  6, 12, 12,  9, 23,  1],
                 [10, 0, 17, 12,  5, 14,  7, 22,  2, 24],
                 [24, 17, 0, 23, 23,  4,  7, 19, 20, 25],
                 [ 7, 12, 23, 0, 18, 10, 15, 14,  2,  7],
                 [ 6,  5, 23, 18, 0, 10, 18,  8,  2,  6],
                 [12, 14,  4, 10, 10, 0,  8,  6, 14, 20],
                 [12,  7,  7, 15, 18,  8, 0, 18,  7,  5],
                 [ 9, 22, 19, 14,  8,  6, 18, 0, 10,  2],
                 [23,  2, 20,  2,  2, 14,  7, 10, 0, 15],
                 [ 1, 24, 25,  7,  6, 20,  5,  2, 15, 0]]
                 # optimum tour cost: 43
'''

graphofcities = G.graph

def calcTourCost(toursequence):
	tourcost = 0

	for i in range(len(toursequence)-1):
		# print (graphofcities[ toursequence[i] ][ toursequence[i+1] ])
		tourcost = tourcost + graphofcities[ toursequence[i] ][ toursequence[i+1] ]

	tourcost = tourcost + graphofcities[ toursequence[-1] ][ toursequence[0] ]          # to complete the cycle
	return tourcost


def SO(list2swap,swaptuple):   # swap operator
	'''
	'swapindextuple' is the tuple of indices to swap from list2swap
	'''
	list2swap[swaptuple[0]], list2swap[swaptuple[1]] = list2swap[swaptuple[1]], list2swap[swaptuple[0]]
	return list2swap


def SS(tlist,SOlist):
	'''
	Applies 'plus' operation 
	'SOlist' is the list of swap operator tuples
	'''
	for SOtuple in SOlist:
		tlist = SO(tlist, SOtuple)
		#print ("after apply first SO",SOtuple,"above list:",tlist)

	return tlist



def initializeparticles(n_particles):
	'''
	Each particle is a potential solution in the form of a tuple of 3 lists.
	A particle is vivualized as a dictionary consiting of following fields
	"currpos": list for current iteration position (a tour around the cities)
	"currcost": current position cost of particle 
	"vel": velocity (Swap Sequence) i.e. list of swap tuples
	"bestpos": tour list of best position attained by the particle in all previous iterations
	"bestcost": best tour cost for the particle
	'''
	n_cities = len(graphofcities[0])
	print ("Number of cities:",n_cities)
	listofparticles = []
	for i in range(n_particles):                                  
		pos = rm.sample(range(0,n_cities),n_cities)      # initialize random position
		bestpos = rm.sample(range(0,n_cities),n_cities)  # initialize random best position for the particle
		
		vel = []
		for i in range(4):                                    # initialize random velocity sequence for every particle
			vel.append( (rm.choice(range(0,n_cities)), rm.choice(range(0,n_cities)) ) )
		# formulate the dictionary of initialized particle
		particle = {"currpos":pos,"currcost":calcTourCost(pos),"vel":vel,"bestpos":bestpos,"bestcost":calcTourCost(bestpos) }
		listofparticles.append( particle)
	return listofparticles


def displayparticles(listofparticles):
	for i in range(len(listofparticles)):
		print ("\nParticle ",i,": Position:",listofparticles[i]["currpos"], "current tour cost:",listofparticles[i]["currcost"],"\nTour Best:",listofparticles[i]["bestpos"], "Cost of Tour Best:", listofparticles[i]["bestcost"])


def tourpositionsubtract(tourpos1, tourpos2):
	'''
	Applies '-' i.e. subtraction operator. This function computes edit distance
	Finds a Basic swap sequence which applied on tourpos2 will give tourpos1
	'''
	toursubtractSS = []
	for i in range(len(tourpos1)):
		pos = tourpos2.index( tourpos1[i] )

		if (i != pos):
			swapop = ( i,pos )
			toursubtractSS.append( swapop )
			tourpos2 = SO(tourpos2,swapop)

	return toursubtractSS

def computeG(listofparticles):
	# returns dictionary of Best tour and cost found amongst all particles
	seq = [ (x["bestpos"],x["bestcost"]) for x in listofparticles ] 
	tour, cost = min( seq, key = lambda t:t[1] )
	Best = {"tour":tour,"cost":cost}
	assert ( Best["cost"] == calcTourCost( Best["tour"] ))    # cross checking code
	return Best


def partialsearch(tourpos, vel):
	min_cost = 1000
	cost = 0
	min_cost_tour = []


	for i in vel:
		#print ("Applying operator",i)
		t = SO( tourpos, i )
		cost = calcTourCost( t )
		if (cost < min_cost):
			min_cost = cost
			min_cost_tour = t.copy()

	return min_cost_tour,min_cost

def sanity_check(particle):

	if ( particle["bestcost"] >  particle["currcost"] ) :
		# swap current and best position
		particle["bestpos"], particle["currpos"] = particle["currpos"],particle["bestpos"]

		# swap current and best costs
		particle["bestcost"], particle["currcost"] = particle["currcost"], particle["bestcost"]
	return particle

