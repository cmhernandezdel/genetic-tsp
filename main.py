def read_distances_table(distances_file):
  """ Read distances from a matrix file.

  Keyword arguments:
  distances_file -- the file where the matrix is stored
  """

  with open(distances_file, 'r') as distances_matrix:
    # Get the names of the cities and how many of them there are
    cities = distances_matrix.readline().rstrip().split(' ')[2:]
    number_of_cities = len(cities)

    # Get the distances between the cities and store them in a data structure
