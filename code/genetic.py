#!/usr/bin/env python3
"""
    This is the main genetic algorythm based on the sample
    code of TR4NSDUC7OR for an article in robologs.net
"""
__author__ = "Ernesto Serrano"
__license__ = "GPLv3"
__email__ = "erseco@correo.ugr.es"

import random
from fitness import *

genes = 13  # The length of each individual's genetic material
individuals = 20  # The number of individuals in the population
pressure = 5  # How many individuals are selected for reproduction. Must be greater than 2
mutation_chance = 0.4  # The probability that an individual mutates
generations = 30  # The number of generations that we will evolve


def individual():
    """
        Create a random individual using the funtion defined in our
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
    return fitness(individual)


def selection_and_reproduction(population):
    """
        Scores all elements of the population and keeps the best.
        by saving them under 'selected'.
        Then mix the genetic material of the chosen ones to create new individuals and
        fill in the population (also keeping a copy of the selected individuals without the
        modify).

        Finally mutate to individuals.

    """
    scored = [(fitnes(i), i) for i in population]  # Calculates the fitness of each individual, and stores it in pairs ordered in the form (5 , [1,2,1,1,1,4,1,8,9,4,1])
    scored = [i[1] for i in sorted(scored, reverse=True)]  # Sorts the ordered pairs and is left alone with the array of values
    population = scored

    selected = scored[(len(scored)-pressure):]  # This line selects the 'n' individuals from the end, where n is given by 'pressure'.

    # Genetic material is mixed to create new individuals
    for i in range(len(population)-pressure):
        gen = random.randint(1, genes - 1)  # A gen is chosen to make the exchange
        parent = random.sample(selected, 2)  # Two parents are selected

        population[i][:gen] = parent[0][:gen]  # Genetic material from parents is mixed into the new individual
        population[i][gen:] = parent[1][gen:]

    return population  # The array now has a new population of individuals, which are returned.


def mutation(population):
    """
        Individuals mutate randomly. Without the mutation of new genes the
        solution could never be reached.
    """
    for i in range(len(population)-pressure):
        if random.random() <= mutation_chance:  # Every individual in the population (except the parents) has a chance to mutate.
            gen = random.randint(0, genes - 1)  # A random gen is chosen
            new_value = generate_random_config()[gen]  # and a new value for this gen

            # It is important to see that the new value is not equal to the old one.
            while new_value == population[i][gen]:
                new_value = generate_random_config()[gen]

            # Applying mutation
            population[i][gen] = new_value

    return population


if __name__ == "__main__":
    # Initialize a population
    population = initialize()

    print("Initial population:")
    pprint(population)  # The initial population is shown

    # Evolves the population
    for i in range(generations):
        population = selection_and_reproduction(population)
        population = mutation(population)

    # Print the results
    print("Final Population:")
    pprint(population)  # The evolved population is shown

    print("")
    print("Print a random population element as NGINX configuration:")
    print(generate(random.choice(population)))
