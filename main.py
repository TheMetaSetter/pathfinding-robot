from map_file_reader import MapFileReader
from solver import DijkstraSolver
from solver import A_asteriskSolver
from visualizer import Visualizer2d
from solver import GBFS_Solver

map_file_reader = MapFileReader("input/input.txt")
map = map_file_reader.readMap2d()

solver = GBFS_Solver()
solution = map.solvedBy(solver)
solution.showToConsole()

visualizer = Visualizer2d(solution, map)
visualizer.visualize2d()