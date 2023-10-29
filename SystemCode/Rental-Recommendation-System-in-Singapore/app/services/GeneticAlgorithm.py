
from deap import base, creator, tools, algorithms
import random
from functools import partial
import multiprocessing

import numpy as np

def checkIndividual(individual, item_features, N,):
    items = [item for item, selected in zip(item_features['HouseID'], individual) if selected]
    return len(items) == N


def fix_individual(individual, item_features, N, id_to_index):
    # print("Original Individual:", individual)
    
    while sum(individual) > N:
        idx = random.choice([i for i, val in enumerate(individual) if val == 1])
        individual[idx] = 0
        # print("Removed 1 at position:", idx)
        
    while sum(individual) < N:
        idx = random.choice([i for i, val in enumerate(individual) if val == 0])
        individual[idx] = 1
        # print("Added 1 at position:", idx)
    
    selected_items = [item for item, selected in zip(item_features['HouseID'], individual) if selected]
    for item in selected_items:
        if item not in id_to_index:
            # print("Item not in id_to_index:", item)
            individual[item_features[item_features['HouseID'] == item].index[0]] = 0
            replacement = random.choice([i for i, val in enumerate(individual) if val == 0 and item_features['HouseID'].iloc[i] in id_to_index])
            individual[replacement] = 1
            # print("Replaced with item at position:", replacement)
    # print("Fixed Individual:", individual)
    return individual

def fix_and_evaluate(individual, item_features, n, id_to_index, toolbox):
    fixed_individual = fix_individual(individual, item_features, n, id_to_index)
    
    fitness = toolbox.evaluate(fixed_individual)
    
    fixed_individual.fitness.values = fitness
    
    return fixed_individual


def cxSet(ind1, ind2, n, item_features, toolbox, id_to_index):
    set1 = set([i for i, val in enumerate(ind1) if val == 1])
    set2 = set([i for i, val in enumerate(ind2) if val == 1])
    
    temp = set1.copy()
    set1 &= set2  
    set2 ^= temp  
    
    new_ind1 = [1 if i in set1 else 0 for i in range(len(ind1))]
    new_ind2 = [1 if i in set2 else 0 for i in range(len(ind2))]
    
    new_ind1 = creator.Individual(new_ind1)
    new_ind2 = creator.Individual(new_ind2)
    
    new_ind1 = fix_and_evaluate(new_ind1, item_features, n, id_to_index, toolbox)
    new_ind2 = fix_and_evaluate(new_ind2, item_features, n, id_to_index, toolbox)
    
    return new_ind1, new_ind2

def mutSet(individual,n,item_features,id_to_index, toolbox):
    """Mutation that ensures the number of 1's remains constant."""
    one_positions = [i for i, val in enumerate(individual) if val == 1]
    if one_positions:
        pos_to_zero = random.choice(one_positions)
        individual[pos_to_zero] = 0
    
    zero_positions = [i for i, val in enumerate(individual) if val == 0]
    if zero_positions:
        pos_to_one = random.choice(zero_positions)
        individual[pos_to_one] = 1
    fixed_individual = fix_and_evaluate(individual, item_features, n, id_to_index, toolbox)
    
    return fixed_individual,

def diversity(items, diversity_matrix,id_to_index):
    indices = [id_to_index[item] for item in items]
    selected_diversity = diversity_matrix[np.ix_(indices, indices)]
    diversity_score = selected_diversity[np.triu_indices(len(items), k=1)].mean()
    return diversity_score

def objective(items, item_features, epsilon,diversity_matrix,id_to_index):
    similarity_score = item_features.set_index('HouseID').loc[items]['weighted_similarity'].mean()
    diversity_score = diversity(items, diversity_matrix,id_to_index)
    weighted_score = (1 - epsilon) * similarity_score + epsilon * diversity_score
    return weighted_score 

def evalSolution(individual,item_features,N, epsilon,diversity_matrix,id_to_index):
    individual = np.array(individual)  
    selected_items = item_features['HouseID'][individual == 1].tolist()
    if len(selected_items) != N:
        return -np.inf,  
    missing_items = [item for item in selected_items if item not in id_to_index]
    # if missing_items:
    #     print("Missing items:", missing_items)
    if any(item not in id_to_index for item in selected_items):
        return -np.inf,
    return objective(selected_items, item_features, epsilon,diversity_matrix,id_to_index),

def initIndividual(item_features, N,individual_creator):
    items = random.sample(item_features['HouseID'].tolist(), N)
    individual = [1 if item in items else 0 for item in item_features['HouseID']]
    return individual_creator(individual)

def genetic_algorithm(item_features, epsilon, N,diversity_matrix,id_to_index):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("individual", initIndividual, item_features=item_features, N=N,individual_creator=creator.Individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    with multiprocessing.Pool() as pool:
        toolbox.register("map", pool.map)
        toolbox.register("evaluate", partial(evalSolution, item_features=item_features, N=N, epsilon=epsilon,diversity_matrix=diversity_matrix,id_to_index=id_to_index))
        toolbox.register("mate", cxSet, n=N,item_features=item_features,toolbox=toolbox,id_to_index=id_to_index)
        toolbox.register("mutate", mutSet, n=N,item_features=item_features,id_to_index=id_to_index,toolbox=toolbox)
        toolbox.register("select", tools.selTournament, tournsize=3)
        
        population = toolbox.population(n=5)
        algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.2, ngen=50, verbose=False)
    
    top1 = tools.selBest(population, 1)[0]
    # print("Top 1 Individual:", top1)
    # print("Number of 1s in Top 1:", sum(top1))
    selected_indices = [i for i, val in enumerate(top1) if val == 1]
    selected_items = item_features.loc[selected_indices, 'HouseID'].tolist()

    # print("Selected Items:", selected_items)
    return selected_items, top1.fitness.values[0]