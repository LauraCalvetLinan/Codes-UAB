import random
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. PROBLEM DATA SETUP
# ==========================================
NUM_FLIGHTS = 25
NUM_GATES = 8
random.seed(42)

# Flight time windows (arrival, departure in minutes from 0 to 120)
flight_times = [(random.randint(0, 70), random.randint(80, 120)) for _ in range(NUM_FLIGHTS)]
# Flight priority (higher means more connecting passengers)
flight_priority = [random.randint(1, 10) for _ in range(NUM_FLIGHTS)]
# Gate quality score (10 = central hub gate, 1 = distant remote apron)
gate_quality = [random.randint(1, 10) for _ in range(NUM_GATES)]

def fitness_function(chromosome):
    """
    Maximizes Gate Quality x Flight Priority
    Penalizes overlapping flight schedules at the same gate.
    """
    total_score = 0
    gate_schedules = {g: [] for g in range(NUM_GATES)}
    
    # Calculate Gate Quality Score
    for flight_idx, gate_idx in enumerate(chromosome):
        total_score += flight_priority[flight_idx] * gate_quality[gate_idx]
        gate_schedules[gate_idx].append(flight_times[flight_idx])
        
    # Overlap Penalty Calculation
    overlap_penalty = 0
    for g in range(NUM_GATES):
        times = sorted(gate_schedules[g], key=lambda x: x[0])
        for i in range(len(times) - 1):
            if times[i][1] > times[i+1][0]: # Overlap detected
                overlap_penalty += 150 # Heavy operational penalty
                
    return max(1, total_score - overlap_penalty)

# ==========================================
# 2. GA OPERATORS
# ==========================================
def init_population(pop_size, mode="random"):
    if mode == "random":
        return [[random.randint(0, NUM_GATES - 1) for _ in range(NUM_FLIGHTS)] for _ in range(pop_size)]
    elif mode == "heuristic":
        # Heuristic seed: Assign highest priority flights to highest quality gates
        best_gates = sorted(range(NUM_GATES), key=lambda g: gate_quality[g], reverse=True)
        pop = []
        for _ in range(pop_size):
            chrom = [random.choice(best_gates[:3]) if flight_priority[f] > 6 
                     else random.randint(0, NUM_GATES - 1) for f in range(NUM_FLIGHTS)]
            pop.append(chrom)
        return pop

def crossover(parent1, parent2, mode="one_point"):
    if mode == "one_point":
        pt = random.randint(1, NUM_FLIGHTS - 1)
        return parent1[:pt] + parent2[pt:], parent2[:pt] + parent1[pt:]
    elif mode == "uniform":
        c1, c2 = [], []
        for i in range(NUM_FLIGHTS):
            if random.random() < 0.5:
                c1.append(parent1[i]); c2.append(parent2[i])
            else:
                c1.append(parent2[i]); c2.append(parent1[i])
        return c1, c2

def mutate(chromosome, p_mut=0.05, mode="random_reset"):
    mutated = list(chromosome)
    for i in range(NUM_FLIGHTS):
        if random.random() < p_mut:
            if mode == "random_reset":
                mutated[i] = random.randint(0, NUM_GATES - 1)
            elif mode == "swap":
                j = random.randint(0, NUM_FLIGHTS - 1)
                mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated

# ==========================================
# 3. GA MAIN ENGINE WITH METRICS TRACKING
# ==========================================
def run_ga(pop_size=50, generations=100, p_cross=0.8, p_mut=0.05, 
           init_mode="random", cross_mode="one_point", mut_mode="random_reset"):
    
    pop = init_population(pop_size, mode=init_mode)
    best_history, avg_history = [], []
    
    for gen in range(generations):
        fitnesses = [fitness_function(ind) for ind in pop]
        
        best_history.append(np.max(fitnesses))
        avg_history.append(np.mean(fitnesses))
        
        # Tournament Selection
        selected = []
        for _ in range(pop_size):
            i1, i2 = random.randint(0, pop_size-1), random.randint(0, pop_size-1)
            selected.append(pop[i1] if fitnesses[i1] > fitnesses[i2] else pop[i2])
            
        # Crossover & Mutation
        next_gen = []
        for i in range(0, pop_size, 2):
            p1, p2 = selected[i], selected[i+1]
            if random.random() < p_cross:
                c1, c2 = crossover(p1, p2, mode=cross_mode)
            else:
                c1, c2 = list(p1), list(p2)
            next_gen.append(mutate(c1, p_mut, mode=mut_mode))
            next_gen.append(mutate(c2, p_mut, mode=mut_mode))
            
        pop = next_gen[:pop_size]
        
    return best_history, avg_history
