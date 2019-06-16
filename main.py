def read_distances_table(distances_file):
  """ Read distances from a matrix file.

  Keyword arguments:
  distances_file -- the file where the matrix is stored
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


distances = read_distances_table("distances.txt")
print(distances)
