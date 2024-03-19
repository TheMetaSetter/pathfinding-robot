# NOTICE: Comment the last line in the file solver.py before running this code.

if __name__ == "__main__":
    try:
        from map_file_reader import MapFileReader
        from solver import GASolver
        from visualizer import Visualizer2d
        
        reader = MapFileReader("input_tsp/tsp_static_obstacles_3.txt")
        
        map2d = reader.readMap2d()
        
        solver = GASolver(num_generations=250, num_of_parents=100, sol_per_pop=1500, mutation_probability=(0.8,0.2))
        solution = map2d.solvedBy(solver=solver)
        solution.showToConsole()
        
        visualizer = Visualizer2d(map=map2d, solution=solution, speed = 100)
        visualizer.visualize2d()
    except Exception as ex:
        print("Error: ", ex)