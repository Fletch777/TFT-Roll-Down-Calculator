import time
import numpy as np
import matplotlib.pyplot as plt
from main import simulate_roll_down
from tft import Data

def run_monte_carlo(gold, level, unit_cost, units_enemies, units_owned, num_simulations=100_000):
    units_needed = 9 - units_owned
    purchase_cost = units_needed * unit_cost
    effective_gold = gold - purchase_cost
    rolls = round(effective_gold / 2)
    total_slots = rolls * 5
    
    base_target = Data.unitsEach[unit_cost] - units_enemies
    base_total = Data.unitsTotal[unit_cost] - units_enemies
    hit_rate_base = Data.levelOdds[level - 1][unit_cost]
    
    results = np.zeros(num_simulations, dtype=int)
    
    for sim in range(num_simulations):
        current_units = units_owned
        for _ in range(total_slots):
            # Absorbing state (3-star hit)
            if current_units >= 9:
                break
                
            target_rem = base_target - current_units
            total_rem = base_total - current_units
            
            if target_rem > 0 and total_rem > 0:
                p_slot = hit_rate_base * (target_rem / total_rem)
            else:
                p_slot = 0.0
                
            # Random draw for a single shop slot
            if np.random.rand() < p_slot:
                current_units += 1
                
        results[sim] = current_units
        
    # Count frequencies to build the empirical probability distribution
    counts = np.bincount(results, minlength=10)
    return counts / num_simulations

def plot_comparison():
    # Test Scenario: 50 gold, Level 8, 4-cost, 2 gone, 1 owned
    gold, level, cost, enemies, owned = 50, 8, 4, 2, 1
    
    # 1. Markov Execution (Using high-res perf_counter)
    start_time = time.perf_counter()
    markov_outcome, _, _ = simulate_roll_down(gold, level, cost, enemies, owned)
    markov_time = time.perf_counter() - start_time
    
    # 2. Monte Carlo Execution
    start_time = time.perf_counter()
    mc_outcome = run_monte_carlo(gold, level, cost, enemies, owned, num_simulations=100_000)
    mc_time = time.perf_counter() - start_time
    
    # Prevent divide-by-zero just in case it still registers as 0 on a supercomputer
    safe_markov = max(markov_time, 1e-9)
    
    print(f"Markov Execution Time:      {markov_time:.6f} seconds")
    print(f"Monte Carlo Time (100k):    {mc_time:.6f} seconds")
    print(f"Performance Speedup:        {mc_time / safe_markov:,.0f}x faster")
    
    # 3. Plotting
    x = np.arange(10)
    width = 0.35
    
    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, markov_outcome * 100, width, label='Markov Chain (Theoretical)')
    plt.bar(x + width/2, mc_outcome * 100, width, label='Monte Carlo (Empirical)')
    
    plt.title('TFT Rolldown Distribution: Markov vs. Monte Carlo')
    plt.xlabel('Final Unit Count')
    plt.ylabel('Probability (%)')
    plt.xticks(x)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    plt.savefig('comparison.png')
    
    
if __name__ == "__main__":
    plot_comparison()