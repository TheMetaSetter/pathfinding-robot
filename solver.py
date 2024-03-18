from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict
from math import sqrt
import time
import random
import numpy as np
import threading

from map_and_obstacles import Map2d, Node2d
from solution import Solution2d
from shapely import Polygon

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
        
    def _constructPath(self, node: Node2d) -> list[Node2d]:
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
    
    def _distance(self, pointA: tuple[int, int], pointB: tuple[int, int]) -> float:
        x_A, y_A = pointA
        x_B, y_B = pointB
        return sqrt((x_A - x_B) ** 2 + (y_A - y_B) ** 2)
class DijkstraSolver(Solver):
    """
    A class to solve a 2D map problem using Dijkstra's algorithm.
    
    Methods:
    - __init__(): Initializes the DijkstraSolver object.
    - solve(map2d: Map2d): Solves the 2D map problem and returns a Solution2d object.
    - _constructPath(node: Node2d): Constructs a path from the start node to the end node.
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
        
        if map2d.getPickUpPoints() != []:
            raise ValueError("DijkstraSolver is not designed to solve TSP problem. Please use another solver, such as GASolver.")
        
        # Start measuring runtime
        start = time.perf_counter()
        
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
                path = self._constructPath(node)
                
                # Measure runtime
                end = time.perf_counter()
                runtime_milisec = (end - start) * 10**3
                
                return Solution2d(path, cost_start_to_node, runtime_milisec)
            
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
    
    
class A_asteriskSolver(Solver):
    """
    A class to solve a 2D map problem using A* algorithm.
    
    Methods:
    - __init__(): Initializes the A_asterickSolver object.
    - solve(map2d: Map2d): Solves the 2D map problem and returns a Solution2d object.
    - _constructPath(node: Node2d): Constructs a path from the start node to the end node.
    """
    
    def __init__(self):
        """
        Initializes the A_asterickSolver object.
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
        
        if map2d.getPickUpPoints() != []:
            raise ValueError("A_asteriskSolver is not designed to solve TSP problem. Please use another solver, such as GASolver.")
        
        # Start measuring runtime in second. Time: t = t0
        start = time.perf_counter()
        
        # Dictionary of $node: distance from start$ pair
        true_cost: Dict[Node2d, int] = {}
        
        # Initialize distance dictionary with start
        true_cost[Node2d(map2d.getStart(), None, None)] = 0
        
        # Define new distance dictionary
        g: Dict[Node2d, int] = {}
        
        # Initialize g
        g[Node2d(map2d.getStart(), None, None)] = self._distance(map2d.getStart(), map2d.getEnd())
        
        # Closed nodes
        closed: list[Node2d] = []
        
        while len(true_cost) > 0:
            # Get the node with the smallest cost from start
            node, cost_start_to_node = min(g.items(), key=lambda x: x[1])
            
            closed.append(node)
            firstIteration = True
            cost = 0
            
            # If the node is the end node, return the path
            if node.getState() == map2d.getEnd():
                path = self._constructPath(node)
                
                for node in path:
                    this_x_coordinates, this_y_coordinates = node.getState()
                    if (firstIteration):
                        firstIteration = False
                        that_x_coordinates, that_y_coordinates = node.getState()
                        continue
                    cost += sqrt((this_x_coordinates - that_x_coordinates)**2 + (this_y_coordinates - that_y_coordinates)**2)
                    that_x_coordinates, that_y_coordinates = node.getState()
                    
                # Measure runtime
                end = time.perf_counter()
                runtime_milisec = (end - start) * 10**3
                    
                return Solution2d(path, cost, runtime_milisec)
            
            # Get the neighbors of the node that are appropriate for the obstacles configuration at this time
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
                cost_neighbor_to_end = sqrt((end_x_coordinates - neighbor_x_coordinates)**2 
                                            + (end_y_coordinates - neighbor_y_coordinates)**2)
                cost_start_to_neighbor = cost_start_to_node \
                                        + cost_node_to_neighbor 
                
                if neighbor not in true_cost or true_cost[neighbor] > cost_start_to_neighbor:
                    # If the neighbor is already in distance, delete it because its parent will be changed.
                    if neighbor in true_cost:
                        del true_cost[neighbor]
                        
                    # Update the cost from start of the neighbor
                    true_cost[neighbor] = cost_start_to_neighbor
                    
                    # Update g dictionary
                    g[neighbor] = cost_start_to_neighbor + cost_neighbor_to_end
                
            # Delete this node from dictionary because it was in closed set.
            del true_cost[node]
            del g[node]

        return None

class GBFS_Solver(Solver):
    """
    A class to solve a 2D map problem using GBFS's algorithm.
    
    Methods:
    - __init__(): Initializes the GBFS Solver object.
    - solve(map2d: Map2d): Solves the 2D map problem and returns a Solution2d object.
    - _constructPath(node: Node2d): Constructs a path from the start node to the end node.
    """
    
    def __init__(self):
        """
        Initializes the GBFS Solver object.
        """
        
        super().__init__()
        
    def solve(self, map2d: Map2d) -> Solution2d:
        """
        Solves the 2D map problem using GBFS's algorithm.
        
        Parameters:
        - map2d (Map2d): The 2D map to be solved.
        
        Returns:
        - Solution2d: The solution to the 2D map problem.
        """
        
        if map2d.getPickUpPoints() != []:
            raise ValueError("GBFS_Solver is not designed to solve TSP problem. Please use another solver, such as GASolver.")
        
        # Start measuring runtime
        start = time.perf_counter()
        
        # Dictionary of $node: distance from start$ pair
        distance: Dict[Node2d, int] = {}
        
        # Initialize distance dictionary with start
        start_node = map2d.getStart()
        end_node = map2d.getEnd()
        start_x, start_y = start_node
        end_x, end_y = end_node
        
        start_node = Node2d((start_x, start_y), None , None)
        end_node = Node2d((end_x, end_y), None , None)

        distance[start_node] = 0

        # Closed nodes
        closed: list[Node2d] = []
                

        while len(distance) > 0:
            # Get the node with the smallest cost from start
            node, cost_start_to_node = min(distance.items(), key=lambda x: x[1])
            
            # Add this node to shortest path tree
            closed.append(node)
            
            # If the node is the end node, return the path
            if node.getState() == map2d.getEnd():
                path = self._constructPath(node)
                
                # Measure runtime
                end = time.perf_counter()
                runtime_milisec = (end - start) * 10**3
                
                return Solution2d(path, cost_start_to_node, runtime_milisec)
            
            # Get the neighbors of the node
            neighbors = map2d.getNeighbors(node)
            
           # For each neighbor in neighbors list, update their distance
            for neighbor in neighbors:
                if neighbor is None or neighbor in closed:
                    continue
                if neighbor not in distance:
                    cost_to_neighbor = neighbor.getAction().cost()
                    
                    neighbor_x, neighbor_y = neighbor.getState()
                    distance[neighbor] = abs(neighbor_x - end_x) + abs(neighbor_y - end_y)
                    
                    distance[neighbor] = cost_start_to_node + cost_to_neighbor  # Accumulating cost
            del distance[node]

        return None
    
class GASolver(Solver):
    def __init__(self, num_generations: int = 75, num_of_parents: int = 20, sol_per_pop: int = 200, mutation_probability: tuple[float, float] = (0.8, 0.2)):
        self.__num_generations: int = num_generations
        self.__num_of_parents: int = num_of_parents
        self.__sol_per_pop: int = sol_per_pop
        self.__mutation_probability: tuple[float, float] = mutation_probability
        self.map: Map2d = None
        self.__tournament_size: int = int(self.__num_of_parents * 0.6)
    
    def __fitness_func(self, solution: list[tuple[int, int]]) -> float:
        # # If there is a line connecting any two consecutive points in the solution crosses over any obstacles, this solution will have negative fitness.
        # if not self.map.validatePickupSequence(solution):
        #     return -1
        
        # If the solution is valid, calculate the cost of the solution.
        cost = 0
        
        first_segment_cost = sqrt((solution[0][0] - self.map.getStart()[0])**2 + (solution[0][1] - self.map.getStart()[1])**2)
        cost += first_segment_cost
        for i in range(1, len(solution)):
            cost += sqrt((solution[i][0] - solution[i - 1][0])**2 + (solution[i][1] - solution[i - 1][1])**2)
        last_segment_cost = sqrt((solution[-1][0] - self.map.getEnd()[0])**2 + (solution[-1][1] - self.map.getEnd()[1])**2)
        cost += last_segment_cost
        
        # Smaller the cost, better the fitness
        return 1 / (cost + 0.0000001) # Add a small number to avoid division by zero
        
    def __init_population(self) -> list[list[tuple[int, int]]]:
        initial_population = []
        for _ in range(self.__sol_per_pop):
            initial_population.append(self.map.getRandomPickUpSequence())
        return initial_population
    
    def __tournament(self, competitors: list[list[tuple[int, int]]]) -> tuple[list[tuple[int, int]], float]:
        # Evaluate each competitor's fitness and store them in a list of tuples
        competitors_fitness = [(competitor, self.__fitness_func(competitor)) for competitor in competitors]
            
        # Sort the competitors by their fitness from high to low
        competitors_fitness.sort(key=lambda x: x[1], reverse=True)
        
        # Return the best competitor and their fitness score as a tuple
        return competitors_fitness[0]

    
    def __tournament_selection(self, population: list[list[tuple[int, int]]], 
                               num_of_parents: int, tournament_size: int) -> list[tuple[list[tuple[int, int]], float]]:
        winners = []
        for _ in range(num_of_parents):
            # Select random competitors from the population
            competitors = random.sample(population, tournament_size)
            winner_tuple = self.__tournament(competitors)
            winners.append(winner_tuple)
         
        return winners
    
    def __order1_crossover(self, parent1: list[tuple[int, int]], 
                              parent2: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
        l = None # length of parents
        if len(parent1) != len(parent2):
            raise ValueError("The size of the parent chromosomes are different")
        else:
            l = len(parent1)
        
        start = 0
        end = 0
        child1 = [None] * l
        child2 = [None] * l
        while start >= end:
            start = random.randint(0, l - 1)
            end = random.randint(start, l - 1)
        
        # Copy part of the parent to the children
        child1[start:end+1] = parent1[start:end+1]
        child2[start:end+1] = parent2[start:end+1]
        
        # Fill the remaining slots in the two child
        child1_idx = (end + 1) % l
        child2_idx = (end + 1) % l
        for i in range(end + 1, l):
            if parent2[i] not in child1 and child1[child1_idx] is None:
                child1[child1_idx] = parent2[i]
                child1_idx = (child1_idx + 1) % l
            if parent1[i] not in child2 and child2[child2_idx] is None:
                child2[child2_idx] = parent1[i]
                child2_idx = (child2_idx + 1) % l
            
        for i in range(0, end + 1):
            if parent2[i] not in child1 and child1[child1_idx] is None:
                child1[child1_idx] = parent2[i]
                child1_idx = (child1_idx + 1) % l
            if parent1[i] not in child2 and child2[child2_idx] is None:
                child2[child2_idx] = parent1[i]
                child2_idx = (child2_idx + 1) % l
                
        return [child1, child2]
    
    def __generate_new_population(self, parents_list_of_tuple: 
        list[tuple[list[tuple[int, int]], float]]) -> list[list[tuple[int, int]]]:
        
        count_children = 0
        new_population: list[list[tuple[int, int]]] = []
        while count_children < self.__sol_per_pop:
            # Select randomly parents
            parent1_idx: int = 0
            parent2_idx: int = 0
            while parent1_idx == parent2_idx:
                parent1_idx = random.randint(0, len(parents_list_of_tuple) - 1)
                parent2_idx = random.randint(0, len(parents_list_of_tuple) - 1)
                
            # Take those randomly chosen parents out of the list of tuple and assign into different variables
            parent1: list[tuple[int, int]] = parents_list_of_tuple[parent1_idx][0]
            parent2: list[tuple[int, int]] = parents_list_of_tuple[parent2_idx][0]
            
            # Perform OX_1 crossover
            children: list[list[tuple[int, int]]] = self.__order1_crossover(parent1, parent2)
            
            # Add the recently born children to the new population
            new_population += children
            
            # Increment the number of born children
            count_children += 2
        
        # If the number of born children exceeded the maximum number of children per generation, kill some of them =))
        if count_children > self.__sol_per_pop:
            new_population = new_population[0:self.__sol_per_pop]
            
        return new_population
    
    def __swap_mutation(self, new_population: list[list[tuple[int, int]]]) -> list[list[tuple[int, int]]]:
        
        # Calculate average fitness of the population
        population_fitness_list: list[float] = [self.__fitness_func(chromosome) for chromosome in new_population]
        average_fitness = np.average(population_fitness_list)
        
        # Iterate through new_population with enum
        for i, chromosome in enumerate(new_population):
            need_to_mutate = False
            if population_fitness_list[i] < average_fitness:
                p = random.randint(0,1) # Probability that this chromosome will be mutated
                if p < self.__mutation_probability[0]:
                    need_to_mutate = True
            else:
                p = random.randint(0,1) # Probability that this chromosome will be mutated
                if p < self.__mutation_probability[1]:
                    need_to_mutate = True
            
            # If the chromosome needs to be mutated, swap two random genes
            if need_to_mutate:
                idx1 = random.randint(0, len(chromosome) - 1)
                while True:
                    idx2 = random.randint(0, len(chromosome) - 1)
                    if idx1 != idx2:
                        break
                chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
                new_population[i] = chromosome
        
        return new_population
    
    def solve(self, map: Map2d):
        # Check if this is the TSP problem
        
        if map.getPickUpPoints() == []:
            raise ValueError("GASolver is designed to solve only TSP problem. Please use another solver.")
        
        self.map = map
        
        try:
            # Lock the obstacles configuration to solve the map at this instant moment
            self.map.obstacles_lock.acquire()
        except AttributeError:
            pass
        
        # Start measuring time
        start = time.perf_counter()
        
        # Population initialization
        initial_population = self.__init_population()
        
        # Select parents
        parents_list_of_tuple = self.__tournament_selection(initial_population, 
                                                            self.__num_of_parents, 
                                                            self.__tournament_size)
        
        # Calculate the average of the 4 most recent set of parents from the 4 most recent generation
        curr_generation = 0
        x = 0
        y = 0
        z = 0
        t = np.average([parents_list_of_tuple[i][1] 
                        for i in range(len(parents_list_of_tuple))]) # Calculate the average fitness of the current parents
        
        # Testing performance of algorithm
        generations_averages = []
        generations_averages.append(t)
        generations_bests = []
        generations_bests.append(max(parents_list_of_tuple, key=lambda x: x[1])[1])
        
        convergence = (t - x < 0.00001) or (curr_generation > self.__num_generations)
        while not convergence:
            new_population: list[list[tuple[int, int]]] = self.__generate_new_population(parents_list_of_tuple)
            new_population = self.__swap_mutation(new_population)
            parents_list_of_tuple = self.__tournament_selection(new_population, 
                                                                self.__num_of_parents, 
                                                                self.__tournament_size)
            x = y
            y = z
            z = t
            t = np.average([parents_list_of_tuple[i][1] 
                            for i in range(len(parents_list_of_tuple))])
            
            # Testing performance of algorithm
            generations_averages.append(t)
            generations_bests.append(max(parents_list_of_tuple, key=lambda x: x[1])[1])
            
            convergence = (t - x < 0.00001) or (curr_generation > self.__num_generations)
            
        # If it is converged, return the best solution
        solution: tuple[list[tuple[int, int]], float] = max(parents_list_of_tuple, key=lambda x: x[1])
        solution = solution[0]
        
        # Use the best solution to construct the path between start and end points.
        # Now we need to find shortest path between start and first pickup point, and between each pair of consecutive pickup points
        # and between last pickup point and end point.
        
        # Construct the shortest path from start to first pickup point using A* algorithm
        # Create the only map to use in below steps
        
        map2d = Map2d(map.getStart(), solution[0], 
                    map.getObstacles(), map.getObstaclesSpeed(), 
                    map.getWidth(), map.getHeight(), [])
        
        # To avoid extending on the end point, add the end point to obstacle list
        map2d.addObstacle(Polygon(map.getEnd()))
        
        start_to_first_pickup = None
        while True:
            start_to_first_pickup = A_asteriskSolver().solve(map2d)
            if start_to_first_pickup is not None:
                break
        
        # Construct the shortest path between each pair of consecutive pickup points using A* algorithm
        pickup_to_pickup = []
        for i in range(len(solution) - 1):
            map2d.setStart(solution[i])
            map2d.setEnd(solution[i + 1])
            
            while True:
                sub_solution = A_asteriskSolver().solve(map2d)
            
                if sub_solution is not None:
                    pickup_to_pickup.append(sub_solution)
                    break
                
        # Debug
        
        # Remove end point out of list of obstacles
        map2d.removeLastObstacle(Polygon(map.getEnd()))
        
        # Construct the shortest path from last pickup point to end using A* algorithm
        map2d.setStart(solution[-1])
        map2d.setEnd(map.getEnd())
        
        while True:
            last_pickup_to_end = A_asteriskSolver().solve(map2d)
            
            if last_pickup_to_end is not None:
                break
        
        # Concatenate the paths to construct the final path
        path = start_to_first_pickup.getPath()
        for p in pickup_to_pickup:
            # Remove the first node of the path as it is the same as the last node of the previous path
            path += p.getPath()[1:]
        path += last_pickup_to_end.getPath()[1:]
        
        cost = start_to_first_pickup.cost + sum([p.cost for p in pickup_to_pickup]) + last_pickup_to_end.cost
        
        end = time.perf_counter()
        
        runtime_milisec = (end - start) * 10**3
        
        # Release the lock
        try:
            self.map.obstacles_lock.release()
        except AttributeError:
            pass
        
        # Debug
        print("Initial obstacles configuration solved.\n")
        
        return Solution2d(path, cost, runtime_milisec)