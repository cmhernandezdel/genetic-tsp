from random import randint
from random import random
import constants

"""
Genetic algorithm to solve the Travelling Salesman Problem.

Each individual is a list containing the position of the city visited in that order,
i.e., if the cities are: A, B, C, D, E, F
each individual will be something like:
2, 1, 3, 1, 0
where, taking into account the cities from B to F only (since A is always the first one),
and assuming that if we choose a city that is out of bounds, we take the last,
this would mean that the order is:
A (implicit), D, C, F, E, B, A (implicit, since we have to return to the first city).

Fitness is the total distance traveled, and we want to minimize it.

Mutation is simple: with a certain probability, replace a random gene with a random number.

Cross is a simple, one-point cross in half, generating two individuals.

Selection is done using tourneys.

"""


def read_distances_table(distances_file):
  """ Read distances from a matrix file.

  Keyword arguments:
  distances_file -- the file where the matrix is stored

  Return value:
  distances_table -- a dictionary with the distances between each city
  """

  with open(distances_file, 'r') as distances_matrix:
    # Get the names of the cities
    cities = distances_matrix.readline().rstrip().split(' ')[2:]

    # Get the distances between the cities and store them in a data structure
    # We will use nested dictionaries, where the first key is the starting city
    # and the second key is the destination city, and the value is the distance
    # between the two cities
    distances_table = dict()
    for city_key in cities:
      distances_table[city_key] = dict()
      distances_from_this_city = distances_matrix.readline().rstrip().split(' ')[1:]
      city_n = 0
      for city in cities:
        distances_table[city_key][city] = distances_from_this_city[city_n]
        city_n += 1

    # Return distances table
    return distances_table

def generate_initial_population(size, individual_size):
  """ Generate a random starting population.

  Keyword arguments:
  size -- the size of the population
  individual_size -- the size of every individual

  Return value:
  population -- a list containing the individuals of the starting population
  """

  population = []
  for i in range(size):
    individual = []
    cities_visited = 0
    for j in range(individual_size):
      # Take indices from 0 (B) to the last city remaining (initially, cities-2)
      # Individual size is cities - 2, that is why it is the starting value
      # This helps us build better individuals than if we chose random numbers
      individual.append(randint(0, individual_size - cities_visited))
      cities_visited += 1
    population.append(individual)
  return population

def get_fitness(individual, cities, distances_table):
  """ Get the fitness of an individual.

  Keyword arguments:
  individual -- the individual to evaluate
  cities -- a list containing the cities excluding the first one
  distances_table -- the distances table obtained through get_distances_table

  Return value:
  fitness -- the fitness of that individual
  """

  last_city = constants.STARTING_CITY
  fitness = 0
  clist = cities.copy()
  for gene in individual:
    # Get the city with index = gene in the list and remove it
    # If out of bounds, get the last (this can happen when crossing individuals or mutating)
    index = gene if (gene < len(clist)) else len(clist)-1
    current_city = clist.pop(index)
    # Update fitness and mark this city as the last one visited
    fitness = fitness + int(distances_table[last_city][current_city])
    last_city = current_city
  # When we get here, we have every city except the last: simply add it
  fitness = fitness + int(distances_table[last_city][cities[0]])
  last_city = clist[0]
  # And then, back to the first city
  fitness = fitness + int(distances_table[last_city]['A'])
  return fitness

def mutation(individual, cities, probability):
  """ Mutate an individual, changing one of its genes with a given probability.

  Keyword arguments:
  individual -- the individual to mutate
  cities --  a list containing the cities excluding the first one
  probability -- the probability of the mutation to happen

  Return value:
  individual -- the mutated individual
  """

  if(random() >= probability):
    return individual
  mutation_index = randint(0, len(individual) - 1)
  mutation_value = randint(0, len(cities) - 1)
  individual[mutation_index] = mutation_value
  return individual

def cross(parent1, parent2):
  """ Cross two individuals, mixing their genes to create two new individuals.

  Cross is a simple one-point cross, with that point being in half

  Keyword arguments:
  parent1, parent2 -- the individuals to cross

  Return value: 
  child1, child2 -- the new individuals
  """

  crossing_point = int(len(parent1) / 2)
  child1 = parent1[0:crossing_point] + parent2[crossing_point:len(parent2)]
  child2 = parent2[0:crossing_point] + parent1[crossing_point:len(parent1)]
  return child1, child2

def get_population_fitness(population, flist, cities, distances_table):
  """ Update fitness list in order to avoid extra calculations

  Keyword arguments:
  population -- the complete population of individuals
  flist -- the list of fitness we have to update
  cities -- the list of cities without the starting one (we need it for calling get_fitness)
  distances_table -- the data structure with the cities and distances between them (we need it for calling get_fitness)

  Return value:
  flist -- the updated list
  """

  for i in range(len(population)):
    flist[i] = get_fitness(population[i], cities, distances_table)
  return flist



# Get the distances table from the distances file
distances = read_distances_table(constants.DISTANCES_FILE)

# Get the list of the cities without the first one for evaluation
cities_list = list(distances.keys())
cities_list.sort()
cities_list.remove('A')

# Generate the starting population
starting_population = generate_initial_population(constants.POPULATION_SIZE, len(cities_list) - 1)

fitness_list = [float("inf") for i in range(len(starting_population))]
fitness_list = get_population_fitness(starting_population, fitness_list, cities_list, distances)
print(fitness_list)


