from .Individual import Individual
from .Node import Node

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-StdGP
#
# Copyright ©2019-2022 J. E. Batista
#

def double_tournament(rng, population, Sf, Sp, switch=False, custom_fitness=None):
	if switch:
		size_tournament_winners = tournament(rng, population, Sf, custom_fitness)
		fitness_tournament_winners = [size_tournament_winners[i] for i in rng.sample(range(Sf), Sp)]
		return tournament(rng, fitness_tournament_winners, Sp)
	else:
		fitness_tournament_winners = tournament(rng, population, Sf, custom_fitness)
		size_tournament_winners = [fitness_tournament_winners[i] for i in rng.sample(range(Sf), Sp)]
		return tournament(rng, size_tournament_winners, Sp, custom_fitness)

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


def getOffspring(rng, population, tournament_size):
	'''
	Genetic Operator: Selects a genetic operator and returns a list with the 
	offspring Individuals. The crossover GOs return two Individuals and the
	mutation GO returns one individual. Individuals over the LIMIT_DEPTH are 
	then excluded, making it possible for this method to return an empty list.
	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	isCross = rng.random()<0.5

	desc = None

	if isCross:
		desc = STXO(rng, population, tournament_size)
	else:
		desc = STMUT(rng, population, tournament_size)

	return desc


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
