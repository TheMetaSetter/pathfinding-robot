import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import to_rgba

from matplotlib.patches import Polygon as MplPolygon
from map_and_obstacles import Map2d
from solution import Solution2d

class Visualizer2d:
    def __init__(self, solution: Solution2d, map: Map2d):
        
        
        self.__solution = solution
        self.__map = map

    # Visualize2d method
    def visualize2d(self):
        """
        Visualizes the 2D map and the solution path.
        
        This method creates a figure and axis, sets the axis limits based on the map size, 
        plots the obstacles, pickup points, start and end points, and the solution path.
        It also adds artistic touches with a blur effect on the grid.
        """
        
        fig, ax = plt.subplots(figsize=(8, 8))  # Create figure and axis
        
        # Set axis limits based on map size
        ax.set_xlim(0, self.__map.getWidth())
        ax.set_ylim(0, self.__map.getHeight())
        
        # Plot the obstacles as black polygons
        for obstacle in self.__map.getObstacles():
            polygon = patches.Polygon(list(obstacle.exterior.coords), closed=True, fill=True, color='black')
            ax.add_patch(polygon)
        
        # Plot the pickup points as blue circles
        pickup_points = self.__map.getPickUpPoints()
        for point in pickup_points:
            ax.scatter(*point, color='blue', zorder=5)
        
        # Plot the start and end points
        ax.scatter(*self.__map.getStart(), color='green', zorder=5)
        ax.scatter(*self.__map.getEnd(), color='red', zorder=5)
        
        # Add artistic touches with a blur effect on the grid
        ax.set_facecolor(to_rgba('white', alpha=0.5))  # Set a white background with transparency
        ax.grid(True, which='both', color='grey', linewidth=0.5, linestyle='-', alpha=0.3)  # Soft grid lines with transparency
        
        # Plot the solution path
        path = self.__solution.getPath()
        for i in range(len(path) - 1):
            start_node = path[i]
            end_node = path[i + 1]
            ax.plot([start_node[0], end_node[0]], 
                    [start_node[1], end_node[1]], 
                    color='blue', zorder=3)
            plt.pause(1)  # Pause to create gradual appearance of the path
        
        plt.show()  # Display the plot