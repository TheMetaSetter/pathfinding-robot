from enum import Enum
from math import sqrt


class Action2d(Enum):
    """
    Enum class for 2D actions

    Attributes:
    - LEFT: Move left
    - RIGHT: Move right
    - UP: Move up
    - DOWN: Move down
    - UP_LEFT: Move up-left
    - UP_RIGHT: Move up-right
    - DOWN_LEFT: Move down-left
    - DOWN_RIGHT: Move down-right

    Methods:
    - cost(): Return cost of the action
    - name(): Return name of the action

    Example:
    >>> action = Action2d.UP
    >>> action.cost()
    1

    >>> action = Action2d.UP
    >>> action.name()
    "UP"
    """

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
        """
        Return cost of the action

        Returns:
        - float: cost of the action

        Example:
        >>> Action2d.UP.cost()
        1
        """
        if self == Action2d.UP or \
                self == Action2d.DOWN or \
                self == Action2d.LEFT or \
                self == Action2d.RIGHT:
            return 1
        else:
            return sqrt(2)

    def name(self):
        """
        Return name of the action

        Returns:
        - str: name of the action

        Example:
        >>> Action2d.UP.name()
        "UP"
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
