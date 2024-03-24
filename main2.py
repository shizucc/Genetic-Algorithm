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
    decimalValue = calculateDecimalValue(individual)
    return decimalValue

def main():
    for _ in range(1,51):
        myChromosomeX1 = []
        myChromosomeX2 = []
        while True:
            c = generateChromosome(5)
            x = fitnessFunction(c)
            if(x >= 3 and x <=10):
                myChromosomeX1 = c
                break
        while True:
            c = generateChromosome(5)
            x = fitnessFunction(c)
            if(x >= 3 and x <=10):
                myChromosomeX2 = c
                break
    
    
        finalChromosome = myChromosomeX1 + myChromosomeX2
        print(finalChromosome)

main()