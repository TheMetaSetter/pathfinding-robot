from map_and_obstacles import Node2d

class Solution2d:
    def __init__(self, path: list[Node2d], cost: float):
        """
        A class to represent a solution to a 2D map problem.
        
        Attributes:
        - path: List of nodes from start to end.
        - cost: Cost of the path.
        
        Methods:
        - __str__(): Returns a string representation of the solution.
        - showToConsole(): Prints the solution to the console.
        
        Example:
        >>> solution = Solution2d([Node2d((0, 0), None, None), Node2d((0, 1), None, None)], 1.0)
        >>> print(solution)
        Solution2d(path=[Node2d((0, 0), None, None), Node2d((0, 1), None, None)], cost=1.0)
        >>> solution.showToConsole()
        (0, 0) TO (0, 1)
        Cost: 1.0
        """
        
        self.path = path
        self.cost = cost
    
    def __str__(self) -> str:
        return f"Solution2d(path={self.path}, cost={self.cost})"
    
    def showToConsole(self):
        # Print path, except the last node
        for node in self.path[:-1]:
            if node.getAction() is not None:
                print(node.getAction().name(), end=" TO ")
            print(node.getState())
        
        # Print cost
        print(f"Cost: {self.cost}")
        
    def getPath(self) -> list[tuple]:
        return [node.getState() for node in self.path]