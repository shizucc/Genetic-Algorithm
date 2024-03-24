import random;

def generateChromosome(size):
    p = 0.5
    return [1 if round(random.uniform(0,1),4) > p else 0 for _ in range(size)]

def generatePopulation(populationSize, genSize):
    population = []
    for _ in range(populationSize):
        individual = generateChromosome(genSize)
        population.append(individual)
    return population

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

def fitnessEvaluation(population):
    for individual in population:
        fitnessValue = fitnessFunction(individual)
        print(f"{individual}, fitness : {fitnessValue}")

# Objective function

    
def main():
    chromosomeSize = 5
    populationSize = 5 
    population = generatePopulation(populationSize,chromosomeSize)

    print(type(population))
    # fitnessEvaluation(population)
     
main()




