if __name__ == "__main__":
    try:
        from map_file_reader import MapFileReader
        from solver import GBFS_Solver
        from visualizer import Visualizer2d
        
        reader = MapFileReader("input_basic/ordinary_path.txt")
        
        map2d = reader.readMap2d()
        
        solver = GBFS_Solver()
        solution = map2d.solvedBy(solver=solver)
        solution.showToConsole()
        
        visualizer = Visualizer2d(map=map2d, solution=solution, speed=100)
        visualizer.visualize2d()
    except Exception as ex:
        print("Error: ", ex)