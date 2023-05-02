from .Individual import Individual
from .Node import Node
import random


# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-StdGP
#
# Copyright ©2019-2022 J. E. Batista
#

def double_tournament(rng, population, Sf, Sp, tournament_size ,switch=False, custom_fitness=None):
    def parsimony_tournament(tournament_size):
        selected = random.sample(population, tournament_size)
        return min(selected, key=lambda x: x.size)
    
    fittest = []
    smallest = []
    if not switch:
        for _ in range(Sf):
            best = tournament(rng, population, tournament_size, custom_fitness=None)
            fittest.append(best)
        
        smallest = random.sample(fittest, Sp)
        for _ in range(Sp):
            best = parsimony_tournament(tournament_size)
            smallest.append(best)
        
        return smallest[-1]  # Return the best individual from the last parsimony tournament run
    
    else:
        for _ in range(Sp):
            best = parsimony_tournament(tournament_size)
            smallest.append(best)
        
        fittest = random.sample(smallest, Sf)
        for _ in range(Sf):
            best = tournament(rng, population, tournament_size, custom_fitness=None)
            fittest.append(best)
        
        return fittest[-1]  # Return the best individual from the last fitness tournament run




'''def double_tournament(rng, population, Sf, Sp, switch=False, , custom_fitness=None):
	def parsonomy_tournament(tournament_size):
		selected = random.sample(population, tournament_size)
		return min(selected, key=lambda x: x.size)
	
	fittest=[]
	smallest=[]
	if not switch:
		for i in Sf:
			best=tournament(rng, population, tournament_size, custom_fitness=None)
			fittest.append(best)
		choice (fittest, Sp)
		smallest.append(parsonomy_tournament(Sp))
		return smallest
	
	else:
		for i in Sp:
			best=tournament(parsonomy_tournament(tournament_size))
			smallest.append(best)
		choice (fittest, Sf)
		fittest.append(tournament(rng, population, tournament_size, custom_fitness=None))
		return fittest'''



'''def double_tournament(population, Sf, Sp, switch=False):
	def first_tournament(tournament_size):
		selected = random.sample(population, tournament_size)
		return max(selected, key=lambda x: x.fitness)

	def second_tournament(tournament_size):
		selected = random.sample(population, tournament_size)
		return min(selected, key=lambda x: x.size)

	winners = [first_tournament(Sf) for _ in range(Sf)]

	if switch:
		Sp, Sf = Sf, Sp

	selected = random.sample(winners, Sp)
	return [second_tournament(Sp) for _ in selected]'''



def tournament(rng, population, tournament_size, custom_fitness=None):
	best = None
	for _ in range(tournament_size):
		competitor = rng.choice(population)
		if custom_fitness:
			competitor_fitness = custom_fitness(competitor)
		else:
			competitor_fitness = competitor.getFitness()
		if best is None or competitor_fitness > best[1]:
			best = (competitor, competitor_fitness)
	return best[0]



def getElite(population,n):
	'''
	Returns the "n" best Individuals in the population.
	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	return population[:n]


def getOffspring(rng, population, tournament_size, double_tournament=False, Sf=7, Sp=3, switch=False):
	'''
	Genetic Operator: Selects a genetic operator and returns a list with the 
	offspring Individuals. The crossover GOs return two Individuals and the
	mutation GO returns one individual. Individuals over the LIMIT_DEPTH are 
	then excluded, making it possible for this method to return an empty list.
	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''

	if double_tournament:
		parent1 = double_tournament(rng, population, Sf, Sp, switch, custom_fitness=accuracy)
		parent2 = double_tournament(rng, population, Sf, Sp, switch, custom_fitness=accuracy)
	else:
		parent1 = tournament(rng, population, tournament_size)
		parent2 = tournament(rng, population, tournament_size)
    
	isCross = rng.random() < 0.5

	if isCross:
		return STXO(rng, parent1, parent2)
	else:
		return STMUT(rng, parent1)


def discardDeep(population, limit):
	ret = []
	for ind in population:
		if ind.getDepth() <= limit:
			ret.append(ind)
	return ret


def STXO(rng, population, tournament_size):
	'''
	Randomly selects one node from each of two individuals; swaps the node and
	sub-nodes; and returns the two new Individuals as the offspring.
	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(rng, population, tournament_size)
	ind2 = tournament(rng, population, tournament_size)

	h1 = ind1.getHead()
	h2 = ind2.getHead()

	n1 = h1.getRandomNode(rng)
	n2 = h2.getRandomNode(rng)

	n1.swap(n2)

	ret = []
	for h in [h1,h2]:
		i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
		i.copy(h)
		ret.append(i)
	return ret


def STMUT(rng, population, tournament_size):
	'''
	Randomly selects one node from a single individual; swaps the node with a 
	new, node generated using Grow; and returns the new Individual as the offspring.
	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(rng, population, tournament_size)
	h1 = ind1.getHead()
	n1 = h1.getRandomNode(rng)
	n = Node()
	n.create(rng, ind1.operators, ind1.terminals, ind1.max_depth)
	n1.swap(n)


	ret = []
	i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
	i.copy(h1)
	ret.append(i)
	return 
