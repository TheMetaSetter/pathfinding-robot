from map_file_reader import MapFileReader
from solver import DijkstraSolver
from solver import A_asteriskSolver
from visualizer import Visualizer2d

map_file_reader = MapFileReader("input/input.txt")
map = map_file_reader.readMap2d()

solver = A_asteriskSolver()
solution = map.solvedBy(solver)
solution.showToConsole()

visualizer = Visualizer2d(solution, map)
visualizer.visualize2d()