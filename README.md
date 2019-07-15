# genetic-tsp
Genetic algorithm to solve Traveling Salesman Problem.

<h2> The problem </h2>
Travelling Salesman Problem is a classic problem in theoretical computer science. It asks the following question: "If you were a salesman and had to travel to a list of cities, visiting each once and returning to the first, which would be the optimal route to minimize distance?"

This is a classic example of NP-hard problem, and it is important in optimization tasks.

The problem has many variants: for example, distance from A to B can be not equal to distance from B to A (for example, if we were to minimize the cost of plane tickets).

For more info on the TSP check <a href="https://books.google.es/books?id=BXBGAAAAYAAJ&redir_esc=y">this book</a>.

<h2> Genetic algorithms </h2>
Genetic algorithms are metaheuristics based on natural selection and evolution of living beings. Applying concepts such as natural selection, procreation and mutations, they are capable of finding acceptable solutions to a lot of optimization problems. They are, however, unable to find optimal solutions, because there is no way of knowing if the best solution was reached. 

In order to understand the algorithm, some key concepts must be explained, such as gene, individual, population or tournament. A lot of quick definitions can be found in the <a href="https://en.wikipedia.org/wiki/Genetic_algorithm">Wikipedia article</a>, and there are several books that cover this topic.

<h2> Files found in this repository </h2>
<h3> Distances file </h3>
The distances file is a matrix representation of the cities and the distances between them. It contains one header line with as many cities as desired and then as many lines as cities. Each one of these lines starts with a city label and then the distances.

There are no constraints about the names of the cities, they can be any string. However, there are one key constraint that must be satisfied for the algorithm to work:
<ul>
  <li> The cities and distances must be delimited by whitespaces (' ') </li>
</ul>

<h3> Constants file </h3>
This file contains system-wide constants that are used in the algorithm, especially parameters. By editing this file, the results of the algorithm may vary, and it is supposed to be like a configuration file. In this file, the following parameters can be found:
<ul>
  <li> DISTANCES_FILE: Represents the path (relative path is preferred) of the distances file. </li>
  <li> STARTING_CITY: Represents the name of the starting city. Since city names can be any string, you must make sure that your starting city is edited in this file accordingly. Short, one-letter names are preferred for clarity. </li>
  <li> POPULATION_SIZE: Represents the number of individuals in the population. More individuals may be useful to improve the quality of the results, since variation is more likely if there are more individuals. However, increasing population size will decrease computing speed, thus making the algorithm slower. A population between 20 and 100 individuals is recommended. </li>
  <li> TOURNAMENT_SIZE: Represents how many individuals are chosen for the tournament (selection operator). A bigger tournament will most likely cause premature convergence. A tournament size between 3 and 5 is recommended. </li>
  <li> THRESHOLD: Represents the threshold for the fitness to be acceptable, and it depends completely on the configuration of the cities. If the threshold is high, the quality of the solutions may be worse. A negative threshold means that this condition will never be met. </li>
  <li> MUTATION_PROBABILITY: Represents the probability for a certain individual to change a random gene. A high mutation rate will mean that solutions are more randomized, but a low mutation rate may produce premature convergence and stagnation. Value will vary from one problem to another and has to be determined experimentally.</li>
</ul>

<h3> Main file </h3>
This file contains the algorithm itself. You do not need to touch anything in this file to make the algorithm work.

<h2> License </h2>
This work is protected by a GNU GPL v3 license. This means that you can use, modify and distribute this code as you want, but the license of the derivative works cannot be more restrictive than this one (i.e., has to be at least as free as GPL v3).
