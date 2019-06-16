from random import choice

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
  """
  cities_list = list(distances_table.keys())
  population = []
  for i in range(size):
    individual = []
    for i in range(individual_size):
      individual.append(choice(cities_list))
    population.append(individual)
  return population


distances = read_distances_table("distances.txt")
starting_population = generate_initial_population(10, distances, 5)
print(starting_population)
