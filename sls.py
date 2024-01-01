# import necessary packages
import random
import math
import time

# Function to load the generated cost matrix
def read_cost_matrix(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()[1:]  # Ignore the first line
        cost_matrix = [[float(cost) for cost in line.split()] for line in lines]
    return cost_matrix

# Function to create a random complete path
    # Returns a random permutation of numbers from 1 to the length of the cost matrix
def random_path(cost_matrix):
    return random.sample(range(1, len(cost_matrix) + 1), len(cost_matrix))

# Function to calculate the cost of the generated path including the return path
def calculate_cost(path, cost_matrix):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += cost_matrix[path[i] - 1][path[i + 1] - 1]
    total_cost += cost_matrix[path[-1] - 1][path[0] - 1]
    return total_cost

# Function to generate different path
    # Random Aspect of the algorithm
def generate_neighbor(path):
    # Swap two random cities in the path to generate a neighbor
    new_path = path.copy()
    i, j = random.sample(range(len(path)), 2) # generate 2 random indexes to switch
    new_path[i], new_path[j] = new_path[j], new_path[i] # swap the 2 paths
    return new_path

# Function to calculate the probability of accepting an "undesireable path" as part of SLS Simulated Annealing
def accept_prob(current_cost, new_cost, temp):
    if new_cost < current_cost: # If the cost of the "neighbor" path is lower, always accept
        return 1.0
    return math.exp((current_cost - new_cost) / temp) # Otherwise use P(accept) = exp( delta_E / T)

# Main Simulated Annealing Algorithm
def simulated_annealing(cost_matrix, initial_temp, cooling_rate, min_temp):
    start_time = time.time() #start timer

    # initial_temp, cooling_rate, min_temp are user defined variables and can be adjusted accordingly
    best_path = random_path(cost_matrix) # First generate a random path and store as best path
    current_cost = calculate_cost(best_path, cost_matrix) # Find the cost of the initial path
    temp = initial_temp # Store the initial temp

    while temp > min_temp: # temperature minimum is used as the stopping criteria for this algorithm
                           # When the algorithm reaches a certain temperature, algorithm stops searching
        new_path = generate_neighbor(best_path) # create neighbors to compare
        new_cost = calculate_cost(new_path, cost_matrix) # calculate the cost of the neighbors

        if new_cost <= current_cost:
            best_path = new_path
            current_cost = new_cost
        elif current_cost > new_cost:
            if accept_prob(current_cost, new_cost, temp) > random.uniform(0, 1):
                best_path = new_path
                current_cost = new_cost

        temp *= cooling_rate # temperature is reduced by a defined cooling rate. 
    
    end_time = time.time()
    elapsed_time = round(end_time - start_time,4)
    
    print("TSP Path using simulated annealing:", best_path)
    print("TSP Cost using simulated annealing:", round(current_cost,3))
    print("Time taken:", elapsed_time, "seconds")

    return best_path

#usage
file_name = "10000_54.0_3.8.out"  # Replace with your own file name if needed
initial_temp = 1000
cooling_rate = 0.99
min_temp = 1

result = simulated_annealing(read_cost_matrix(file_name), initial_temp, cooling_rate, min_temp)
