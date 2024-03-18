import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import to_rgba
from matplotlib.animation import FuncAnimation

from map_and_obstacles import Map2d
from solution import Solution2d

class Visualizer2d:
    def __init__(self, solution: Solution2d, map: Map2d, speed: int = 1000):
        self.__solution = solution
        self.__map = map
        self.__speed = speed # Delay between frames in miliseconds
        
    def update(self, frame):
        self.ax.clear()  # Clear previous frame

        # Reset the plot (similarly to how you initially set it up)
        self.ax.set_xlim(0, self.__map.getWidth())
        self.ax.set_ylim(0, self.__map.getHeight())
        self.ax.set_facecolor(to_rgba('white', alpha=0.5))
        self.ax.grid(True, which='both', color='grey', linewidth=0.5, linestyle='-', alpha=0.3)

        # Redraw obstacles, pickup points, start and end points
        # (similar to how you initially drew them, but inside this function)
        for obstacle in self.__map.getObstacles():
            self.ax.add_patch(patches.Polygon(list(obstacle.exterior.coords), closed=True, color='black'))
        
        # Plot pickup-points
        for pickup in self.__map.getPickUpPoints():
            self.ax.add_patch(patches.Circle((pickup[0], pickup[1]), 0.3, color='green'))
        
        # Plot start and end points
        start = self.__map.getStart()
        end = self.__map.getEnd()
        self.ax.add_patch(patches.Circle((start[0], start[1]), 0.3, color='red'))
        self.ax.add_patch(patches.Circle((end[0], end[1]), 0.3, color='blue'))

        # For an animated path drawing, adjust to draw up to 'frame' index of your path
        path = self.__solution.getTuplePath()
        if frame > 0:
            for i in range(frame):
                if i < len(path) - 1:
                    self.ax.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]], color='blue')

    def visualize2d(self):
        fig, self.ax = plt.subplots(figsize=(8, 8))
        
        # Initial plot setup, if needed
        self.ax.set_xlim(0, self.__map.getWidth())
        self.ax.set_ylim(0, self.__map.getHeight())
        self.ax.set_facecolor(to_rgba('white', alpha=0.5))
        self.ax.grid(True, which='both', color='grey', linewidth=0.5, linestyle='-', alpha=0.3)

        # Create an animation
        anim = FuncAnimation(fig, self.update, frames=len(self.__solution.getTuplePath()), interval=self.__speed, repeat=False)
        
        if self.__map.getObstaclesSpeed() > 0:
            self.__map.restart()
        
        plt.show()