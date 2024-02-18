###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Angel Cruz
# Collaborators: none
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    dict ={}
    inFile = open(filename, 'r')
    for line in inFile:
        currentline = line.strip().split(",")
        dict[currentline[0]] = currentline[1]
            
    return dict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cowsCopy = dict(sorted(cows.items(), key=lambda x:x[1], reverse=True))
    trips = []
    
    while len(cowsCopy) > 0:
        subTrip = []
        cowsAvail = {}
        totalWeight = 0.0
        for k,v in cowsCopy.items():
            if (totalWeight + float(v)) <= limit:
                subTrip.append(k)
                totalWeight += float(v)
            else:
                cowsAvail[k] = v
        
        trips.append(subTrip)
        cowsCopy = cowsAvail.copy()
        
    return trips

            

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    def is_weight_limit_compliant(partition):
        '''
        Checks whether the partiiton respects teh weight limitation of the spaceship
        
        Parameters:
        partition - A list of lists, with each inner list containing the names of cows
        transported on a particular trip and the overall list containing all the
        trips
        '''
        for l in partition:
            totalWeight = 0.0
            for i in l:
                if totalWeight + float(cows[i]) <= limit:
                    totalWeight += float(cows[i])
                else:
                    return False
        return True
    
    
    bestTrip = []
    minTrips = len(cows)
    for partition in get_partitions(cows.keys()):
        if is_weight_limit_compliant(partition) and len(partition) < minTrips:
            bestTrip = partition[:]
            minTrips = len(partition)
            
    return bestTrip
                    
                
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    
    start = time.time()
    trips = greedy_cow_transport(cowDic)
    end = time.time()
    print('Result using Greedy algorithm. Number of trips = ', len(trips),'. Runtime = ', end - start)
    print(trips)
    print('\n')
    
    start = time.time()
    trips = brute_force_cow_transport(cowDic)
    end = time.time()
    print('Result using Brute Force algorithm. Number of trips = ', len(trips), '. Runtime = ', end - start)
    print(trips)
    


if __name__ == '__main__':
    cowDic = load_cows("ps1_cow_data.txt")
    print('Dictionary of cows to be transported')
    print(cowDic, end ="\n\n")
    
    compare_cow_transport_algorithms()
    