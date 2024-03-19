import threading
import numpy as np

if __name__ == "__main__":
    from map_file_reader import MapFileReader
    from solver import GASolver
    import numpy as np
    import matplotlib.pyplot as plt
    
    import os
    input_directory = "input_tsp"
    file_names = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
    
    # Delete file .DS_Store
    if ".DS_Store" in file_names:
        file_names.remove(".DS_Store")
    
    generations_bests_of_inputs = []

    for file_name in file_names:
        map_file_reader = MapFileReader(f"input_tsp/{file_name}")
        map = map_file_reader.readMap2d()
        
        solver = GASolver(num_generations=250, num_of_parents=100, sol_per_pop=1500, mutation_probability=(0.8,0.2))
        
        solution, generations_averages, generations_bests = map.solvedBy(solver)
        
        generations_bests_of_inputs.append(generations_bests)
        
    data_1 = np.array(generations_bests_of_inputs[0]).reshape(1, len(generations_bests_of_inputs[0]))
    data_2 = np.array(generations_bests_of_inputs[1]).reshape(1, len(generations_bests_of_inputs[1]))
    
    # Calculate the average of the two data sets
    data_avg = (data_1 + data_2) / 2
    
    # Plot the data sets
    plt.plot(data_1, label="Data Set 1")
    plt.plot(data_2, label="Data Set 2")
    plt.plot(data_avg, label="Average")
    
    # Add a legend
    plt.legend()
    
    # Add a title
    plt.title("Data Sets and Their Average")
    
    # Add X and y Label
    plt.xlabel("X Label")
    plt.ylabel("Y Label")
    
    # Save the plot
    plt.savefig("bests_by_generations.png")
        
    plt.plot(generations_bests_of_inputs)
    plt.xlabel('Generation')
    plt.ylabel('Fitness Value')
    plt.title('Best Fitness Value of Each Generation')
    plt.savefig("bests_by_generations.png")