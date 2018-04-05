# Authors: Lokesh Balani, Aditya Saripalli, 2018
#
# A simultor for a Weighted Colonel Blotto game that is played as follows:
#
# We are given battlefields labelled 1-n, and we say that the battlefield's
# label is its value. Two players present attack strategies given
# a fixed number of soldiers, deciding how many soldiers they want
# to send to every battlefield. Once the bets are compared, the player with
# the most soldiers at a battlefield wins that battlefield's points. For 4
# battlefield and 10 soldiers, this might look like:
#
#
#  Player 1's bets:   4   2   3   1
#  ----------------------------------
#  Battlefields:      1   2   3   4
#  ----------------------------------
#  Player 2's bets:   0   0   5   5
#
#
# In this case, Player 1 is assigned a score of 3, because the player
# won the battlefields labelled 1 and 2. Player 2 scores 7 for winning the
# other two battlefields and thus wins the game
#
# 

import random
import os

class Blotto:
    def __init__(self, n_sol, n_battles):
        '''Set the number of soldiers available and the number of battlefields'''
        self.n_soldiers = int(n_sol)
        self.n_battlefields = int(n_battles)
        self.train_data = None
        self.r_dataset = self.random_strategy_set(1000)
        self.dataset = self.prepare_dataset(["./dataset/castle-solutions.csv", "./dataset/castle-solutions-2.csv"])
        print("#Soldiers : {}".format(self.n_soldiers))
        print("#Battlefields : {}".format(self.n_battlefields))

        print("--------------------------------")
        print("Random Generated Dataset")
        print("--------------------------------")
        for i in range(len(self.r_dataset)):
            print("Strategy #{} : {}".format(i + 1, self.r_dataset[i]))

        print("--------------------------------")
        print("Five Thirty Eight Dataset")
        print("--------------------------------")
        for i in range(len(self.dataset)):
            print("Strategy #{} : {}".format(i + 1, self.dataset[i]))


    def prepare_dataset(self, dir_list):
        dataset = []

        for path in dir_list:
            for line in self.read_dataset(path):
                sol = [int(float(item)) for item in line.split(",")]
                if sum(sol) == self.n_soldiers:
                    dataset.append(sol)

        return dataset

    # Reads in the given file and creates a list of betting selections from the data
    def read_dataset(self, dataset_path):
        data = []
        with open(dataset_path, "r", encoding="utf-8") as file:
            for line in file.readlines()[1:]:
                data.append(line)

        return data

    # Create a single random integer-valued strategy that sums to 
    # No of soldiers with length equal to number of battlefields
    def random_strategy(self):
        # Create a random resource variable
        res = self.n_soldiers

        #Empty list
        strategy = []

        for i in range(self.n_battlefields - 1):
            # Fill each position in strategy with a random number 
            # between 0 and remaining reserves
            rand = random.randint(0, res)
            # add this to the strategy
            strategy.append(rand)
            # Reduce reserves by the allocated number
            res -= rand

        # Add any remaining reserves at the last
        strategy.append(res)

        # Shuffle the strategy
        random.shuffle(strategy)

        return strategy

    def random_strategy_set(self, n_strategies):
        #Empty list
        strategy_set = []
        strategy = []

        #Keep going until we put n_strategies in strategy set
        while len(strategy_set) < n_strategies:
            strategy = self.random_strategy()

            if sum(strategy)  == self.n_soldiers:
                strategy_set.append(strategy)

        return strategy_set




print("Input the Number of Soldiers")
inp_n_soldiers = input("[User]: ")
print("Input the Number of Battlefronts")
inp_n_battlefronts = input("[User]: ")
Blotto(inp_n_soldiers, inp_n_battlefronts)
