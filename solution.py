from map_and_obstacles import Node2d

class Solution2d:
    def __init__(self, path: list[Node2d], cost: float):
        """_summary_

        Args:
            path (list[Node2d]): _description_
            cost (int): _description_
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