from map_and_obstacles import Map2d
from shapely.geometry import Polygon

class MapFileReader:
    """
    A class to read a map from a file.
    
    Attributes:
    - filename: Name of the file to read the map from.
    
    Methods:
    - readMap2d(): Reads the map from the file and returns a Map2d object.
    
    Example:
    >>> reader = MapFileReader("map.txt")
    >>> map2d = reader.readMap2d()
    """
    
    def __init__(self, filename: str):
        self.__filename = filename
    
    def readMap2d(self) -> Map2d:
        # Open file and read map
        with open(self.__filename, "r") as f:
            # Read map width and height on a line
            line = f.readline()
            width, height = line.split(',')
            width = int(width)
            height = int(height)
            
            # Read start point, end point and pick up points on a line
            line = f.readline()
            list_coordinates = line.split(',')
            # Group list coordinates into tuples of 2
            tuple_coordinates = [(int(list_coordinates[i]), int(list_coordinates[i + 1]))
                                 for i in range(0, len(list_coordinates), 2)] # Step of the for loop is 2
            start = tuple_coordinates[0]
            end = tuple_coordinates[1]
            
            # Check if there is any pick-up points
            pick_up_points = None
            if len(tuple_coordinates) >= 2:
                pick_up_points = tuple_coordinates[2:]
            
            # Read number of obstacles and obstacles speed on a line
            # Read number of obstacles and obstacles speed on a line
            line = f.readline()
            try:
                number_of_obstacles, obstacles_speed = int(line.split(',')[0]), int(line.split(',')[1])
            except IndexError:
                number_of_obstacles = int(line)
                obstacles_speed = 0
            
            # Read obstacles line by line
            obstacles = []
            for i in range(number_of_obstacles):
                line = f.readline()
                list_coordinates = line.split(',')
                # Group list coordinates into tuples of 2
                tuple_coordinates = [(int(list_coordinates[i]), int(list_coordinates[i + 1]))
                                     for i in range(0, len(list_coordinates), 2)]
                obstacles.append(Polygon(tuple_coordinates))
            
            return Map2d(start, end, obstacles, obstacles_speed, width, height, pick_up_points)