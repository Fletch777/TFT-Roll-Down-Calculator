import pytest
import numpy as np
from main import simulate_roll_down

def test_probabilities_sum_to_one():
    # A valid Markov chain must conserve probability across all states.
    # The sum of all state probabilities must equal exactly 1.0.
    outcome, _, _ = simulate_roll_down(gold=50, level=8, unit_cost=4, units_enemies=2, units_owned=1)
    assert sum(outcome) == pytest.approx(1.0)

def test_hard_pool_cap():
    # There are exactly 10 copies of a 4-cost unit in the game.
    # If enemies hold 7, and we own 2, only 1 copy is left in the shop pool.
    outcome, _, _ = simulate_roll_down(gold=500, level=8, unit_cost=4, units_enemies=7, units_owned=2)
    
    # 1. 0% chance to reach 4 units or higher (The cap works!)
    assert sum(outcome[4:]) == 0.0
    
    # 2. Because we started at 2 and the cap is 3, the final state 
    # MUST be either 2 or 3. Their probabilities must sum to 100%.
    assert outcome[2] + outcome[3] == pytest.approx(1.0)

def test_insufficient_gold():
    # If we need 3 copies of a 4-cost (12 gold minimum) and only have 10 gold total, 
    # the script should catch it before building the matrix.
    outcome, cost, eff_gold = simulate_roll_down(gold=10, level=8, unit_cost=4, units_enemies=0, units_owned=6)
    assert outcome is None
    assert eff_gold == -2