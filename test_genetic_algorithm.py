if __name__ == "__main__":
    from map_file_reader import MapFileReader
    from solver import GASolver
    from visualizer import Visualizer2d
    
    reader = MapFileReader("input/tsp_static_obstacles_2.txt")
    
    map2d = reader.readMap2d()
    
    solver = GASolver(num_generations=500, num_of_parents=200, sol_per_pop=700, mutation_probability=(0.8,0.2))
    solution = map2d.solvedBy(solver=solver)
    solution.showToConsole()
    
    visualizer = Visualizer2d(map=map2d, solution=solution, speed = 100)
    visualizer.visualize2d()