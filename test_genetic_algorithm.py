if __name__ == "__main__":
    from map_file_reader import MapFileReader
    from solver import GASolver
    
    # Test performance of GASolver
    import numpy as np

    map_file_reader = MapFileReader("input/input.txt")
    map = map_file_reader.readMap2d()
    
    average_volatilities = [] # Store the average fitness score of each generation in each run
    best_volatilities = [] # Store the best fitness score of each generation in each run
    
    for i in range(500):
        solver = GASolver(num_generations=75, num_of_parents=20, sol_per_pop=200, mutation_probability=(0.8,0.2))
        solution, generations_averages, generations_bests = map.solvedBy(solver)
        
        # Measure the volatility of the generations_average
        average_volatility = np.std(generations_averages)
        
        # Measure the volatility of the generations_best
        best_volatility = np.std(generations_bests)
        
        average_volatilities.append(average_volatility)
        best_volatilities.append(best_volatility)
        
        # solution.showToConsole()
        
    # Plot the average and best volatilities of each run on different plots
    import matplotlib.pyplot as plt
    plt.plot(average_volatilities)
    plt.xlabel("Run")
    plt.ylabel("Average Volatility")
    plt.savefig("average_volatility.png")
    
    plt.clf()
    
    plt.plot(best_volatilities)
    plt.xlabel("Run")
    plt.ylabel("Best Volatility")
    plt.savefig("best_volatility.png")