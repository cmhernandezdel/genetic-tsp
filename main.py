from random import randint
from random import random
from random import choice
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

def population_cross(population):
  """ Cross the individuals in an intermediate population.

  Keyword arguments:
  population -- the intermediate population to cross

  Return value:
  intermediate_population -- the crossed population
  """
  intermediate_population = []
  iterations = len(population) if len(population) % 2 == 0 else len(population) + 1
  for i in range(iterations):
    child1, child2 = cross(choice(population), choice(population))
    intermediate_population.append(child1)
    intermediate_population.append(child2)
  # We need to keep the population size equal
  if(len(population) != len(intermediate_population)):
    intermediate_population.remove(choice(intermediate_population))
  return intermediate_population

def population_mutation(population, probability, cities):
  """ Mutate the population

  Keyword arguments:
  population -- the population to mutate
  probability -- the probability of the mutation to happen
  cities --  a list containing the cities excluding the first one

  Return value:
  intermediate_population -- the mutated population
  """
  intermediate_population = []
  for individual in population:
    intermediate_population.apppend(mutation(individual, cities, probability))
  return intermediate_population

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


def selection(population, flist):
  """ Do N tourneys among the individuals in population, simulating natural selection

  Keyword arguments:
  population -- the complete population of individuals
  flist -- the list of fitness of the population

  Return value:
  intermediate_population -- the new population
  """
  intermediate_population = []
  while len(intermediate_population) < len(population):
    arena = []
    while len(arena) < constants.TOURNEY_SIZE:
      # Append just the index because it is faster and we do not need anything else
      arena.append(randint(0, len(population) - 1))
    # Search for the lowest fitness individual  
    min_index = 0  
    min_val = population[0]
    for ind in arena:
      if(population[ind] < min_val):
        min_val = population[ind]
        min_index = ind
    # Add that individual to the population
    intermediate_population.append(population[arena[min_index]])
  return intermediate_population

def get_best_individual_and_fitness(population, flist):
  """ Return the best individual and fitness of the current population

  Keyword arguments:
  population -- the complete population of individuals
  flist -- the list of fitness of the population

  Return value:
  best_individual -- the best individual of the population
  best_fitness -- the fitness of best_individual
  """
  best_fitness = min(flist)
  best_individual = population[population.index(best_fitness)]
  return best_individual, best_fitness
    

# Get the distances table from the distances file
distances = read_distances_table(constants.DISTANCES_FILE)

# Get the list of the cities without the first one for evaluation
cities_list = list(distances.keys())
cities_list.sort()
cities_list.remove('A')

# Generate the starting population and starting parameters
current_population = generate_initial_population(constants.POPULATION_SIZE, len(cities_list) - 1)
fitness_list = [float("inf") for i in range(len(current_population))]
last_fitness = float("inf")
iteration = 0

while(True):
  # Update fitness list with the current population, best individual and best fitness
  fitness_list = get_population_fitness(current_population, fitness_list, cities_list, distances)
  current_best_individual, current_best_fitness = get_best_individual_and_fitness(current_population, fitness_list)
  # Print info if fitness changed
  if(current_best_fitness != last_fitness):
    print("Iteration " + str(iteration) ", best fitness: " + str(current_best_fitness))
  # Stop condition: if best fitness is lower than a given threshold
  if(current_best_fitness < constants.THRESHOLD):
    break

  # Operators: selection, then cross, then mutation
  after_selection_population = selection(current_population, fitness_list)
  after_cross_population = population_cross(after_selection_population)
  after_mutation_population = population_mutation(after_cross_population, constants.MUTATION_PROBABILITY, cities_list)
  



