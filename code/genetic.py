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
import click
from pytictoc import TicToc

genes = 13  # The length of each individual's genetic material
individuals = 20  # The number of individuals in the population
pressure = 5  # How many individuals are selected for reproduction. Must be greater than 2
mutation_chance = 0.4  # The probability that an individual mutates
generations = 15  # The number of generations that we will evolve
crossover_type = 1  # The crossover type, can be 1 or 2
mutation_type_random = True  # Set if the mutation is random or +-1


def print_variable_info():
    print("genes: %d" % genes)
    print("individuals : %d" % individuals)
    print("pressure: %d" % pressure)
    print("mutation_chance: %d" % mutation_chance)
    print("generations: %d" % generations)
    print("crossover_type: %d" % crossover_type)
    print("mutation_type_random: %d" % mutation_type_random)


def individual():
    """
        Create a random individual using the function defined in our
        NGINX generator
    """
    config = generate_random_config()
    # return [fitness(config), config]
    return config


def initialize():
    """
        Create a new population of individuals
    """
    return [individual() for i in range(individuals)]


def fitnes(individual):
    """
        Calculates the fitness of a specific individual.
    """
    # return random.randint(1, 99)
    # return 99
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


def crossover(individual1, individual2):

    # Genetic material from parents is mixed into the new individual
    if crossover_type == 1:
        result = crossover_one_point(individual1, individual2)
    else:
        result = crossover_two_points(individual1, individual2)

    return (fitnes(result), result)


def selection_and_reproduction(population):
    """
        Scores all elements of the population and keeps the best.
        by saving them under 'selected'.
        Then mix the genetic material of the chosen ones to create new individuals and
        fill in the population (also keeping a copy of the selected individuals without the
        modify).
    """

    # print("population")
    # pprint(population)

    population = sorted(population, reverse=True)  # Sorts the ordered pairs and is left alone with the array of values

    # print("scored")
    # pprint(population)

    selected = population[(len(population) - pressure):]  # This line selects the 'n' individuals from the end, where n is given by 'pressure'.

    # Genetic material is mixed to create new individuals
    for i in range(len(population) - pressure):
        parent = random.sample(selected, 2)  # Two parents are selected

        population[i] = crossover(parent[0][1], parent[1][1])

    # print("crossed")
    # pprint(population)

    # Sort again the population
    population = sorted(population, reverse=True)

    # print("sorted")
    # pprint(population)

    return population  # The array now has a new population of individuals, which are returned.


def mutate(population):
    """
        Individuals mutate randomly. Without the mutation of new genes the
        solution could never be reached.
    """
    for i in range(len(population) - pressure):
        if random.random() <= mutation_chance:  # Every individual in the population (except the parents) has a chance to mutate.
            print("muta")
            gen = random.randint(0, genes - 1)  # A random gen is chosen

            new_value = None

            if mutation_type_random:
                new_value = generate_random_config()[gen]  # and a new value for this gen

                # It is important to see that the new value is not equal to the old one.
                while new_value == population[i][1][gen]:
                    new_value = generate_random_config()[gen]

            else:
                # In this case we are randomly adding(+) or substracting(-) 1
                new_value = population[i][1][gen]
                new_value += 1 if random.random() < 0.5 else -1

            # Applying mutation
            population[i][1][gen] = new_value

    return population


def print_results(initial_population, last_population):
    """
        Print the results
    """
    print("")
    print("Población de %d individuos durante %d generaciones" % (individuals, generations))
    print("Población inicial:")
    pprint(initial_population)
    print("Población final:")
    pprint(last_population)


@click.command()
@click.option('--individuals', '-i', 'individuals_number', help='Number of individuals', default=16, prompt=True)
@click.option('--crossover-one-point', '-1', 'crossover', help='Crossover function in one point', flag_value=1, default=True)
@click.option('--crossover-two-points', '-2', 'crossover', help='Crossover function in two points', flag_value=2)
@click.option('--random-mutation/--no-random-mutation', 'mutation', is_flag=True, help='Random value mutation or +-1', default=False, prompt=True)
def main(individuals_number, crossover, mutation):

    global individuals
    individuals = individuals_number
    global crossover_type
    crossover_type = crossover
    global mutation_type_random
    mutation_type_random = mutation

    print_variable_info()

    t = TicToc()
    t.tic()

    # Initialize a population
    population = initialize()

    population = [(fitnes(i), i) for i in population] # Calculates the fitness of each individual, and stores it in pairs ordered in the form (5 , [1,2,1,1,1,4,1,8,9,4,1])

    initial_population = sorted(population, reverse=True)

    # Evolves the population
    for i in range(generations):
        population = selection_and_reproduction(population)
        pprint(population)
        population = mutate(population)

    # Print the results
    print_results(initial_population, population)

    t.toc()


if __name__ == "__main__":

    main()
