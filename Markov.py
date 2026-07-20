import numpy as np
class Markov():
    def __init__(self):
        pass
    
    @staticmethod
    def calc(initial_state: list, p_table: list, rolls: int):
        # take Sn = initial_state * P^n
        istate = np.array(initial_state)
        ptable = np.array(p_table)
        n: int = rolls
        ptable = np.linalg.matrix_power(ptable, n)
        
        outcome_state = np.matmul(istate, ptable)
        
        outcome_state = outcome_state / np.sum(outcome_state)
        return outcome_state
        