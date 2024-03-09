from __future__ import annotations
from abc import ABC, abstractmethod
from map_and_obstacles import Map2d, Node2d
from solution import Solution2d
from action import Action2d
from queue import Queue
from typing import Dict
from math import sqrt

class Solver(ABC):
    """
    An interface for a solver to solve a 2D map problem.
    
    Methods:
    - solve(map2d: Map2d): Solves the 2D map problem and returns a Solution2d object.
    - __str__(): Returns a string representation of the solver.
    """
        
    @abstractmethod
    def solve(self, map2d: Map2d):
        """
        Solves the 2D map problem and returns a Solution2d object.
        
        Parameters:
        - map2d (Map2d): The 2D map to be solved.
        
        Returns:
        - Solution2d: The solution to the 2D map problem.
        """
        
        pass

class DijkstraSolver(Solver):
    """
    A class to solve a 2D map problem using Dijkstra's algorithm.
    
    Methods:
    - __init__(): Initializes the DijkstraSolver object.
    - solve(map2d: Map2d): Solves the 2D map problem and returns a Solution2d object.
    - __constructPath(node: Node2d): Constructs a path from the start node to the end node.
    """
    
    def __init__(self):
        """
        Initializes the DijkstraSolver object.
        """
        
        super().__init__()
        
    def solve(self, map2d: Map2d) -> Solution2d:
        """
        Solves the 2D map problem using Dijkstra's algorithm.
        
        Parameters:
        - map2d (Map2d): The 2D map to be solved.
        
        Returns:
        - Solution2d: The solution to the 2D map problem.
        """
        
        # Dictionary of $node: distance from start$ pair
        distance: Dict[Node2d, int] = {}
        
        # Initialize distance dictionary with start
        distance[Node2d(map2d.getStart(), None, None)] = 0
        
        # Closed nodes
        closed: list[Node2d] = []
        
        while len(distance) > 0:
            # Get the node with the smallest cost from start
            node, cost_start_to_node = min(distance.items(), key=lambda x: x[1])
            
            # Add this node to shortest path tree
            closed.append(node)
            
            # If the node is the end node, return the path
            if node.getState() == map2d.getEnd():
                path = self.__constructPath(node)
                return Solution2d(path, cost_start_to_node)
            
            # Get the neighbors of the node
            neighbors = map2d.getNeighbors(node)
            
            # For each neighbor in neighbors list, update their cost from start (if needed)
            for neighbor in neighbors:
                if neighbor is None:
                    continue
                if neighbor in closed:
                    continue
                cost_node_to_neighbor = neighbor.getAction().cost()
                cost_start_to_neighbor = cost_start_to_node + cost_node_to_neighbor
                if neighbor not in distance or distance[neighbor] > cost_start_to_neighbor:
                    # If the neighbor is already in distance, delete it because its parent will be changed.
                    if neighbor in distance:
                        del distance[neighbor]
                    # Update the cost from start of the neighbor
                    distance[neighbor] = cost_start_to_neighbor
                
            # Delete this node from dictionary because it was in closed set.
            del distance[node]

        return None
    
    def __constructPath(self, node: Node2d) -> list[Node2d]:
        """
        This method constructs the path by following the parent pointers.
        It takes a node as input and returns a list of nodes.
        """
        
        # Construct the path by following the parent pointers
        path = []
        while node:
            path.append(node)
            node = node.getParent()
        path.reverse()
        return path
    
    
class A_asterickSolver(Solver):
    """
    A class to solve a 2D map problem using A* algorithm.
    
    Methods:
    - __init__(): Initializes the A* object.
    - solve(map2d: Map2d): Solves the 2D map problem and returns a Solution2d object.
    - __constructPath(node: Node2d): Constructs a path from the start node to the end node.
    """
    
    def __init__(self):
        """
        Initializes the A* object.
        """
        
        super().__init__()
        
    def solve(self, map2d: Map2d) -> Solution2d:
        """
        Solves the 2D map problem using A* algorithm.
        
        Parameters:
        - map2d (Map2d): The 2D map to be solved.
        
        Returns:
        - Solution2d: The solution to the 2D map problem.
        """
        
        # Dictionary of $node: distance from start$ pair
        distance: Dict[Node2d, int] = {}
        
        # Initialize distance dictionary with start
        distance[Node2d(map2d.getStart(), None, None)] = 0
        
        # Closed nodes
        closed: list[Node2d] = []
        node_x_coordinates, node_y_coordinates = 0, 0
        end_x_coordinates, end_y_coordinates = 0, 0
        
        while len(distance) > 0:
            # Get the node with the smallest cost from start
            node, cost_start_to_node = min(distance.items(), key=lambda x: x[1])
            
            # Add this node to shortest path tree
            closed.append(node)
            cost = 0
            
            # If the node is the end node, return the path
            if node.getState() == map2d.getEnd():
                path = self.__constructPath(node)
                for node in path:
                    this_x_coordinates, this_y_coordinates = node.getState()
                    if (node.getParent == None):
                        continue
                    that_x_coordinates, that_y_coordinates = node.getParent()
                    cost = sqrt((that_x_coordinates - this_x_coordinates)**2 + (that_y_coordinates - this_y_coordinates)**2)
                return Solution2d(path, cost)
            
            # Get the neighbors of the node
            neighbors = map2d.getNeighbors(node)
            
            # For each neighbor in neighbors list, update their cost from start (if needed)
            for neighbor in neighbors:
                if neighbor is None:
                    continue
                if neighbor in closed:
                    continue
                cost_node_to_neighbor = neighbor.getAction().cost()
                end_x_coordinates, end_y_coordinates = map2d.getEnd()
                neighbor_x_coordinates, neighbor_y_coordinates = neighbor.getState()
                node_x_coordinates, node_y_coordinates = node.getState()
                cost_neighbor_to_end = sqrt((end_x_coordinates - neighbor_x_coordinates)**2 + (end_y_coordinates - neighbor_y_coordinates)**2)
                cost_start_to_neighbor = cost_start_to_node + cost_node_to_neighbor + cost_neighbor_to_end
                
                if neighbor not in distance or distance[neighbor] > cost_start_to_neighbor:
                    # If the neighbor is already in distance, delete it because its parent will be changed.
                    if neighbor in distance:
                        del distance[neighbor]
                    # Update the cost from start of the neighbor
                    distance[neighbor] = cost_start_to_neighbor
                
            # Delete this node from dictionary because it was in closed set.
            del distance[node]

        return None
    
    def __constructPath(self, node: Node2d) -> list[Node2d]:
        """
        This method constructs the path by following the parent pointers.
        It takes a node as input and returns a list of nodes.
        """
        
        # Construct the path by following the parent pointers
        path = []
        while node:
            path.append(node)
            node = node.getParent()
        path.reverse()
        return path