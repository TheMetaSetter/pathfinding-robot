from shapely.geometry import Polygon, Point
from action import Action2d
from typing import Optional
# from solver import Solver  # Moved inside the function where it's used to avoid circular import

class Node2d:
    """Data structure that searching algorithms use to traverse the map and store information about the path.
    """
    
    def __init__(self, state: tuple[int, int], parent: tuple[int, int], action: Action2d):
        self.__state = state # A state is simply a point in the map, which is a tuple of (x, y)
        self.__parent = parent # parent state of a node
        self.__action = action # action that led to this node from the parent state
        
    def getState(self) -> tuple[int, int]:
        return self.__state
    
    def getParent(self) -> tuple[int, int]:
        return self.__parent
    
    def getAction(self) -> Action2d:
        return self.__action
    
    def __str__(self) -> str:
        return f"Node2d(state={self.__state}, parent={self.__parent}, action={self.__action})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        return self.getState() == other.getState()
    
    def __hash__(self) -> int:
        return hash(self.getState())
    
class Map2d:
    """_summary_
    """
    
    def __init__(self, start: tuple[int, int], end: tuple[int, int], obstacles: 
                    list[Polygon], width: int, height: int, pickUpPoints: list[tuple[int, int]]):
        self.__start = start
        self.__end = end
        self.__obstacles = obstacles
        self.__width = width
        self.__height = height
        self.__pickUpPoints = pickUpPoints
        
    def solvedBy(self, solver: 'Optional[Solver]') -> 'Optional[Solution2d]':
        from solver import Solver  # Moved here to avoid circular import
        return solver.solve(self) if solver is not None else None
    
    def getStart(self) -> tuple[int, int]:
        return self.__start
    
    def getEnd(self) -> tuple[int, int]:
        return self.__end
    
    def getObstacles(self) -> list[Polygon]:
        return self.__obstacles
    
    def getWidth(self) -> int:
        return self.__width
    
    def getHeight(self) -> int:
        return self.__height
    
    def getPickUpPoints(self) -> list[tuple[int, int]]:
        return self.__pickUpPoints
    
    def __str__(self):
        # Return a dictionary-like string representation of the map
        return f"Map2d(start={self.__start}, end={self.__end}, obstacles={self.__obstacles}, \
                    width={self.__width}, height={self.__height}, pickUpPoints={self.__pickUpPoints})"
    
    def result(self, node: Node2d, action: Action2d) -> Node2d:
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
            if obstacle.contains(Point(new_state)):
                return None
            
        # If the new state is out-of-bound, then return None
        if not(0 < new_state[0] < self.__width
               and 0 < new_state[1] < self.__height):
            return None
            
        return Node2d(new_state, node, action)
    
    def getNeighbors(self, node: Node2d) -> list[Node2d]:
        # List to store the neighbors
        neighbors: list[Node2d] = []
        
        # For each action, calculate the new state and create a new node
        for action in Action2d:
            new_node: Node2d = self.result(node, action)
            if new_node is not None:
                neighbors.append(new_node)
        
        return neighbors
        