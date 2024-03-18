if __name__ == "__main__":
    from map_file_reader import MapFileReader
    from solver import GASolver
    from visualizer import Visualizer2d
    
    reader = MapFileReader("input/tsp_static_obstacles.txt")
    
    map2d = reader.readMap2d()
    
    solver = GASolver()
    solution = map2d.solvedBy(solver=solver)
    solution.showToConsole()
    
    visualizer = Visualizer2d(map=map2d, solution=solution)
    visualizer.visualize2d()