import time
from shapely.affinity import translate
from shapely.geometry import Polygon, Point, LineString
import threading

from action import Action2d
from typing import Optional
# from solver import Solver  # Moved inside the function where it's used to avoid circular import

class Node2d:
    """A class representing a data structure that searching algorithms use to traverse the map and store information about the path.
    
    Attributes:
    - state: A point in the map, which is a tuple of (x, y)
    - parent: Parent state of a node
    - action: Action that led to this node from the parent state
    
    Methods:
    - getState(): Return the state of the node.
    - getParent(): Return the parent state of the node
    - getAction(): Return the action that led to this node from the parent state
    
    Example:
    >>> node = Node2d((0, 0), None, Action2d.UP)
    >>> node.getState()
    (0, 0)
    """
    
    def __init__(self, state: tuple[int, int], parent: tuple[int, int], action: Action2d):
        self.__state = state # A state is simply a point in the map, which is a tuple of (x, y)
        self.__parent = parent # parent state of a node
        self.__action = action # action that led to this node from the parent state
        
    def getState(self) -> tuple[int, int]:
        """
        Return the state of the node.
        
        Returns:
        - tuple[int, int]: state of the node
        
        Example:
        >>> node = Node2d((0, 0), None, Action2d.UP)
        >>> node.getState()
        (0, 0)
        """
        
        return self.__state
    
    def getParent(self) -> tuple[int, int]:
        """
        Return the parent state of the node.
        
        Returns:
        - tuple[int, int]: parent state of the node
        
        Example:
        >>> node = Node2d((0, 0), None, Action2d.UP)
        >>> node.getParent()
        None
        """
        return self.__parent
    
    def getAction(self) -> Action2d:
        """
        Return the action that led to this node from the parent state.
        
        Returns:
        - Action2d: action that led to this node from the parent state
        """
        
        return self.__action
    
    def __str__(self) -> str:
        """
        Return a string representation of the node.
        
        Returns:
        - str: string representation of the node
        """
        
        return f"Node2d(state={self.__state}, parent={self.__parent}, action={self.__action})"
    
    def __repr__(self) -> str:
        """
        Return a string representation of the node
        
        Returns:
        - str: string representation of the node
        """
        
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        """
        Return True if the state of this node is equal to the state of the other node.
        
        Returns:
        - bool: True if the state of this node is equal to the state of the other node
        """
        
        return self.getState() == other.getState()
    
    def __hash__(self) -> int:
        """
        Return the hash of the state of the node.
        
        Returns:
        - int: hash of the state of the node
        """
        
        return hash(self.getState())
    
class Map2d:
    """
    A class representing a 2D map with obstacles.
    
    Attributes:
    - start: Start point of the map
    - end: End point of the map
    - obstacles: List of obstacles in the map
    - width: Width of the map
    - height: Height of the map
    - pickUpPoints: List of pick-up points
    
    Methods:
    - solvedBy(solver: Optional[Solver]) -> Optional[Solution2d]: Solve the map by a solver
    - getStart() -> tuple[int, int]: Return the start point of the map
    - getEnd() -> tuple[int, int]: Return the end point of the map
    - getObstacles() -> list[Polygon]: Return the list of obstacles in the map
    - getWidth() -> int: Return the width of the map
    - getHeight() -> int: Return the height of the map
    - getPickUpPoints() -> list[tuple[int, int]]: Return the list of pick-up points
    - result(node: Node2d, action: Action2d) -> Node2d: Return the new state based on the action
    - getNeighbors(node: Node2d) -> list[Node2d]: Return the neighbors of the node
    """
    
    def __init__(self, start: tuple[int, int], end: tuple[int, int], obstacles: 
                    list[Polygon], obstacles_speed: int, width: int, height: int, pickUpPoints: list[tuple[int, int]]):
        """
        Initialize a 2D map with obstacles.
        
        Args:
        - start (tuple[int, int]): Start point of the map
        - end (tuple[int, int]): End point of the map
        - obstacles (list[Polygon]): List of obstacles in the map
        - obstacles_speed (int): Speed of obstacles
        - width (int): Width of the map
        - height (int): Height of the map
        - pickUpPoints (list[tuple[int, int]]): List of pick-up points
        """
        
        self.__start = start
        self.__end = end
        self.__obstacles = obstacles # Current obstacles (obstacles with current coordinates)
        self.__obstacles_speed = obstacles_speed
        self.__width = width
        self.__height = height
        self.__pickUpPoints = pickUpPoints
        
        if obstacles_speed > 0:
            # Attributes for managing obstacles thread
            self.__stop_event = threading.Event()
            self.obstacles_lock = threading.Lock()
            
            # 
            self.__delay_time = 0.001
            
            # Another thread will handle the movement of the obstacles
            self.__obstacles_thread = threading.Thread(target=self.__perform_obstacles_movement, daemon=True)
            self.__obstacles_thread.start()
            
            # Save the original state of the obstacles in order to restart the map if needed
            self.__original_obstacles = obstacles
        
    def solvedBy(self, solver: 'Optional[Solver]') -> 'Optional[Solution2d]':
        """
        Solve the map by a solver.
        
        Args:
        - solver: Solver to solve the map
        
        Returns:
        - Optional[Solution2d]: Solution of the map
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> solver = DijkstraSolver()
        >>> solution = map2d.solvedBy(solver)
        """
        
        self.__delay_time = 0.001
        from solver import Solver  # Moved here to avoid circular import
        return solver.solve(self) if solver is not None else None
    
    def getStart(self) -> tuple[int, int]:
        """
        Return the start point of the map.
        
        Returns:
        - tuple[int, int]: start point of the map
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> map2d.getStart()
        (0, 0)
        """
        
        return self.__start
    
    def getEnd(self) -> tuple[int, int]:
        """
        Return the end point of the map.
        
        Returns:
        - tuple[int, int]: end point of the map
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> map2d.getEnd()
        (10, 10)
        return self.__end
        """
        
        return self.__end
    
    def getObstacles(self) -> list[Polygon]:
        """
        Return the obstacles of the map.
        
        Returns:
        - list[Polygon]: obstacles of the map
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> map2d.getObstacles()
        [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        """
        
        return self.__obstacles
    
    def getWidth(self) -> int:
        """
        Return the width of the map.
                
        Returns:
        - int: width of the map
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> map2d.getWidth()
        20
        """
        
        return self.__width
    
    def getHeight(self) -> int:
        """
        Return the height of the map.
                
        Returns:
        - int: height of the map
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> map2d.getHeight()
        20
        """
        
        return self.__height
    
    def getPickUpPoints(self) -> list[tuple[int, int]]:
        """
        Return the pick up points on the map.
                
        Returns:
        - list[tuple[int, int]]: pick up points on the map
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> map2d.getPickUpPoints()
        [(5, 5), (7, 7)]
        """
        
        return self.__pickUpPoints
    
    def __str__(self):
        """
        Return a string representation of the map.
                
        Returns:
        - str: string representation of the map
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> print(map2d)
        Map2d(start=(0, 0), end=(10, 10), obstacles=[Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])], \
                    width=20, height=20, pickUpPoints=[(5, 5), (7, 7)])
        """
        
        # Return a dictionary-like string representation of the map
        return f"Map2d(start={self.__start}, end={self.__end}, obstacles={self.__obstacles}, \
                    width={self.__width}, height={self.__height}, pickUpPoints={self.__pickUpPoints})"
    
    def result(self, node: Node2d, action: Action2d) -> Node2d:
        """
        Calculate the new state based on the action.
        
        Args:
        - node: Current node
        - action: Action to be performed
        
        Returns:
        - Node2d: New node after performing the action
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> node = Node2d(start, None, Action2d.UP)
        >>> action = Action2d.UP
        >>> map2d.result(node, action)
        Node2d(state=(0, 1), parent=(0, 0), action=Action2d.UP)
        """
        
        new_state = None
        
        # Calculate the new state based on the action
        if action == Action2d.LEFT:
            new_state = (node.getState()[0] - 1, node.getState()[1])
        elif action == Action2d.RIGHT:
            new_state = (node.getState()[0] + 1, node.getState()[1])
        elif action == Action2d.UP:
            new_state = (node.getState()[0], node.getState()[1] + 1)
        elif action == Action2d.DOWN:
            new_state = (node.getState()[0], node.getState()[1] - 1)
        elif action == Action2d.UP_LEFT:
            new_state = (node.getState()[0] - 1, node.getState()[1] + 1)
        elif action == Action2d.UP_RIGHT:
            new_state = (node.getState()[0] + 1, node.getState()[1] + 1)
        elif action == Action2d.DOWN_LEFT:
            new_state = (node.getState()[0] - 1, node.getState()[1] - 1)
        elif action == Action2d.DOWN_RIGHT:
            new_state = (node.getState()[0] + 1, node.getState()[1] - 1)
        
        # If the new state intersect with any obstacle, then return None
        for obstacle in self.__obstacles:
            if obstacle.contains(Point(new_state)) or obstacle.touches(Point(new_state)):
                return None
            
        # If the new state is out-of-bound, then return None
        if not(0 < new_state[0] < self.__width
               and 0 < new_state[1] < self.__height):
            return None
            
        return Node2d(new_state, node, action)
    
    def getNeighbors(self, node: Node2d) -> list[Node2d]:
        """
        Return the neighbors of the node.
        
        Args:
        - node: Node for which neighbors are to be found
        
        Returns:
        - list[Node2d]: List of neighboring nodes
        
        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> node = Node2d(start, None, Action2d.UP)
        >>> map2d.getNeighbors(node)
        [Node2d(state=(0, 1), parent=(0, 0), action=Action2d.UP), ...]
        """
        
        # List to store the neighbors
        neighbors: list[Node2d] = []
        
        # For each action, calculate the new state and create a new node
        for action in Action2d:
            new_node: Node2d = self.result(node, action)
            if new_node is not None:
                neighbors.append(new_node)
        
    
    
    def validatePickupSequence(self, sequence: list[tuple[int, int]]) -> bool:
        
        first_line = LineString([self.__start, sequence[0]])
        if first_line.intersects(self.__obstacles).any() or first_line.touches(self.__obstacles).any():
            return False
        
        for i in range(len(sequence) - 1):
            curr_line = LineString([sequence[i], sequence[i + 1]])
            for obstacle in self.__obstacles:
                if curr_line.intersects(obstacle) or curr_line.touches(obstacle):
                    return False

        last_line = LineString([sequence[-1], self.__end])
        if last_line.intersects(self.__obstacles).any() or last_line.touches(self.__obstacles).any():
            return False
        
        return True
    
    def __perform_obstacles_movement(self):
        """
        Perform the movement of the obstacles.
        
        This method is called by the __init__ method to start a separate thread for the movement of the obstacles.
        The obstacles are moved every second, alternating between moving to the left and to the right.
        The speed of the obstacles is determined by the __obstacles_speed attribute.
        """
        
        count = 0
        while not self.__stop_event.is_set():
            self.obstacles_lock.acquire()
            new_obstacles = []
            # For each second, move the obstacles
            for obstacle in self.__obstacles:
                if count % 2 != 0:
                    # Move the obstacle to the left
                    obstacle = translate(obstacle, xoff=-self.__obstacles_speed)
                else:
                    # Move the obstacle to the right
                    obstacle = translate(obstacle, xoff=self.__obstacles_speed)
                new_obstacles.append(obstacle)
            self.__obstacles = new_obstacles
            count += 1
            
            self.obstacles_lock.release()
            # Delay for 1 milisecond.
            time.sleep(self.__delay_time) # This is real implementation so movement can be theoritically faster to make computing be efficient.
            # In visualization, the delay between movements will be 1 second.
            
            
            
    def getRandomPickUpSequence(self) -> list[tuple[int, int]]:
        """
        Generate a random sequence of pick-up points.

        Returns:
        - list[tuple[int, int]]: Random sequence of pick-up points

        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7), (3, 3), (8, 8)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> map2d.getRandomPickUpSequence()
        [(3, 3), (8, 8), (7, 7), (5, 5)]
        """
        
        # From the self.__pickUpPoints, generate a radom sequence of pick-up points
        import random
        random_pickup_points = self.__pickUpPoints.copy()
        random.shuffle(random_pickup_points)
        return random_pickup_points
    
    def setStart(self, start: tuple[int, int]):
        """
        Set the start point of the map.

        Args:
        - start: Start point of the map

        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> map2d.setStart((1, 1))
        """
        
        self.__start = start
        
    def setEnd(self, end: tuple[int, int]):
        """
        Set the end point of the map.

        Args:
        - end: End point of the map

        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, width, height, pickUpPoints)
        >>> map2d.setEnd((10, 20))
        """
        
        self.__end = end
        
    def getObstaclesSpeed(self) -> int:
        """
        Get the speed of the obstacles.

        Returns:
        - int: Speed of the obstacles (unit: coordinate/second)

        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> obstacle_speed = 2
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, obstacle_speed, width, height, pickUpPoints)
        >>> map2d.getObstaclesSpeed()
        2
        """
        
        return self.__obstacles_speed
    
    def __stop_moving_obstacles(self):
        """
        Stop the movement of the obstacles.
        
        This method sets the stop event, which is used to stop the obstacles thread.
        """
        
        self.__stop_event.set()
        self.__obstacles_thread.join()
    
    def restart(self):
        """
        Restart the map.

        This method stops the movement of the obstacles, resets the obstacles to their original state,
        and starts the movement of the obstacles again.

        Example:
        >>> start = (0, 0)
        >>> end = (10, 10)
        >>> obstacles = [Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])]
        >>> obstacle_speed = 2
        >>> width = 20
        >>> height = 20
        >>> pickUpPoints = [(5, 5), (7, 7)]
        >>> map2d = Map2d(start, end, obstacles, obstacle_speed, width, height, pickUpPoints)
        >>> map2d.restart()
        """
        
        self.__stop_moving_obstacles()
        self.__obstacles = self.__original_obstacles
        self.__delay_time = 1
        self.__obstacles_thread = threading.Thread(target=self.__perform_obstacles_movement, daemon=True)
        self.__obstacles_thread.start()