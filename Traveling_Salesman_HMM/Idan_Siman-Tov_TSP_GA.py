
import numpy as np
import statistics as stats
import random


cities = ['London', 'Venice', 'Dunedin', 'Singapore', 'Beijing', 'Phoenix', 'Tokyo', 'Victoria']    
city_inds = {'London':0, 'Venice':1, 'Dunedin':2, 'Singapore':3, 'Beijing':4, 'Phoenix':5, 'Tokyo':6, 'Victoria':7} #names to numbers

data = [] 

def open_CSV(): 
   data_csv = open(r"C:\Users\idansim\Dropbox\Masters\Semester 4\CS 223 Bioinformatics\Homework\programing_assignment_1\TS_Distances_Between_Citie.csv")
   data_table = []
   for r in data_csv:
         for row in r.split('\n'):
            current_row = row.split(',')
            fixed_row = []
            for item in current_row:
               try:
                  fixed_row.append(int(item)) 
               except:
                  pass
            if fixed_row != []:
               data_table.append(fixed_row)
   return data_table


def array_to_sequence(index_array):
    chars = [str(int) for int in index_array]
    return(''.join(chars))


def fitness(individual): # the fitness is the total distance traveled. The distances between the cities in sequence are summed up.
    steps = len(individual) - 1
    distance = 0
    for x in range(0, steps):
        thisCity = int(individual[x])
        nextCity = int(individual[x + 1])
        distance += data[thisCity][nextCity]
    return distance


def generate_rand_pop(pop_num, max_index): #this will generate a random starting pop
    pop = []
    for x in range(0, pop_num):
        index_array = np.random.permutation(range(0,max_index)).tolist()
        pop.append((array_to_sequence(index_array)))
    return pop


def get_fitness(population): #iterates through all sequences and gets fitnesses
    distances = []
    for individual in population:
        distances.append(fitness(individual))
    return distances

def select_parents(population, fitnesses, numParents):
    parents = []
    for x in range(0, numParents):
        mostFitIndex = fitnesses.index(min(fitnesses)) #minimum distance between individuals
        parents.append(population[mostFitIndex]) #add it to a list
        del fitnesses[mostFitIndex] #delete fitness value, next minimum will be selected for the next iteration
        del population[mostFitIndex] #delete sequence
    return parents


def mutate_code(individual):
    index_array = list(individual)
    city1 = int(random.random()*len(individual))
    city2 = int(random.random()*len(individual)) #select two cities for swapping
    index_array[city1], index_array[city2] = index_array[city2], index_array[city1] #swap them
    return array_to_sequence(index_array)
    return individual   


def crossover_code(parent1, parent2):
    child = ""
    half = int(len(parent1)/2)
    rand1 = int(random.random()*half)
    parent1Half = parent1[rand1: rand1 + half] #select a half of parent1 randomly
    parent2Half = ""
    for char in parent2:
        if char not in parent1Half:
            parent2Half += char #subsequence of parent2 using missing values
    for x in range(0, len(parent1Half)):
        child += parent2Half[x] #build a child off of parent2
        if x == rand1: #if you have reached the original location in parent1, add parent1 sequence
            child += parent1Half
    return child


def reproduce(parent1, parent2, mutProb): #perform a crossover_code
    child = crossover_code(parent1, parent2)
    if(random.random() < mutProb):
        child = mutate_code(child)
    return child


def write_results(population): #output results format
    output = ""
    for x in range(1, len(population) + 1):
        output += str(x) + ". " + cities[int(population[x - 1])]
        output += '\n'
    output_file = open("Idan_Siman-Tov_GA_TS_Results.txt", 'w')
    output_file.write(output)
    output_file.close()


def populate(parents, pop_size, mut_prob):
    children = []
    numChildren = pop_size - len(parents)
    for x in range(0, numChildren):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        children.append(reproduce(parent1, parent2, mut_prob))
    return children


def populationRec(population, fitnesses, it_num, select_parent): 
    rec = ""
    rec += str(it_num) + ". " + "Population Size: " + str(len(population)) + " for iteration " + str(it_num) + '\n'
    rec += str(stats.mean(fitnesses)) + "\n"
    rec += str(stats.median(fitnesses)) + '\n'
    rec += str(stats.stdev(fitnesses)) + '\n'
    rec += str(select_parent) + '\n'
    return rec
    

def GA(pop_size, parent_select, cycle_off, fitness_off, mut_prob):
    rec = "" #empty string
    population = generate_rand_pop(pop_size, len(city_inds)) #start with a randomly generated pop
    fitnesses = get_fitness(population) #initialize the fitnesses
    it_num = 1 
    while(min(fitnesses) > fitness_off and it_num < cycle_off): 
        rec += populationRec(population, fitnesses, it_num, parent_select) 
        it_num +=1 
        parents = select_parents(population, fitnesses, parent_select) #parent_select is the numb of best individuals that are selected for reproduction
        children = populate(parents, pop_size, mut_prob) #generate children in order to create a new population of the same n to the original population
        population = parents + children 
        fitnesses = get_fitness(population) 
    results = population[fitnesses.index(min(fitnesses))]
    write_results(results) 
    output_file = open("Idan_Siman-Tov_GA_TS_Info.txt", 'w')
    output_file.write(rec)
    output_file.close()
    





if __name__ == '__main__':
    data = open_CSV()
    pop_size = 256 #popsize at each generation
    parent_select = int(pop_size/4) #numb of parents chosen for producing next generation
    mut_prob = 0.1 #prob that a child will mutate
    cycle_off = 1000 #max its for the program to run.
    fitness_off = 0 #min fitness value
    GA(pop_size, parent_select, cycle_off, fitness_off, mut_prob)
    