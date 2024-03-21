from itertools import compress
import random
import time
import matplotlib.pyplot as plt
import numpy as np

from data import *


def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]


def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))


def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness


items, knapsack_max_capacity = get_big()
print(items)

population_size = 100
generations = 200
n_selection = 20
n_elite = 2

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), population_size)
for _ in range(generations):

    # TODO: implement genetic algorithm

    population.sort(key=lambda x: fitness(items, knapsack_max_capacity, x), reverse=True)

    elites = population[:n_elite]

    population = population[n_elite:]

    fitness_values = [fitness(items, knapsack_max_capacity, i) for i in population]
    total_fitness = sum(fitness_values)
    prob_population = np.array(fitness_values)/total_fitness

    non_zero_entries = np.count_nonzero(prob_population)
    if non_zero_entries >= n_selection:
        selected_indexes = np.random.choice(len(population), size=n_selection, p=prob_population, replace=False)
    else:
        selected_indexes = np.random.choice(len(population), size=n_selection, p=None, replace=False)

    selected_population = [population[i] for i in selected_indexes]

    population = []
    for _ in range(int((population_size - n_elite) / 2)):
        parent1, parent2 = random.sample(selected_population, 2)

        child1 = parent1[int(len(parent1) / 2):] + parent2[:int(len(parent2) / 2)]
        child2 = parent2[int(len(parent2) / 2):] + parent1[:int(len(parent1) / 2)]

        mutation_rate = 1.0

        if random.random() < mutation_rate:
            tmp = random.randint(0, len(child1)-1)
            child1[tmp] = not child1[tmp]

        if random.random() < mutation_rate:
            tmp = random.randint(0, len(child1)-1)
            child2[tmp] = not child2[tmp]

        population.extend([child1, child2])

    population.extend(elites)

    population_history.append(population)

    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)

end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
