from tabulate import tabulate
import numpy as np
import random
import copy
import matplotlib.pyplot as plt


def generateChromosome(size):
    p = 0.5
    return [1 if round(random.uniform(0,1),4) > p else 0 for _ in range(size)]

def calculateDecimalValue(individual):
    binaryString = ''.join(map(str,individual))
    
    decimalValue = 0
    for i in range(len(binaryString)):
        digit = int(binaryString[len(binaryString) - 1 - i])
        decimalValue += digit * (2**i)
    return decimalValue

def fitnessFunction(individual):
    individualMedian= int(len(individual) /2)
    myArr1 = individual[:individualMedian]
    myArr2 = individual[individualMedian:]
    
    myArr1Decimal = calculateDecimalValue(myArr1)
    myArr2Decimal = calculateDecimalValue(myArr2)

    fitness = 3 * myArr1Decimal - 2 * myArr2Decimal
    return(fitness)
    

def generatePopulation(populationSize, intervalMin, intervalMax):
    population = []
    for _ in range(1,populationSize+1):
        myChromosomeX1 = generateChromosome(5)
        myChromosomeX2 = generateChromosome(5)
        # while True:
        #     c = generateChromosome(5)
        #     x = calculateDecimalValue(c)
        #     if(x >= intervalMin and x <= intervalMax):
        #         myChromosomeX1 = c
        #         break
        # while True:
        #     c = generateChromosome(5)
        #     x = calculateDecimalValue(c)
        #     if(x >= intervalMin and x <= intervalMax):
        #         myChromosomeX2 = c
        #         break
    
    
        finalChromosome = myChromosomeX1 + myChromosomeX2
        population.append(finalChromosome)
    return population

def selection(population):
    populationLen =  len(population)
    fitnesses = []
    for individual in population:
        fitness = fitnessFunction(individual)
        fitnesses.append(fitness)
    percentages = []
    # Get Ranking

    sortedIndices = sorted(range(len(fitnesses)), key=lambda k: fitnesses[k])


    rankArray = [0] * len(fitnesses)
    for i, idx in enumerate(sortedIndices):
        rankArray[idx] = i + 1

    if 0 in rankArray:
        minRank = min(rankArray)
        rankArray = [rank - minRank + 1 for rank in rankArray]



    # Count Percentage
    for rank in rankArray:
        percentage = rank/(populationLen * (populationLen +1) /2)
        percentages.append(percentage)


    choice1 = random.uniform(0, 1)
    choice2 = random.uniform(0, 1)

    index1 = None
    index2 = None

    # Roulette wheel selection
    currentTotal = 0
    for idx, nilai in enumerate(percentages):
        currentTotal += nilai
        if currentTotal >= choice1 and index1 is None:
            index1 = idx
        if currentTotal >= choice2 and index2 is None:
            index2 = idx
        if index1 is not None and index2 is not None:
            break

    return [index1,index2]

def crossover(parent1,parent2):
    mask = generatePopulation(1,3,4)[0]
    
    child1 = []
    child2 = []

    for i in range(len(parent1)):
        if mask[i] == 0:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    
    return [child1, child2]

def mutation(individual, rate):
    mutatedChromosome = individual.copy()
    for i in range(len(mutatedChromosome)):
        if np.random.rand() < rate:
            # Pilih gen yang akan dimutasi
            gene_to_move = mutatedChromosome[i]
            # Hapus gen tersebut dari posisi asalnya
            del mutatedChromosome[i]
            # Pilih posisi baru untuk memasukkan gen
            new_index = np.random.randint(0, len(mutatedChromosome))
            # Masukkan gen ke posisi baru
            mutatedChromosome.insert(new_index, gene_to_move)
    return mutatedChromosome

def evaluation(population, intervalMin, intervalMax):
    filteredPopulation = []

    for individual in population:
        individualMedian= int(len(individual) /2)
        myArr1 = individual[:individualMedian]
        myArr2 = individual[individualMedian:]
        
        myArr1Decimal = calculateDecimalValue(myArr1)
        myArr2Decimal = calculateDecimalValue(myArr2)

        if((myArr1Decimal >= intervalMin and myArr1Decimal <= intervalMax) and (myArr2Decimal >= intervalMin and myArr2Decimal <= intervalMax)):
            filteredPopulation.append(individual)
    return filteredPopulation

def cycle(initPopulation):
    currentPopulation = []
    population = initPopulation.copy()

    while len(population) > 0:
        choices = selection(population)
        [choice1, choice2] = choices
        parent1 = population[choice1]
        parent2 = population[choice2]

        [child1, child2 ] =crossover(parent1,parent2)
        mutated1 = mutation(child1,0.01)
        mutated2 = mutation(child2,0.01)

        currentPopulation.append(mutated1)
        currentPopulation.append(mutated2)
        indices = sorted([choice1,choice2], reverse=True)
        for index in indices:
            try:
                del population[index]
            except:
                pass        
        
    return evaluation(currentPopulation,3,10)

def GENETIC_ALGORITHM(initPopulation, generation):
    population = initPopulation.copy()

    history = [{
        "generation" : 1,
        "population" : population,
        "fitnesses" : [0]
    }]
    
    for currentGenerationIndex in range(generation-1):
        newGen = cycle(history[currentGenerationIndex]["population"])

        fitnesses = []
        for individual in newGen:
            fitness = fitnessFunction(individual)
            fitnesses.append(fitness)

        newHistory = {
            "generation" : history[currentGenerationIndex]["generation"]+1,
            "population" : copy.deepcopy(newGen),
            "fitnesses" : fitnesses
        }
        history.append(newHistory)
    return history



def main():
    initPopulation = generatePopulation(50, 3, 10)
    fitnesses = []
    
    for individual in initPopulation:
        fitness = fitnessFunction(individual)
        fitnesses.append(fitness)
    
    head = ["Chromosome", "Fitness"]

    plotTableDump = list(zip(initPopulation,fitnesses))
    result = [list(item) for item in plotTableDump]

    # print(tabulate(result, headers=head, tablefmt="grid"))

    res = GENETIC_ALGORITHM(initPopulation,30)

    generationList = [element["generation"] for element in res]
    # fitnessList = [ (sum(element["fitnesses"]) / len(element["fitnesses"])) for element in res ]
    # fitnessList = [ (max(element["fitnesses"]) for element in res ) ]
    fitnessList =[element["fitnesses"] for element in res]
    maxFitnessList = [max(sublist) for sublist in fitnessList]
    plt.plot(generationList, maxFitnessList)
    plt.xlabel("Generasi")
    plt.ylabel("Fitness")

    plt.show()

    
main()