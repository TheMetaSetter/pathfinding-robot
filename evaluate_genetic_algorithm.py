# NOTICE: Uncomment the last line in the file solver.py before running this code.

import threading
import numpy as np

if __name__ == "__main__":
    from map_file_reader import MapFileReader
    from solver import GASolver
    import numpy as np
    import matplotlib.pyplot as plt

    # Read the map file
    map_file_reader = MapFileReader("input_tsp/tsp_static_obstacles_2.txt")
    
    # Read the map
    map = map_file_reader.readMap2d()
    
    # Initialize the genetic algorithm solver
    ga_solver = GASolver(num_generations=300, num_of_parents=200, sol_per_pop=2000, mutation_probability=(0.8,0.2))
    
    # Solve the TSP problem
    solution, generations_averages, generations_bests = map.solvedBy(ga_solver)
    
    # Plot the generations_averages on a plot
    plt.plot(generations_averages)
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.title('Average Fitness of Generations')
    plt.savefig('average_fitness.png')
    
    # Clear the plot
    plt.clf()
    
    # Plot the generations_bests on a plot
    plt.plot(generations_bests)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.title('Best Fitness of Generations')
    plt.savefig('best_fitness.png')