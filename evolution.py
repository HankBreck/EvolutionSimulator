# [0]: Speed, [1]: height, [2]: weight, [3]: food/water needs, [4]: insulation

import random
import numpy as np
import operator
from collections import defaultdict
import matplotlib.pyplot as plt

class NewSpecies():
    def __init__(self):
        self.speed = np.random.randint(45, 55)
        self.height = np.random.randint(45, 55)
        self.weight = np.random.randint(45, 55)
        self.req_nourish = np.random.randint(45,55)
        self.insulation = np.random.randint(45,55)

        # Phenotype attribute is used for storing all of the atributes, and it acts as an organism in this program.
        self.phenotype = tuple([self.speed, self.height, self.weight, self.req_nourish, self.insulation])

def form_population(k):
    population = []
    for i in range(k):
        new_organism = NewSpecies()
        population.append(new_organism.phenotype)
    return population

# These are the hardcoded fitness functions designed for my SL IB Biology design lab

def calc_fitnessT1(organism, j): # For control. Tropical the entire time.
    fitness = organism[0]*0.21 + organism[1]*0.23 + organism[2]*0.2 + organism[3]*0.18 + organism[4]*0.18

def calc_fitnessT2(organism, j): # For variation number 1 (Tropical, Desert, IA, RoP)
    if j < 250: # Represents the tropical environment
        fitness = organism[0]*0.21 + organism[1]*0.23 + organism[2]*0.2 + organism[3]*0.18 + organism[4]*0.18
    elif j < 500: # Represents the desert environment
        fitness = organism[0]*0.22 + organism[1]*0.18 + organism[2]*0.2 + organism[3]*0.23 + organism[4]*0.17
    elif j < 750: # Represents the ice age environment
        fitness = organism[0]*0.18 + organism[1]*0.16 + organism[2]*0.2 + organism[3]*0.22 + organism[4]*0.24
    elif j < 1000: # Represents the rise of predators environment
        fitness = organism[0]*0.26 + organism[1]*(8/(organism[1]+1)) + organism[2]*0.2 + organism[3]*0.2 + organism[4]*0.2
    return fitness

def calc_fitnessT3(organism, j): # For variation number 2 (Desert, Tropical, IA, RoP)
    if j < 250: # Represents the desert environment
        fitness = organism[0]*0.22 + organism[1]*0.18 + organism[2]*0.2 + organism[3]*0.23 + organism[4]*0.17
    elif j < 500: # Represents the tropical environment
        fitness = organism[0]*0.21 + organism[1]*0.23 + organism[2]*0.2 + organism[3]*0.18 + organism[4]*0.18
    elif j < 750: # Represents the ice age environment
        fitness = organism[0]*0.18 + organism[1]*0.16 + organism[2]*0.2 + organism[3]*0.22 + organism[4]*0.24
    elif j < 1000: # Represents the rise of predators environment
        fitness = organism[0]*0.26 + organism[1]*(8/(organism[1]+1)) + organism[2]*0.2 + organism[3]*0.2 + organism[4]*0.2
    return fitness

def calc_fitnessT4(organism, j): # For variation number 3 (IA, Tropical, Desert, RoP)
    if j < 250: # Represents the ice age environment
        fitness = organism[0]*0.18 + organism[1]*0.16 + organism[2]*0.2 + organism[3]*0.22 + organism[4]*0.24
    elif j < 500: # Represents the tropical environment
        fitness = organism[0]*0.21 + organism[1]*0.23 + organism[2]*0.2 + organism[3]*0.18 + organism[4]*0.18
    elif j < 750: # Represents the desert environment
        fitness = organism[0]*0.22 + organism[1]*0.18 + organism[2]*0.2 + organism[3]*0.23 + organism[4]*0.17
    elif j < 1000: # Represents the rise of predators environment
        fitness = organism[0]*0.26 + organism[1]*(8/(organism[1]+1)) + organism[2]*0.2 + organism[3]*0.2 + organism[4]*0.2
    return fitness

def calc_fitnessT5(organism, j): # For variation number 4 (Tropical, IA, Desert, RoP)
    if j < 250: # Represents the tropical environment
        fitness = organism[0]*0.21 + organism[1]*0.23 + organism[2]*0.2 + organism[3]*0.18 + organism[4]*0.18
    elif j < 500: # Represents the ice age environment
        fitness = organism[0]*0.18 + organism[1]*0.16 + organism[2]*0.2 + organism[3]*0.22 + organism[4]*0.24
    elif j < 750: # Represents the desert environment
        fitness = organism[0]*0.22 + organism[1]*0.18 + organism[2]*0.2 + organism[3]*0.23 + organism[4]*0.17
    elif j < 1000: # Represents the rise of predators environment
        fitness = organism[0]*0.26 + organism[1]*(8/(organism[1]+1)) + organism[2]*0.2 + organism[3]*0.2 + organism[4]*0.2
    return fitness

def sort_population(population, j): # Change 'calc_fitnessT1' in both locations to change trial
    pop_sorted = defaultdict(list)
    for organism in population:
        if organism not in pop_sorted:
            pop_sorted[organism].append(calc_fitnessT2(organism, j))
        else:
            x = NewSpecies().phenotype # This is required in case the phenotype already exists. The dictionary doesn't let use store multiple instances of the same phenotype.
            pop_sorted[x].append(calc_fitnessT2(x, j))
    return sorted(pop_sorted.items(), key = operator.itemgetter(1), reverse=True)

def select_from_population(population_sorted, best_organisms, lucky_few):
    next_gen = []
    for i in range(best_organisms):
        next_gen.append(population_sorted[i][0])
    for i in range(lucky_few):
        next_gen.append(random.choice(population_sorted)[0])
    random.shuffle(next_gen)
    return next_gen

def create_child(parent1, parent2):
    child_arr = []
    for i in range(len(parent1)):
        if (100 * random.random() > 50): # Randomly selects whether to use the attribute from parent1 or parent 2. This is our method of crossing over.
            child_arr.append(parent1[i])
        else:
            child_arr.append(parent2[i])
    child = tuple(child_arr)
    return child

def create_children(breeders, number_of_children):
    next_pop = []
    for i in range(len(breeders)):
        for j in range(number_of_children):
            next_pop.append(create_child(breeders[i], breeders[len(breeders) - 1 - i]))
    return next_pop

def mutate_organism(organism):
    temp_organism = list(organism)
    index_mod = int(random.random() * len(organism))
    if (100 * random.random() > 50):
        temp_organism[index_mod] = organism[index_mod] + 5
    else:
        temp_organism[index_mod] = organism[index_mod] - 5
    organism = tuple(temp_organism)
    return organism

def mutate_population(population, chance_of_mutation): # chance_of_mutation must be a number between 0 & 100 (representing the % chance of a mutation occuring)
    for i in range(len(population)):
        if (random.random() * 100 < chance_of_mutation):
            population[i] = mutate_organism(population[i])
    return population

def run_game(pop):
    pop1 = pop
    population = pop
    global j
    j = 0 # Keeps count of what generation we are on
    avg_pops = [] # List of all of the average phenotypes from each generation
    for i in range(1000): # Runs 1000 generations
        pop_sorted = sort_population(population, j)
        next_gen = select_from_population(pop_sorted, 22, 3)
        next_pop = create_children(next_gen, 2)
        population = mutate_population(next_pop, 1)
        average_pop = tuple(np.mean(population, axis=0))
        avg_pops.append(average_pop)
        j += 1
    return avg_pops


if __name__ == '__main__':
    population = form_population(50) # Makes the population of 50 organisms
    def average_all(iter):
        average_all_arr = []
        for i in range(iter):
            X = run_game(population)
            average_all_arr.append(X)
        xyz = []
        for i in range(len(average_all_arr[1])): # Creates the xyz list with the averages of all 10 trials
             Y = (average_all_arr[0][i], average_all_arr[1][i], average_all_arr[2][i], average_all_arr[3][i], average_all_arr[4][i])
             y = list(np.mean(Y, axis=0))
             xyz.append(y)
        print("Attributes after first env: ", xyz[249])
        print("Attributes after second env: ", xyz[499])
        print("Attributes after third env: ", xyz[749])
        print("Attributes after fourth env: ", xyz[999])
        attribute1 = []
        attribute2 = []
        attribute3 = []
        attribute4 = []
        attribute5 = []
        for iter in xyz:
            attribute1.append(iter[0])
            attribute2.append(iter[1])
            attribute3.append(iter[2])
            attribute4.append(iter[3])
            attribute5.append(iter[4])
        j1 = []
        for j in range(1000):
            j1.append(j)
        plt.plot(j1, attribute1, color='blue', label='Speed', linewidth=1)
        plt.plot(j1, attribute2, color='red', label='Height', linewidth=1)
        plt.plot(j1, attribute3, color='black', label='Weight', linewidth=1)
        plt.plot(j1, attribute4, color='purple', label='Food/Water Needs', linewidth=1)
        plt.plot(j1, attribute5, color='green', label='Insulation', linewidth=1)
        plt.xlabel('Generation')
        plt.ylabel('Attribute Score')
        plt.legend(loc='upper left')
        plt.title('Change in Attribute Scores Based on Generation')
        plt.show()
    average_all(10) # 10 is the number of trials used to reduce the random error of the program
