# NOTICE: Uncomment the last line in the file solver.py before running this code.

import threading
import numpy as np

if __name__ == "__main__":
    from map_file_reader import MapFileReader
    from solver import GASolver
    import numpy as np
    import matplotlib.pyplot as plt
    from typing import List

    import os
    input_directory = "input_tsp"
    file_names = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]

    # Delete file .DS_Store
    if ".DS_Store" in file_names:
        file_names.remove(".DS_Store")

    for file_name in file_names:
        map_file_reader = MapFileReader(f"input_tsp/{file_name}")
        map = map_file_reader.readMap2d()

        # For each test case, we run the genetic algorithm 100 times
        generations_bests: List[List[float]] = [] # This list will hold the best fitness value of each generation for each test case
        generations_averages: List[List[float]] = [] # This list will hold the average fitness value of each generation for each test case

        import threading

        # This function will call 20 times in 20 different threads for this current test case
        def run_genetic_algorithm(file_name, generations_bests, generations_averages):
            for i in range(5):
                ga_solver = GASolver(num_generations=200, num_of_parents=200, sol_per_pop=400)
                
                # Print
                print("Running genetic algorithm for test case", file_name, "for the", i, "time.")
                
                try:
                    best, average = map.solvedBy(ga_solver)
                    generations_bests.append(best)
                    generations_averages.append(average)
                except Exception:
                    pass

        # Create a list to hold the threads
        threads = []

        # Create a lock to prevent race conditions when appending to the lists
        lock = threading.Lock()

        # Run the function in 20 threads
        for i in range(20):
            t = threading.Thread(target=run_genetic_algorithm, args=(file_name, generations_bests, generations_averages))
            threads.append(t)
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

        # Make sure the length of all lists inside generations_bests are the same
        max_length = max([len(x) for x in generations_bests])
        
        # If an element list has its length less than max_length, we append 0 to it until it reaches max_length
        for i in range(len(generations_bests)):
            while len(generations_bests[i]) < max_length:
                generations_bests[i].append(0)
                generations_averages[i].append(0)

        # Convert the lists to numpy arrays
        generations_bests = np.array(generations_bests)
        generations_averages = np.array(generations_averages)

        print(generations_bests.shape)
        print(generations_averages.shape)