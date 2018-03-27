import random
import os

class Blotto:
    def __init__(self, n_sol, n_battles):
        '''Set the number of soldiers available and the number of battlefields'''
        self.n_soldiers = n_sol
        self.n_battlefields = n_battles
        print("#Soldiers : {}".format(self.n_soldiers))
        print("#Battlefields : {}".format(self.n_battlefields))


print("Input the Number of Soldiers")
inp_n_soldiers = input("[User]: ")
print("Input the Number of Battlefronts")
inp_n_battlefronts = input("[User]: ")
Blotto(inp_n_soldiers, inp_n_battlefronts)
