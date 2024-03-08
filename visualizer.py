from map_and_obstacles import Map2d
from solution import Solution2d

class Visualizer:
    def __init__(self, solution: Solution2d, map: Map2d):
        self.solution = solution
        self.map = map
    
    def visualize(self):
        print("Visualizing solution")
        print("Path: ", self.solution.path)
        print("Cost: ", self.solution.cost)