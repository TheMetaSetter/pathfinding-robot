from map_and_obstacles import Map2d
from map_file_reader import MapFileReader
from solver import DijkstraSolver
from solution import Solution2d
from visualizer import Visualizer2d

map_file_reader = MapFileReader("input/input.txt")
map = map_file_reader.readMap2d()

solver = DijkstraSolver()
solution = map.solvedBy(solver)
solution.showToConsole()

visualizer = Visualizer2d(solution, map)
visualizer.visualize2d()