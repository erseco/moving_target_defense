#!/usr/bin/env python3
"""
    This is the main genetic algorithm based on the sample
    code of TR4NSDUC7OR for an article in robologs.net
"""
__author__ = "Ernesto Serrano"
__license__ = "GPLv3"
__email__ = "erseco@correo.ugr.es"

import random
from fitness import *
from generate_nginx_config import *

genes = 13  # The length of each individual's genetic material
individuals = 20  # The number of individuals in the population
pressure = 5  # How many individuals are selected for reproduction. Must be greater than 2
mutation_chance = 0.4  # The probability that an individual mutates
generations = 20  # The number of generations that we will evolve


def individual():
    """
        Create a random individual using the function defined in our
        NGINX generator
    """
    return generate_random_config()


def initialize():
    """
        Create a new population of individuals
    """
    return [individual() for i in range(individuals)]


def fitnes(individual):
    """
        Calculates the fitness of a specific individual.
    """
    return calculate_fitness(individual)


def crossover_one_point(individual1, individual2):
    """
        Executes a one point crossover on the input individuals.
    """

    # A random crosspoint is chosen to make the exchange
    crosspoint = random.randint(1, genes - 1)

    return individual2[:crosspoint] + individual1[crosspoint:]


def crossover_two_points(individual1, individual2):
    """
        Executes a two-point crossover on the input individuals.
    """

    # Two random cross points is chosen to make the exchange
    crosspoint1 = random.randint(1, genes - 3)
    crosspoint2 = random.randint(crosspoint1, genes - 1)

    return individual1[:crosspoint1] + individual2[crosspoint1:crosspoint2] + individual1[crosspoint2:]


def selection_and_reproduction(population):
    """
        Scores all elements of the population and keeps the best.
        by saving them under 'selected'.
        Then mix the genetic material of the chosen ones to create new individuals and
        fill in the population (also keeping a copy of the selected individuals without the
        modify).
    """
    scored = [(fitnes(i), i) for i in population]  # Calculates the fitness of each individual, and stores it in pairs ordered in the form (5 , [1,2,1,1,1,4,1,8,9,4,1])
    scored = [i[1] for i in sorted(scored, reverse=True)]  # Sorts the ordered pairs and is left alone with the array of values
    population = scored

    selected = scored[(len(scored) - pressure):]  # This line selects the 'n' individuals from the end, where n is given by 'pressure'.

    # Genetic material is mixed to create new individuals
    for i in range(len(population) - pressure):
        parent = random.sample(selected, 2)  # Two parents are selected

        # Genetic material from parents is mixed into the new individual
        # population[i] = crossover_one_point(parent[0], parent[1])
        population[i] = crossover_two_points(parent[0], parent[1])

    return population  # The array now has a new population of individuals, which are returned.


def mutation(population):
    """
        Individuals mutate randomly. Without the mutation of new genes the
        solution could never be reached.
    """
    for i in range(len(population) - pressure):
        if random.random() <= mutation_chance:  # Every individual in the population (except the parents) has a chance to mutate.
            gen = random.randint(0, genes - 1)  # A random gen is chosen
            new_value = generate_random_config()[gen]  # and a new value for this gen

            # It is important to see that the new value is not equal to the old one.
            while new_value == population[i][gen]:
                new_value = generate_random_config()[gen]

            # Applying mutation
            population[i][gen] = new_value

    return population


def print_latex_table(population):
    """
        Print the results as latex table to easily put in the memory. Set red
        color for invalid values
    """

    print('\\begin{table}[H]')
    print('\\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|l|l|}')
    print('\\hline')
    print('\\textbf{1} & \\textbf{2} & \\textbf{3} & \\textbf{4} & \\textbf{5} & \\textbf{6} & \\textbf{7} & \\textbf{8} & \\textbf{9} & \\textbf{10} & \\textbf{11} & \\textbf{12} & \\textbf{13} \\\\ \\hline')

    for individual in population:

        for i in range(genes):

            if i == genes - 1:
                print("%d \\\\ \\hline" % individual[i])
            elif i == 10 and individual[i] > 3:
                print("{\\color[HTML]{FE0000}%d}  &  " % individual[i], end='')
            elif i == 11 and individual[i] > 4:
                print("{\\color[HTML]{FE0000}%d}  &  " % individual[i], end='')
            else:
                print("%d  &  " % individual[i], end='')

    print('\\end{tabular}')
    print('\\end{table}')


def print_results(initial_population, last_population):
    """
        Print the results in LaTeX format to easily put in the memory
    """
    print("")
    print("")
    print("\\subsection{Población de %d individuos durante %d generaciones}" % (individuals, generations))
    print("Resultados para una población de %d individuos durante %d generaciones:" % (individuals, generations))
    print("Población inicial:")
    print_latex_table(initial_population)
    print("Población final:")
    print_latex_table(last_population)
    print("Configuración de NGINX")
    print('\\begin{lstlisting}[label={lst:nginx_config_random},caption={Configuración de NGINX tras %d generaciones}]' % generations)
    print(generate(last_population[len(population) - 1]))
    print('\\end{lstlisting}')


if __name__ == "__main__":

    # Initialize a population
    population = initialize()

    initial_population = population

    # Evolves the population
    for i in range(generations):
        population = selection_and_reproduction(population)
        population = mutation(population)

    # Print the results
    print_results(initial_population, population)
