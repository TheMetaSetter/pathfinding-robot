if __name__ == "__main__":
    from map_file_reader import MapFileReader
    from solver import DijkstraSolver
    from visualizer import Visualizer2d
    
    reader = MapFileReader("input/long_path.txt")
    
    map2d = reader.readMap2d()
    
    solver = DijkstraSolver()
    solution = map2d.solvedBy(solver=solver)
    solution.showToConsole()
    
    visualizer = Visualizer2d(map=map2d, solution=solution)
    visualizer.visualize2d()