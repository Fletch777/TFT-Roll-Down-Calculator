import argparse
import numpy as np
from Markov import Markov
from tft import Data

def simulate_roll_down(gold, level, unit_cost, units_enemies, units_owned):
    levelOdds = Data.levelOdds
    unitsTotal = Data.unitsTotal
    unitsEach = Data.unitsEach

    units_needed = 9 - units_owned
    purchase_cost = units_needed * unit_cost
    effective_gold = gold - purchase_cost

    if effective_gold < 0:
      return None, purchase_cost, effective_gold

    rolls = round(effective_gold / 2)
    total_slots = rolls * 5

    # 2. Base pools: Subtract ONLY enemy holdings
    # (Your holdings 'i' are subtracted dynamically inside the loop)
    base_target_pool = unitsEach[unit_cost] - units_enemies
    base_total_pool = unitsTotal[unit_cost] - units_enemies

    # 3. Build the 10x10 row-stochastic transition matrix
    p_table = np.zeros((10, 10), dtype=float)

    for i in range(9):
      # At state i, you hold i units, so we subtract i from the pool
      target_rem = base_target_pool - i
      total_rem = base_total_pool - i

      if target_rem > 0 and total_rem > 0:
        p_slot = levelOdds[level - 1][unit_cost] * (target_rem / total_rem)
      else:
        p_slot = 0.0

      p_slot = max(0.0, min(1.0, p_slot))  # Clamp between 0 and 1

      p_table[i, i] = 1.0 - p_slot  # Miss: stay at i units
      p_table[i, i + 1] = p_slot  # Hit: advance to i + 1 units

    # State 9 (3-star) is absorbing
    p_table[9, 9] = 1.0

    initial_state = np.zeros(10, dtype=float)
    initial_state[units_owned] = 1.0

    outcome_state = Markov.calc(initial_state, p_table, total_slots)
    
    return outcome_state, purchase_cost, effective_gold

def main():
    # arguments
    parser = argparse.ArgumentParser(description="TFT Rolldown Probability Calculator")
    parser.add_argument("-g", "--gold", type=int, required=True, help="Total gold available")
    parser.add_argument("-l", "--level", type=int, required=True, help="Player level")
    parser.add_argument("-c", "--cost", type=int, required=True, help="Unit cost (1-5)")
    parser.add_argument("-e", "--enemies", type=int, default=0, help="Units held by enemy players")
    parser.add_argument("-o", "--owned", type=int, default=0, help="Units currently owned")
    
    args = parser.parse_args()
    
    outcome, cost, eff_gold = simulate_roll_down(
        args.gold, args.level, args.cost, args.enemies, args.owned
    )
    
    print("\n--- Roll Stats ---")
    print(f"Total Gold: {args.gold}")
    
    if outcome is None:
        print(f"Error: Need at least {cost} gold just to purchase the remaining units.")
        return
        
    rolls = round(eff_gold / 2)
    print(f"Purchase Cost: {cost}")
    print(f"Effective Roll Gold: {eff_gold} ({rolls} rolls)")
    
    print("\n--- Probability Distribution ---")
    for i, prob in enumerate(outcome):
        print(f"{i} units: {prob * 100:.2f}%")

if __name__ == "__main__":
    main()