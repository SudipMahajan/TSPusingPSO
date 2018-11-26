import numpy as np
import psofortspmodule as PSO

'''
TSP problem is to find minimum cost Hamiltonian Cycle in the graph
All functions and TSP graph are initialized in user defined module 'psofortspmodule.py'
This code assumes TSP graph to be a complete graph, so while calculating TSP tour, it is understood that
last node is same as first, so last node is NOT considered explicitly
'''

############################################### START OF CODE #######################################

## STEP 1: Initialization
print ("TSP graph created...")

listofparticles = PSO.initializeparticles(n_particles = 5)
print ("Particles initialized to compute TSP tour")

# PSO.displayparticles(listofparticles)
GlobalBest = PSO.computeG(listofparticles)
print ("\n ******Initial Global Best tour:",GlobalBest["tour"], ",with cost :",GlobalBest["cost"],"****** \n")

n_iter = 5

## STEP 2
for iter in range(n_iter):

	iterglobal = {}    # dictionary to store best tour path and cost every iteration
	print ("\nIteration:",iter)
## STEP 3

	for particle in listofparticles:   # For all particles 
	
		# COMPUTE A = Pid (Previous best tour found by a particle) - X (Current tour position of particle)
		A = PSO.tourpositionsubtract( particle["bestpos"].copy(), particle["currpos"].copy() )
		assert ( PSO.SS( particle["currpos"].copy(), A ) == particle["bestpos"].copy() )      # cross checking

		# COMPUTE B = Gid (Previous best achieved by any particle) - X (Current tour position)
		B = PSO.tourpositionsubtract( GlobalBest["tour"].copy(), particle["currpos"].copy() )
		assert ( PSO.SS( particle["currpos"].copy(), B ) == GlobalBest["tour"].copy() )      # cross checking

		# Calculate new Velocity Vid = Vid (Previous iteration velocity) + alpha * A + beta * B; 
		# where alpha & beta are randomly generated values between zero and one, '+' is concatenation operator implemented by 'extend'
		alpha = np.random.random()
		beta = np.random.random()
		if ( alpha > 0.7 ):
			particle["vel"].extend(A)   
		if ( beta > 0.7 ):
			particle["vel"].extend(B)


		# Calculate new current tour Position using Xid = Xid + Vid and corresponding cost
		particle["currpos"] = PSO.SS( particle["currpos"] , particle["vel"] )
		particle["currcost"] = PSO.calcTourCost( particle["currpos"] )
		assert ( particle["currcost"] == PSO.calcTourCost( particle["currpos"] ) ),( particle["currcost"], PSO.calcTourCost( particle["currpos"]) )    # cross checking code

		# Implement partial search to compute new position of particle, VTPSO paper implementation
		particle["currpos"], particle["currcost"] = PSO.partialsearch(particle["currpos"],particle["vel"])


		# Update 'P'i.e best tour for particle if current tour is better than stored best tour
		if ( ( particle["currcost"] < particle["bestcost"] ) & ( particle["bestcost"] > particle["currcost"] )) :
			particle["bestpos"] = particle["currpos"]
		particle["bestcost"] = PSO.calcTourCost( particle["bestpos"] )

		particle = PSO.sanity_check(particle)                 # additional cross checking code

		assert ( particle["bestcost"] == PSO.calcTourCost( particle["bestpos"] ) ),particle    # cross checking code
		assert ( particle["bestcost"] <= particle["currcost"] ),particle                       # cross checking code
    # inner FOR loop ends, updating particle postions and velocities is over

	PSO.displayparticles(listofparticles)
	iterglobal =  PSO.computeG(listofparticles)  # best tour found in current iteration
	print ( "\n** Global Best Tour:",GlobalBest["tour"],"with Cost:",GlobalBest["cost"] )
	assert ( iterglobal["cost"] == PSO.calcTourCost( iterglobal["tour"] ))    # cross checking code

## STEP 4 
# Update Global tour if required
	if ( iterglobal["cost"] < GlobalBest["cost"] ):
		GlobalBest = iterglobal.copy()

	assert ( GlobalBest["cost"] <= iterglobal["cost"] ),( GlobalBest,iterglobal )   # cross checking code
### End of outer FOR Loop, represents ITERATIONS



print ("\n\n After all iterations:\n Global Best tour",GlobalBest["tour"],"with cost:",GlobalBest["cost"])
############################################# END OF CODE ################################################
