# Authors: Lokesh Balani, Aditya Saripalli, 2018
#
# A simulator for a Weighted Colonel Blotto game that is played as follows:
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
    def __init__(self,
                 n_sol,
                 n_bfs):
        """ Set the number of soldiers available and the number of battlefields """
        self.n_soldiers = int(n_sol)
        self.n_battlefields = int(n_bfs)
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


    def prepare_dataset(self,
                        dir_list):
        dataset = []
        for path in dir_list:
            for line in self.read_dataset(path):
                sol = [int(float(item)) for item in line.split(",")]
                if sum(sol) == self.n_soldiers:
                    dataset.append(sol)
        return dataset

    # Reads in the given file and creates a list of betting selections from the data
    @staticmethod
    def read_dataset(dataset_path):
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

        # Empty list for list of strategies
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

        # Validate the strategies
        assert sum(strategy) == self.n_soldiers

        # Shuffle the strategies and return
        random.shuffle(strategy)
        return strategy

    def random_strategy_set(self,
                            n_strategies):
        # Empty list for storing list of strategies
        strategy_set = []
        # Keep going until we put n_strategies in strategy set
        while len(strategy_set) < n_strategies:
            strategy_set.append(self.random_strategy())
        return strategy_set

    def player_scores(self,
                      player1_strategy,
                      player2_strategy):
        # Determine which player wins each battlefield. If each player has 
        # attacked with the same number of soldiers, battlefield is won by
        # neither
        p1_score = 0
        p2_score = 0

        # Assign scores
        for i in range(0, self.n_battlefields):
            if player1_strategy[i] > player2_strategy[i]:
                p1_score += (i + 1)
            elif player2_strategy[i] > player1_strategy[i]:
                p2_score += (i + 1)
        return p1_score, p2_score

    def pl_strategy_stats(self,
                          pl_strategy,
                          dataset):
        # Calculates wins losses and ties that a strategy achieves
        # when compared against every selection in dataset
        #
        # Params:
        #   strategy : the strategy to compare
        #   dataset : pruned subset of valid strategy space for the game
        # Returns:  
        #   tuple : (no_of_wins, no_of_ties, no_of_losses)
        #
        n_wins = 0
        n_losses = 0
        n_ties = 0

        for strategy in dataset:
            pl_strategy_score, strategy_score = self.player_scores(pl_strategy,
                                                                   strategy)
            # Determine if given player strategy wins, draws, or loses
            if pl_strategy_score > strategy_score:
                n_wins += 1
            elif pl_strategy_score < strategy_score:
                n_losses += 1
            else:
                n_ties += 1
        return n_wins, n_ties, n_losses

    @staticmethod
    def calc_final_score(strategy_stats):
        # Score-calculating function that assigns appropriate score
        # (5pts for a win, 2 for a tie, 0 for a loss)
        # 
        # Params:
        #   strategy_stats : tuple (no_of_wins, no_of_ties, no_of_losses)
        # Return:
        #   number : score for the strategy
        return 3 * strategy_stats[0] + 2 * strategy_stats[1]



print("Input the Number of Soldiers")
inp_n_soldiers = input("[User]: ")
print("Input the Number of Battlefronts")
inp_n_battlefronts = input("[User]: ")
Blotto(inp_n_soldiers, inp_n_battlefronts)
