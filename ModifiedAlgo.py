
import random
from random import randint
from com.Classes.Room import Room
from Professor import Professor

POPULATION_SIZE = 100
GENES = []
ROOMS = []
SAMEPROFESSORS = []
LABS = []
arrayofTime = ["Mon-08:30-11:30", "Mon-11:45-02:45", "Mon-3:00-06:00", "Tue-08:30-11:30", "Tue-11:45-02:45",
               "Tue-3:00-06:00", "Wed-08:30-11:30", "Wed-11:45-02:45", "Wed-3:00-06:00", "Thurs-08:30-11:30",
               "Thurs-11:45-02:45", "Thurs-3:00-06:00", "Sat-08:30-11:30", "Sat-11:45-02:45", "Sat-3:00-06:00",
               "Sun-08:30-11:30", "Sun-11:45-02:45", "Sun-3:00-06:00"]


class Individual(object):

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calcFitness()

    @classmethod
    def create_gnome(self):
        '''
        create chromosome or string of genes
        '''
        global GENES

        gnome_len = len(GENES)
        # print("LENGth", gnome_len)
        gene = GENES
        return [self.mutated_genes(gene[i]) for i in range(gnome_len)]

    @classmethod
    def mutated_genes(self, Gene):
        '''
        create random genes for mutation
        '''
        global arrayofTime
        global ROOMS
        global SAMEPROFESSORS
        global LABS
        # gene = random.choice(arrayofTime) ,"Available_TimeSlots":[]

        newgene = Gene
        # newgene["Available_TimeSlots"] =

        if len(newgene["Available_TimeSlots"]) == 0:
            for time in arrayofTime:
                # print('time', time)
                if time in newgene["Professor"].availability:
                    # Gene["Assigned-timeSlot"] = time
                    newgene["Available_TimeSlots"].append(time)

        newtime = random.choice(newgene["Available_TimeSlots"])

        # print('newtime', newtime)
        if newgene["isLab"] == True:
            newgene["roomAlotted"] = random.choice(LABS)
        else:
            newgene["roomAlotted"] = random.choice(ROOMS)

        newgene["Assigned-timeSlot"] = newtime
        newgene["Professor"].courses.append(newgene["Name"])
        # txt = newgene["Professor"].name+"-"+newtime[0:3]
        # if txt in SAMEPROFESSORS:
        #     newgene["Professor"].sameDayCount = 1
        # else:
        #     SAMEPROFESSORS.append(txt)
        # newGENE = Gene
        # print('Gene->>>>>>', newgene)

        return newgene

    def calcFitness(self):
        clashMsg = ""
        alreadyCounted = []
        countedIndex = []
        fitness = 0
        ifFound = False
        
        for i in range(0, len(self.chromosome), +1):
            
            if i in countedIndex:
                continue
            countedIndex.append(i)
            if self.chromosome[i]["Assigned-timeSlot"] in self.chromosome[i]["Professor"].availability:
                for ch in range(0, len(self.chromosome), +1):
                    if ch not in countedIndex:
                        
                        if self.chromosome[i]["Assigned-timeSlot"] == self.chromosome[ch]["Assigned-timeSlot"] and self.chromosome[ch]["roomAlotted"].room == self.chromosome[i]["roomAlotted"].room:
                            
                            ifFound = True
                            fitness += 1
                            countedIndex.append(ch)

                        if self.chromosome[i]["Professor"].name == self.chromosome[ch]["Professor"].name:
                            if self.chromosome[i]["Assigned-timeSlot"] == self.chromosome[ch]["Assigned-timeSlot"]:
                                
                                fitness += 1
                                countedIndex.append(ch)
                    else:
                        continue
            # else:
               
            
            if self.chromosome[i]["Professor"].name not in alreadyCounted:
                if len(self.chromosome[i]["Professor"].courses) > 2:
                    fitness += 1
            
            if self.chromosome[i]["roomAlotted"].capacity < self.chromosome[i]["Capacity"]:
                clashMsg = "CAPACITY ISSUE"
                ifFound = True
                fitness += 1

            if self.chromosome[i]["isLab"] == False:
                if self.chromosome[i]["roomAlotted"].isLab == True:
                    clashMsg = "LAB Issue"
                    ifFound = True
                    fitness += 1

        return fitness

    def crossover(self, p2):
        child = []
        isOdd = False
        num = len(p2.chromosome) // 2
        # print('Before CrossOver', p2.chromosome)
        # print('Total', num)
        if num % 2 != 0:
            num = len(p2.chromosome) - 1 // 2
            isOdd = True
        # num = num//2
        # print(num)
        randomNum = randint(0, num)
        sub = len(p2.chromosome) - randomNum
        # child.extend(self.chromosome[:randomNum])
        for i in range(0, num - 1, +1):
            # print(p2.chromosome[i]['Assigned-timeSlot'])
            child.append(p2.chromosome[i])
        for j in range(num - 1, len(p2.chromosome), +1):
            # print(self.chromosome[j]['Assigned-timeSlot'])
            child.append(self.chromosome[j])
        newchild = self.mutation(child)
        # print('After CrossOver', child)

        # print('Child Len', len(child))
        return Individual(newchild)

    def mutation(self, chromosome):
        mutatedChromosome = chromosome
        alreadyCounted = []
        countedIndex = []
        global ROOMS
        for gene in range(0, len(mutatedChromosome), +1):
            countedIndex.append(gene)
            for nextGene in range(0, len(mutatedChromosome), +1):
                
                if nextGene not in countedIndex:
                    if mutatedChromosome[gene]["Assigned-timeSlot"] == mutatedChromosome[nextGene]["Assigned-timeSlot"]:

                        if mutatedChromosome[gene]["roomAlotted"].room == mutatedChromosome[nextGene][
                            "roomAlotted"].room:
                            if len(mutatedChromosome[gene]["Available_TimeSlots"]) > 1:
                                mutatedChromosome[gene]["Assigned-timeSlot"] = random.choice(mutatedChromosome[gene]["Available_TimeSlots"])
                                countedIndex.append(nextGene)
                                
                            elif len(mutatedChromosome[nextGene]["Available_TimeSlots"]) > 1:
                                mutatedChromosome[nextGene]["Assigned-timeSlot"] = random.choice(mutatedChromosome[nextGene]["Available_TimeSlots"])
                                countedIndex.append(nextGene)
                                
            # if mutatedChromosome[gene]["Professor"].sameDayCount>2:

                if mutatedChromosome[gene]["Assigned-timeSlot"] == mutatedChromosome[nextGene]["Assigned-timeSlot"]:
                    if mutatedChromosome[gene]["Professor"].name == mutatedChromosome[nextGene]["Professor"].name:
                        mutatedChromosome[nextGene]["Assigned-timeSlot"] = random.choice(mutatedChromosome[nextGene]["Available_TimeSlots"])
                        countedIndex.append(nextGene)
               
            if mutatedChromosome[gene]["Professor"].name not in alreadyCounted:
                alreadyCounted.append(mutatedChromosome[gene]["Professor"].name)
            else:
                mutatedChromosome[gene]["Assigned-timeSlot"] = random.choice(mutatedChromosome[gene]["Available_TimeSlots"])

            if mutatedChromosome[gene]["isLab"] == False:
                if mutatedChromosome[gene]["roomAlotted"].isLab == True:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(ROOMS)

            if mutatedChromosome[gene]["isLab"] == True:
                if mutatedChromosome[gene]["roomAlotted"].isLab == False:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(LABS)
            if mutatedChromosome[gene]["roomAlotted"].capacity < mutatedChromosome[gene]["Capacity"]:
                if mutatedChromosome[gene]["isLab"] == True:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(LABS)
                else:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(ROOMS)

        return mutatedChromosome


def main():
    global POPULATION_SIZE
    global arrayofTime
    global GENES
    global LABS
    global ROOMS
    prevFitness = 10
    fitness_Same_Count = 0
    ifFound = False
    population = []
    # current generation
    generation = 1
    rooms = [
        Room("CS-101", 70, False),
        Room("CS-102", 70, False),
        Room("CS-103", 70, False),
        Room("Lab-1", 70, True),
        Room("CS-104", 70, False),
        Room("CS-105", 70, False),
        Room("Lab-2", 70, True),
        Room("CS-106", 70, False)
        
    ]
    
    for r in rooms:
        if r.isLab == True:
            LABS.append(r)
        else:
            ROOMS.append(r)
    Prof1 = Professor("Shoaib", arrayofTime,"",0,[])
    Prof2 = Professor("adnan",arrayofTime,"",0,[])
    Prof3 = Professor("mirza",[arrayofTime[3], arrayofTime[7], arrayofTime[9], arrayofTime[11], arrayofTime[7]],"",0,[])
    Prof4 = Professor("Ali",[arrayofTime[0], arrayofTime[1], arrayofTime[10], arrayofTime[11]],"",0,[])
    Prof5 = Professor("faiq",[arrayofTime[0], arrayofTime[1], arrayofTime[2]],"",0,[])
    Prof6 = Professor("Jamal",arrayofTime,"",0,[])
    Prof7 = Professor("Noman",[arrayofTime[1], arrayofTime[2], arrayofTime[3], arrayofTime[4], arrayofTime[14]],"",0,[])
    Prof8 = Professor("Adeel",arrayofTime,"",0,[])
    Prof9 = Professor("shahzain", [arrayofTime[0], arrayofTime[1], arrayofTime[2], arrayofTime[3], arrayofTime[4],
                                arrayofTime[5], arrayofTime[6]],"",0,[])
    Prof10 = Professor("saim",[arrayofTime[0], arrayofTime[1], arrayofTime[2], arrayofTime[13]],"",0,[])
    Prof11 = Professor("areeb",[arrayofTime[3], arrayofTime[7], arrayofTime[9], arrayofTime[11], arrayofTime[7]],"",0,[])
    Prof12 = Professor("billal",[arrayofTime[1], arrayofTime[2]],"",0,[])
    Prof13 = Professor("irfan",[arrayofTime[0], arrayofTime[1], arrayofTime[10], arrayofTime[11]],"",0,[])
    Prof14 = Professor("ismael",[arrayofTime[0], arrayofTime[1], arrayofTime[2]],"",0,[])
    Prof15 = Professor("aarif",arrayofTime,"",0,[])
    Prof16 = Professor("faris",[arrayofTime[1], arrayofTime[2], arrayofTime[3], arrayofTime[4], arrayofTime[14]],"",0,[])

    course1 = {"Name": "MAD","Professor": Prof1,
               "Capacity": 55, "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "",
               "roomAlotted": None, "isLab": True}
    course2 = {"Name": "Probability", "Professor": Prof2,"Capacity": 50,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course3 = {"Name": "AI LAB", "Professor":Prof3,
               "Capacity": 30,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": True}
    course4 = {"Name": "Multi", "Professor": Prof2, "Capacity": 50,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course5 = {"Name": "POM", "Professor": Prof4,
               "Capacity": 50,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course6 = {"Name": "AI", "Professor": Prof5,
               "Capacity": 30, "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "",
               "roomAlotted": None, "isLab": True}
    course7 = {"Name": "CAO", "Professor": Prof6, "Capacity": 60,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course8 = {"Name": "DCL", "Professor": Prof7,"Capacity": 50,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course9 = {"Name": "FYP", "Professor": Prof8, "Capacity": 60,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course10 = {"Name": "Calculus", "Professor": Prof8, "Capacity": 60,
                "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None,
                "isLab": False}
    course11 = {"Name": "MAD","Professor": Prof9,
               "Capacity": 55, "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "",
               "roomAlotted": None, "isLab": True}
    course12 = {"Name": "Probability", "Professor": Prof10,"Capacity": 50,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course13 = {"Name": "AI LAB", "Professor": Prof11,
               "Capacity": 30,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": True}
    course14 = {"Name": "Multi", "Professor": Prof12, "Capacity": 50,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course15 = {"Name": "POM", "Professor": Prof13,
               "Capacity": 50,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course16 = {"Name": "AI", "Professor": Prof14,
               "Capacity": 30, "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "",
               "roomAlotted": None, "isLab": True}
    course17 = {"Name": "CAO", "Professor": Prof15, "Capacity": 60,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    course18 = {"Name": "DCL", "Professor": Prof16,"Capacity": 50,
               "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "", "roomAlotted": None, "isLab": False}
    
 
            
    
    courses = [course1, course2, course3, course4, course5, course6, course7, course8, course9,course10,course11, course12, course13, course14, course15, course16, course17, course18]
    GENES = courses

    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        # print('GNOME',gnome)
        population.append(Individual(gnome))

        print('Fitness-----', Individual(gnome).fitness)

    # Population Created
    while not ifFound:
        # sort the population in increasing order of fitness score
        population = sorted(population, key=lambda x: x.fitness)
        print('Fitness After-----', population[0].fitness)

        prevFitness = population[0].fitness
        if population[0].fitness <= 0:
            ifFound = True
            # print('SELECTED GENERATION')
            # for i in population[0].chromosome:
            #     print('', i['Name'], i['Assigned-timeSlot'] )
            break
        elif population[0].fitness == prevFitness:
            fitness_Same_Count += 1
            if fitness_Same_Count > 40:
                ifFound = True
                break

        new_generation = []
        s = int((10 * POPULATION_SIZE) // 100)
        for ch in range(0, s, +1):
            ind = Individual(population[ch].mutation(population[ch].chromosome))
            new_generation.append(ind)

        ns = int((90 * POPULATION_SIZE) // 100)
        # print(ns)
        # sub = ns - s
        for _ in range(ns):
            rand = randint(s, ns - 1)
            parent1 = population[rand]
            rand = randint(s, ns - 1)
            parent2 = population[rand]

            child = parent1.crossover(parent2)
            new_generation.append(child)

        population = new_generation
        # print('new', population[0].chromosome)
        # print('Generation: ', generation)
        # print('Population: ', population[0].chromosome)
        # print('Fitness: ', population[0].fitness)

        # print("Generation: {}\tDict: {}\tFitness: {}".format(generation, "".join(population[0].chromosome),population[0].fitness))

        generation += 1

    print('SELECTED GENERATION ')
    for ch in population[0].chromosome:
        print('Name : ', ch["Name"])
        print('Professor : ', ch["Professor"].name)
        print('TimeSlot : ', ch["Assigned-timeSlot"])
        print('Room : ', ch["roomAlotted"].room)
        print('\n')
    # print('SELECTED CHROMOSOME LENGTH  ', len(population[0].chromosome))


if __name__ == "__main__":
    main()