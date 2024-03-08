from __future__ import annotations
from abc import ABC, abstractmethod
from map_and_obstacles import Map2d, Node2d
from solution import Solution2d
from action import Action2d
from queue import Queue
from typing import Dict

class Solver(ABC):
    """Interface for a solver.
    """
        
    @abstractmethod
    def solve(self, map2d: Map2d):
        pass

class DijkstraSolver(Solver):
    """Concrete implementation of the Solver interface using Dijkstra's algorithm.
    """
    
    def __init__(self):
        super().__init__()
        
    def solve(self, map2d: Map2d) -> Solution2d:
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
        # Construct the path by following the parent pointers
        path = []
        while node:
            path.append(node)
            node = node.getParent()
        path.reverse()
        return path