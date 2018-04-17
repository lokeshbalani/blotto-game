import random
import math
import numpy as np
from operator import add
from cvxopt import matrix, solvers

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

        # Getting the troop deployment strategies
        A_strats = self.list_strat(A, B)
        n_A_strats = len(A_strats)

        #print(A_strats)

        D_strats = self.list_strat(D, B)
        n_D_strats = len(D_strats)

        #print(D_strats)

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
        
        return np.array(gm_mtx)

    def lp_opt_sol(self, gm_mtx, solver="glpk"):
        '''
        Solves Linear Programs in the following form:

        min_{x} f.T @ x
        s.t     A @ x <= b
                A_eq @ x = b_eq
                lb <= x

        This implies that for attacker:
        x.T = [p1, p2, p3, ...., pm, v]
        f.T = [0, 0, 0, ..., -1]
        A = [[-g_{1,1}, ....., -g_{m,1}, 1]
             [-g_{1,2}, ....., -g_{m,2}, 1]
             ....
             [-g_{1,n}, ....., -g_{m,n}, 1]]
        A_eq = [1,1,....,1,0]
        b_eq = 1
        b.T = [0,0,...., 0]

        This implies that for defender:
        x.T = [q1, q2, q3, ...., qn, w]
        f.T = [0, 0, 0, ..., 1]
        A = [[g_{1,1}, ....., g_{m,1}, -1]
             [g_{1,2}, ....., g_{m,2}, -1]
             ....
             [g_{1,n}, ....., g_{m,n}, -1]]
        A_eq = [1,1,....,1,0]
        b_eq = 1
        b.T = [0,0,...., 0]
        '''
        m_mtx, n_mtx = gm_mtx.shape

        '''Solving for Attacker'''
        # f.T denoted as f
        f_A = [0 for i in range(m_mtx)] + [-1]
        f_A = np.array(f_A, dtype="float")
        f_A = matrix(f_A)

        # constraints A @ x <= b
        A = np.matrix(gm_mtx, dtype="float").T # reformat each variable is in a row
        print(A)
        A *= -1 # minimization constraint
        A = np.vstack([A, np.eye(m_mtx) * -1]) # > 0 constraint for all vars
        new_col = [1 for i in range(m_mtx)] + [0 for i in range(m_mtx)]
        A = np.insert(A, 0, new_col, axis=1) # insert utility column
        A = matrix(A)

        b_A = ([0 for i in range(m_mtx)] + [0 for i in range(m_mtx)])
        b_A = np.array(b_A, dtype="float")
        b_A = matrix(b_A)

        # contraints A_eq @ x = b_eq
        A_eq = [0] + [1 for i in range(m_mtx)]
        A_eq = np.matrix(A_eq, dtype="float")
        A_eq = matrix(A_eq)
        b_A_eq = np.matrix(1, dtype="float")
        b_A_eq = matrix(b_A_eq)

        # solve the LP for Attacker
        sol_A = solvers.lp(c=f_A, G=A, h=b_A, A=A_eq, b=b_A_eq, solver=solver)

        '''Solving for defender'''
        # f.T denoted as f
        f_D = [0 for i in range(n_mtx)] + [1]
        f_D = np.array(f_D, dtype="float")
        f_D = matrix(f_D)

        # constraints D @ x <= b
        D = np.matrix(gm_mtx, dtype="float").T # reformat each variable is in a row
        print(D)
        D = np.vstack([D, np.eye(n_mtx) * 1]) # > 0 constraint for all vars
        new_col = [1 for i in range(n_mtx)] + [0 for i in range(n_mtx)]
        D = np.insert(D, 0, new_col, axis=1) # insert utility column
        D = matrix(D)

        b_D = ([0 for i in range(n_mtx)] + [0 for i in range(n_mtx)])
        b_D = np.array(b_D, dtype="float")
        b_D = matrix(b_D)

        # contraints A_eq @ x = b_eq
        D_eq = [0] + [1 for i in range(n_mtx)]
        D_eq = np.matrix(D_eq, dtype="float")
        D_eq = matrix(D_eq)
        b_D_eq = np.matrix(1, dtype="float")
        b_D_eq = matrix(b_D_eq)

        # solve the LP for Attacker
        sol_D = solvers.lp(c=f_D, G=A, h=b_D, A=D_eq, b=b_D_eq, solver=solver)

        return sol_A, sol_D


game_lp = BlottoLP(4,5,2)

gm_mtx = game_lp.game_matrix()
#print(gm_mtx)

game_lp.lp_opt_sol(gm_mtx)

