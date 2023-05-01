from .Individual import Individual
from .Node import Node

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-StdGP
#
# Copyright ©2019-2022 J. E. Batista
#

def double_tournament(rng, population, Sf, Sp, Switch=False):
	"""
	Selects "n" Individuals from the population and returns a single Individual
	using double tournament selection based on fitness and parsimony.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	Sf (int): The fitness tournament size.
	Sp (int): The parsimony tournament size.
	Switch (bool): If True, qualifiers select on size and the final selects on fitness;
			     If False, qualifiers select on fitness and the final selects on size.
	"""

	def select_by_fitness(population, n):
		candidates = [rng.randint(0, len(population) - 1) for i in range(n)]
		return population[min(candidates)]

	def select_by_size(population, n):
		candidates = [rng.randint(0, len(population) - 1) for i in range(n)]
		return min(candidates, key=lambda x: len(population[x].genome))

	if Switch:
		# Size -> Fitness
		first_round_winners = [select_by_size(population, Sf) for _ in range(Sp)]
		return select_by_fitness(first_round_winners, Sp)
	else:
		# Fitness -> Size
		first_round_winners = [select_by_fitness(population, Sf) for _ in range(Sp)]
		return select_by_size(first_round_winners, Sp)



def tournament(rng, population,n):
	'''
	Selects "n" Individuals from the population and return a 
	single Individual.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	candidates = [rng.randint(0,len(population)-1) for i in range(n)]
	return population[min(candidates)]


def getElite(population,n):
	'''
	Returns the "n" best Individuals in the population.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	return population[:n]


# Modify the getOffspring function to use the double_tournament method
def getOffspring(rng, population, Sf, Sp, do_fitness_first=False):
	parent1 = double_tournament(rng, population, Sf, Sp, do_fitness_first)
	parent2 = double_tournament(rng, population, Sf, Sp, do_fitness_first)

	offspring1 = parent1.crossover(parent2, rng)
	offspring1.mutate(rng)

	offspring2 = parent2.crossover(parent1, rng)
	offspring2.mutate(rng)

	return [offspring1, offspring2]


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
	return ret
