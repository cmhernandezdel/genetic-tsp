from random import randint

"""
Genetic algorithm to solve the Travelling Salesman Problem.

Each individual is a list containing the position of the city visited in that order,
i.e., if the cities are: A, B, C, D, E, F
each individual will be something like:
2, 1, 3, 1, 0
where, taking into account the cities from B to F only (since A is always the first one),
and assuming that if we choose a city that is out of bounds, we take the last,
this would mean that the order is:
A (implicit), D, C, F, E, B, A (implicit, since we have to return to the first city)

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

def generate_initial_population(size, distances_table, individual_size):
  """ Generate a random starting population.

  Keyword arguments:
  size -- the size of the population
  distances_table -- the distances table obtained through read_distances_table
  individual_size -- the size of every individual

  Return value:
  population -- a list containing the individuals of the starting population
  """
  number_of_cities = len(distances_table.keys()) - 2
  population = []
  for i in range(size):
    individual = []
    cities_visited = 0
    for j in range(individual_size):
      # Take indices from 0 (B) to the last city remaining (initially cities-2)
      individual.append(randint(0, number_of_cities - cities_visited))
      # Substract 1 every time we visit a city
      cities_visited += 1
    population.append(individual)
  return population


distances = read_distances_table("distances.txt")
starting_population = generate_initial_population(10, distances, 5)
print(starting_population)
