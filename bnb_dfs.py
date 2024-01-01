# import necessary packages
import heapq
import random
import time

# function to read the cost matrix from a file
def read_cost_matrix(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()[1:]  #ignore the first line
        cost_matrix = [[float(cost) for cost in line.split()] for line in lines]
    return cost_matrix

# function to return a random city index within the range of the cost matrix
def random_city(cost_matrix):
    return random.randint(0, len(cost_matrix) - 1)

# function to return the length of a given path
def count(path):
    return len(path)

# function to calculate the total cost of a given path in the TSP
def cost(path, cost_matrix):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += cost_matrix[path[i]][path[i+1]]
    return total_cost

# function to return the last city in a given path
def last_city(path):
    return path[-1]

# function to check if a path exists (not None)
def exists(path):
    return path is not None

# function to check if a path visits all cities in the cost matrix
def is_complete_path(path, cost_matrix):
     return len(set(path)) == len(cost_matrix)

# function to get unvisited neighbors of the last city in the given path
def unvisited_neighbors(path, cost_matrix):
    return [neighbor for neighbor in range(len(cost_matrix)) if neighbor != last_city and neighbor not in path]

# function to solve the TSP using Branch and Bound with Depth-First Search
def BnB_DFS_TSP(file_name):
    cost_matrix = read_cost_matrix(file_name) # read cost matrix from the file

    # initialize priority queue
    pq = []

    # initialize best_cost to infinity
    best_cost = float('inf')

    # initialize best_path to empty
    best_path = []

    # initialize starting variables
    start_city = random_city(cost_matrix)
    initial_path = [start_city]
    path_length = count(initial_path)
    heapq.heappush(pq, (path_length, cost(initial_path, cost_matrix), initial_path)) #push initial path into the priority queue with its length, cost, and the path itself

    start_time = time.time() #start timer

    while pq:

        current_path_length, current_cost, current_path = heapq.heappop(pq)

        # pruning: if a better solution already exists, skip the current path
        if exists(best_path):
            if current_cost > best_cost: #pruning
                continue  

        # check if the current path is a complete path visiting all cities
        if is_complete_path(current_path, cost_matrix):
            current_cost = cost(current_path, cost_matrix)
            # update the best solution if the current path has a lower cost
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = current_path
        else:
            # explore unvisited neighbors of the last city in the current path
            for next_city in unvisited_neighbors(current_path, cost_matrix):
                new_path = current_path + [next_city]
                new_path_length = count(new_path)
                new_path_cost = cost(new_path, cost_matrix)
                heapq.heappush(pq, (new_path_length, new_path_cost, new_path)) # push the new path into the priority queue with its length, cost, and the path itself
                if new_path_cost < best_cost: #If the new path has a lower cost, push it again with its count as the priority
                    heapq.heappush(pq, (count(new_path), new_path_cost, new_path))
    
    end_time = time.time() #end timer
    elapsed_time = end_time - start_time
    print("Time taken to find the path:", round(elapsed_time, 4), "seconds")
    print("Best TSP Cost using Bnb DFS:",round(best_cost, 2))
    best_path = [x+1 for x in best_path] # returns the cities from 1 instead of 0

    return best_path

#usage
file_name = "5_10.0_2.0.out"       # Replace with your own file name if needed
result = BnB_DFS_TSP(file_name)
print("Best TSP Path using Bnb DFS:", result)
