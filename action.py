from enum import Enum
from math import sqrt

# Enum class for actions
class Action2d(Enum):
    # Name for each action
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    UP_LEFT = 4
    UP_RIGHT = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7
    
    def cost(self) -> float:
        """Return cost of the action

        Returns:
            float: cost of the action
        """
        if self == Action2d.UP or self == Action2d.DOWN or self == Action2d.LEFT or self == Action2d.RIGHT:
            return 1
        else:
            return sqrt(2)
        
    def name(self):
        """Return name of the action

        Returns:
            str: name of the action
        """
        if self == Action2d.LEFT:
            return "LEFT"
        elif self == Action2d.RIGHT:
            return "RIGHT"
        elif self == Action2d.UP:
            return "UP"
        elif self == Action2d.DOWN:
            return "DOWN"
        elif self == Action2d.UP_LEFT:
            return "UP_LEFT"
        elif self == Action2d.UP_RIGHT:
            return "UP_RIGHT"
        elif self == Action2d.DOWN_LEFT:
            return "DOWN_LEFT"
        elif self == Action2d.DOWN_RIGHT:
            return "DOWN_RIGHT"
        else:
            return "UNKNOWN"