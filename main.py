from map_file_reader import MapFileReader
from solver import DijkstraSolver
from solver import A_asterickSolver
from visualizer import Visualizer2d
from time import time

map_file_reader = MapFileReader("input/input.txt")
map = map_file_reader.readMap2d()

start = time()
solver = A_asterickSolver()
solution = map.solvedBy(solver)
solution.showToConsole()
end = time()
print("Runtime =", end - start)

visualizer = Visualizer2d(solution, map)
visualizer.visualize2d()