from tabulate import tabulate
import random
def generatePopulation(populationSize, genSize):
    population = []
    for _ in range(populationSize):
        individual = generateChromosome(genSize)
        population.append(individual)
    return population

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
    

def generatePopulation2(populationSize, intervalMin, intervalMax):
    population = []
    for _ in range(1,populationSize+1):
        myChromosomeX1 = []
        myChromosomeX2 = []
        while True:
            c = generateChromosome(5)
            x = calculateDecimalValue(c)
            if(x >= intervalMin and x <= intervalMax):
                myChromosomeX1 = c
                break
        while True:
            c = generateChromosome(5)
            x = calculateDecimalValue(c)
            if(x >= intervalMin and x <= intervalMax):
                myChromosomeX2 = c
                break
    
    
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

    
def main():
    myPopulation = generatePopulation2(50, 3, 10)
    fitnesses = []
    
    for individual in myPopulation:
        fitness = fitnessFunction(individual)
        fitnesses.append(fitness)
    
    head = ["Chromosome", "Fitness"]

    plotTableDump = list(zip(myPopulation,fitnesses))
    result = [list(item) for item in plotTableDump]

    # print(tabulate(result, headers=head, tablefmt="grid"))

    # Rank Selection
    choices = selection(myPopulation)
    [choice1, choice2] = choices
    
    
    
    

main()