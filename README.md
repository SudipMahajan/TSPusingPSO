# TSPusingPSO
This repository contains an implementation of Particle Swarm Optimization to solve Traveling Salesman Problem

The PSO variant used in code is Velocity-Tentative PSO presented in following paper:
https://www.researchgate.net/publication/279948232_Velocity_Tentative_PSO_An_Optimal_Velocity_Implementation_based_Particle_Swarm_Optimization_to_Solve_Traveling_Salesman_Problem

It is essential to read following paper for understanding first application of PSO for solving TSP Problem:
https://www.researchgate.net/publication/4052712_Particle_swarm_optimization_for_traveling_salesman_problem

'TSPusingsspso.py' is main python implementation file which needs to be run.
All functions and TSP graph are implemented in the user-defined module
'psofortspmodule.py' which is imported in 'TSPusingsspso.py'

TSP problem is initialized for 10 cities, with an optimum tour cost of 43.

Code implemented and maintained by Sudip Mahajan; email: sudipcmahajan@gmail.com
