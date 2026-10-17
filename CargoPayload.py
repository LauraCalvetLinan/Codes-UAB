# ==========================================
# As a hub cargo dispatcher for an air express carrier, you must choose which high-priority air shipments to load onto a regional freighter flight. 
# The aircraft has a maximum structural payload weight capacity ($W_{max}$). Each potential shipment $i$ has a verified weight $w_i$ (kg) and an associated revenue $v_i$ ($).
# Your goal is to maximize total flight revenue without exceeding $W_{max}$.
# You will test and compare three algorithmic paradigms across problem sizes $N \in [10, 12, 14, 16, 18, 20, 22, 24]$:
# - Exact Method (Brute-Force Enumeration): Evaluates all $2^N$ binary combinations to guarantee the 100% optimal global revenue. Max: 60 seconds.
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
    random.seed(seed + num_items)
    weights = [random.randint(20, 150) for _ in range(num_items)]
    values = [random.randint(100, 1200) for _ in range(num_items)]
    max_weight = int(sum(weights) * capacity_ratio)
    return weights, values, max_weight

# ==========================================
# 2. EXACT METHOD: Brute-Force with 60s Timeout
# ==========================================
def exact_brute_force_timed(weights, values, max_weight, time_limit=60.0):
    start_time = time.perf_counter()
    n = len(weights)
    best_value = 0
    is_optimal = True
    
    # Iterate through all 2^N combinations
    for idx, combination in enumerate(itertools.product([0, 1], repeat=n)):
        # Periodically check time limit every 10,000 evaluations to minimize timer overhead
        if idx % 10000 == 0:
            if (time.perf_counter() - start_time) >= time_limit:
                is_optimal = False
                break
                
        curr_w = sum(combination[i] * weights[i] for i in range(n))
        curr_v = sum(combination[i] * values[i] for i in range(n))
        
        if curr_w <= max_weight and curr_v > best_value:
            best_value = curr_v
                
    exec_time = time.perf_counter() - start_time
    return best_value, exec_time, is_optimal

# ==========================================
# 3. GREEDY HEURISTIC: Revenue Density O(N log N)
# ==========================================
def heuristic_greedy_ratio(weights, values, max_weight):
    start_time = time.perf_counter()
    n = len(weights)
    
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
def metaheuristic_ils(weights, values, max_weight, max_iterations=500):
    start_time = time.perf_counter()
    n = len(weights)
    
    sorted_indices = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    
    def evaluate(sol):
        w = sum(sol[i] * weights[i] for i in range(n))
        v = sum(sol[i] * values[i] for i in range(n))
        return (v, w) if w <= max_weight else (0, w)

    # Smart Warm Start
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
        
        # Repair mechanism
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
# 5. BENCHMARK EXECUTION & GAP COMPUTATION
# ==========================================
def run_student_benchmark():
    sizes = [10, 15, 20, 25, 30]
    
    print(f"{'Scale (N)':<10} | {'Algorithm':<22} | {'Revenue ($)':<12} | {'Time (s)':<12} | {'Gap (%)':<10} | {'Status'}")
    print("=" * 82)
    
    for N in sizes:
        weights, values, max_weight = generate_cargo_problem(N, capacity_ratio=0.45, seed=100)
        
        # 1. Run Exact Method (60s limit)
        val_exact, time_exact, is_optimal = exact_brute_force_timed(weights, values, max_weight, time_limit=60.0)
        
        # 2. Run Greedy Heuristic
        val_heur, time_heur = heuristic_greedy_ratio(weights, values, max_weight)
        
        # 3. Run Metaheuristic (ILS)
        val_meta, time_meta = metaheuristic_ils(weights, values, max_weight)
        
        # Determine the best known baseline value to compute gaps
        best_known_val = max(val_exact, val_heur, val_meta)
        
        # Calculate percentage gaps: Gap = (Best_Known - Method_Val) / Best_Known * 100
        gap_exact = ((best_known_val - val_exact) / best_known_val) * 100
        gap_heur = ((best_known_val - val_heur) / best_known_val) * 100
        gap_meta = ((best_known_val - val_meta) / best_known_val) * 100
        
        status_exact = "Proven Optimal" if is_optimal else "TIMED OUT (60s)"
        
        # Output Row Formats
        print(f"{N:<10} | {'Exact (Brute-Force)':<22} | ${val_exact:<11} | {time_exact:<12.4f} | {gap_exact:<9.2f}% | {status_exact}")
        print(f"{N:<10} | {'Greedy Heuristic':<22} | ${val_heur:<11} | {time_heur:<12.6f} | {gap_heur:<9.2f}% | Completed")
        print(f"{N:<10} | {'Metaheuristic (ILS)':<22} | ${val_meta:<11} | {time_meta:<12.6f} | {gap_meta:<9.2f}% | Completed")
        print("-" * 82)

if __name__ == "__main__":
    run_student_benchmark()
