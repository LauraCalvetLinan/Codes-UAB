# ==========================================
# As a hub cargo dispatcher for an air express carrier, you must choose which high-priority air shipments to load onto a regional freighter flight. 
# The aircraft has a maximum structural payload weight capacity ($W_{max}$). Each potential shipment $i$ has a verified weight $w_i$ (kg) and an associated revenue $v_i$ ($).
# Your goal is to maximize total flight revenue without exceeding $W_{max}$.
# You will test and compare three algorithmic paradigms across problem sizes $N \in [10, 12, 14, 16, 18, 20, 22, 24]$:
# - Exact Method (Brute-Force Enumeration): Evaluates all $2^N$ binary combinations to guarantee the 100% optimal global revenue.
# - Greedy Heuristic (Revenue Density Ratio): Sorts shipments by efficiency ($/kg) and loads them until space runs out.
# - Metaheuristic (Iterated Local Search - ILS): Begins with the greedy solution and executes iterative local swaps and structural perturbations to escape local optima.
# ==========================================

import time
import random
import itertools

# ==========================================
# 1. PROBLEM INSTANCE GENERATOR
# ==========================================
def generate_cargo_problem(num_items, capacity_ratio=0.45, seed=42):
    """
    Generates a realistic cargo loading instance.
    capacity_ratio sets W_max relative to total weight of all cargo.
    """
    random.seed(seed + num_items)  # Seed varies predictably with scale N
    weights = [random.randint(20, 150) for _ in range(num_items)]
    values = [random.randint(100, 1200) for _ in range(num_items)]
    max_weight = int(sum(weights) * capacity_ratio)
    return weights, values, max_weight

# ==========================================
# 2. EXACT METHOD: Brute-Force Enumeration O(2^N)
# ==========================================
def exact_brute_force(weights, values, max_weight):
    start_time = time.perf_counter()
    n = len(weights)
    best_value = 0
    
    # Evaluate all 2^N combinations
    for combination in itertools.product([0, 1], repeat=n):
        curr_w = sum(combination[i] * weights[i] for i in range(n))
        curr_v = sum(combination[i] * values[i] for i in range(n))
        if curr_w <= max_weight and curr_v > best_value:
            best_value = curr_v
                
    exec_time = time.perf_counter() - start_time
    return best_value, exec_time

# ==========================================
# 3. GREEDY HEURISTIC: Revenue Density O(N log N)
# ==========================================
def heuristic_greedy_ratio(weights, values, max_weight):
    start_time = time.perf_counter()
    n = len(weights)
    
    # Sort items by value-to-weight ratio ($/kg) descending
    sorted_indices = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    
    total_w = 0
    total_v = 0
    for i in sorted_indices:
        if total_w + weights[i] <= max_weight:
            total_w += weights[i]
            total_v += values[i]
            
    exec_time = time.perf_counter() - start_time
    return total_v, exec_time

# ==========================================
# 4. METAHEURISTIC: Iterated Local Search (ILS)
# ==========================================
def metaheuristic_ils(weights, values, max_weight, max_iterations=300):
    start_time = time.perf_counter()
    n = len(weights)
    
    sorted_indices = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    
    def evaluate(sol):
        w = sum(sol[i] * weights[i] for i in range(n))
        v = sum(sol[i] * values[i] for i in range(n))
        return (v, w) if w <= max_weight else (0, w)

    # Smart Warm Start: Initialize with Greedy Solution
    current_sol = [0] * n
    curr_w = 0
    for i in sorted_indices:
        if curr_w + weights[i] <= max_weight:
            current_sol[i] = 1
            curr_w += weights[i]
            
    best_sol = list(current_sol)
    best_val, _ = evaluate(best_sol)
    
    # Iterated Search Loop
    for _ in range(max_iterations):
        candidate = list(current_sol)
        
        # Perturbation: Flip 2 random bits
        idx1, idx2 = random.sample(range(n), 2)
        candidate[idx1] = 1 - candidate[idx1]
        candidate[idx2] = 1 - candidate[idx2]
        
        cand_v, cand_w = evaluate(candidate)
        
        # Repair mechanism: Remove least efficient items if over capacity
        if cand_w > max_weight:
            for i in reversed(sorted_indices):
                if candidate[i] == 1:
                    candidate[i] = 0
                    cand_v, cand_w = evaluate(candidate)
                    if cand_w <= max_weight:
                        break
                        
        # Acceptance Criterion
        if cand_v > best_val:
            best_val = cand_v
            best_sol = list(candidate)
            current_sol = list(candidate)
            
    exec_time = time.perf_counter() - start_time
    return best_val, exec_time

# ==========================================
# 5. BENCHMARK EXECUTION
# ==========================================
def run_student_benchmark():
    sizes = [10, 12, 14, 16, 18, 20, 22, 24]
    
    print(f"{'Scale (N)':<10} | {'Algorithm':<22} | {'Revenue ($)':<12} | {'Time (ms)':<10} | {'Optimality (%)':<12}")
    print("=" * 75)
    
    for N in sizes:
        weights, values, max_weight = generate_cargo_problem(N, capacity_ratio=0.45, seed=100)
        
        # Exact Method
        val_exact, time_exact = exact_brute_force(weights, values, max_weight)
        t_exact_ms = time_exact * 1000
        
        # Greedy Heuristic
        val_heur, time_heur = heuristic_greedy_ratio(weights, values, max_weight)
        t_heur_ms = time_heur * 1000
        opt_heur = (val_heur / val_exact) * 100
        
        # Metaheuristic (ILS)
        val_meta, time_meta = metaheuristic_ils(weights, values, max_weight)
        t_meta_ms = time_meta * 1000
        opt_meta = (val_meta / val_exact) * 100
        
        print(f"{N:<10} | {'Exact (Brute-Force)':<22} | ${val_exact:<11} | {t_exact_ms:<10.3f} | 100.0%")
        print(f"{N:<10} | {'Greedy Heuristic':<22} | ${val_heur:<11} | {t_heur_ms:<10.3f} | {opt_heur:.1f}%")
        print(f"{N:<10} | {'Metaheuristic (ILS)':<22} | ${val_meta:<11} | {t_meta_ms:<10.3f} | {opt_meta:.1f}%")
        print("-" * 75)

if __name__ == "__main__":
    run_student_benchmark()
