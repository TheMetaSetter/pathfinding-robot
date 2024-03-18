import threading

if __name__ == "__main__":
    from map_file_reader import MapFileReader
    from solver import GASolver
    import numpy as np
    import matplotlib.pyplot as plt

    map_file_reader = MapFileReader("input/tsp_static_obstacles_2.txt")
    map = map_file_reader.readMap2d()
    
    solver = GASolver(num_generations=500, num_of_parents=200, sol_per_pop=700, mutation_probability=(0.8,0.2))
    
    solution, generations_averages, generations_bests = map.solvedBy(solver)
    
    plt.plot(generations_bests)
    plt.xlabel('Generation')
    plt.ylabel('Fitness Value')
    plt.title('Best Fitness Value of Each Generation')
    plt.show()