import random
import math
import numpy as np
from operator import add

class BlottoLP:
    def __init__(self, n_sol_atk, n_sol_def, n_bfs):
        self.n_sol_attacker = n_sol_atk
        self.n_sol_defender = n_sol_def
        self.n_battlefields = n_bfs

    def unique_depl_strats(self, depl_strat_list):
        '''Extract and return unique deplyment strategies'''
        strats = [s for s in depl_strat_list]

        for idx, s in enumerate(strats):
            kidx = idx + 1
            while kidx < len(strats):
                if set(s) == set(strats[kidx]):
                    del strats[kidx]
                else:
                    kidx += 1
        
        return strats

    def list_strat(self, n_sol, n_bfs):
        '''
        list_strat creates a matrix with all strategies for
        a number of armies

        Lists all the strategies that a player has where
          no of troops = n_sol
          no of bases = n_bfs

        The strategies are given in a matrix where each row
        represents a strategy
        '''

        strategies = []

        if n_bfs == 2:
            i = n_sol
            j = 0
            strategies.extend([[i,j]])

            while i > (j + 1):
                i -= 1
                j += 1
                strategies.extend([[i,j]])
        else:
            i = n_sol
            j = 0
            strategies.extend([[i, j] + [0] * (n_bfs - 2)])

            while i > math.ceil(n_sol / n_bfs):
                i -= 1
                j += 1
                strat = self.list_strat(j, n_bfs - 1)
                n_strat = len(strat)
                leading_nums = [[0] for n in range(n_strat)]

                for r in range(n_strat):
                    leading_nums[r] = [i]

                unsorted_strats = map(add, leading_nums, strat)
                sorted_strats = sorted(unsorted_strats, key=lambda s: s[1], reverse=True)

                strategies.extend(sorted_strats)

                strategies = self.unique_depl_strats(strategies)
                
        return strategies

    def game_matrix(self):
        '''
        Creates a matrix for the Blotto Game with
           A = no of troops with the attacker
           D = no of troops with the defender
           B = no of battlefields
        '''

        A = self.n_sol_attacker
        D = self.n_sol_defender
        B = self.n_battlefields
        print(B)

        # Getting the troop deployment strategies
        A_strats = self.list_strat(A, B)
        n_A_strats = len(A_strats)

        print(A_strats)

        D_strats = self.list_strat(D, B)
        n_D_strats = len(D_strats)

        print(D_strats)

        # Zero Initialise the Game Matrix
        gm_mtx = np.zeros([n_A_strats, n_D_strats])

        for a_s_idx in range(n_A_strats):
            for d_s_idx in range(n_D_strats):
                # Reset and initialise the bases captured
                bfs_win = 0

                for a_b in range(B):
                    for d_b in range(B):
                        if A_strats[a_s_idx][a_b] > D_strats[d_s_idx][d_b]:
                            bfs_win += 1

                gm_mtx[a_s_idx][d_s_idx] = bfs_win / B
        
        return gm_mtx

game_lp = BlottoLP(4,5,2)

gm_mtx = game_lp.game_matrix()
print(gm_mtx)

