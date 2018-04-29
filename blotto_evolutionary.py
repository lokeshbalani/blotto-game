# Authors: Lokesh Balani, Aditya Saripalli, 2018
#
# A simulator for a Weighted Colonel Blotto game that is played as follows:
#
# We are given battlefields labelled 1-n, and we assume that each battlefield has the same value.
# Two players present attack strategies given a fixed number of soldiers, deciding how many
# soldiers they want to send to every battlefield. Once the bets are compared, the player with
# the most number soldiers at a battlefield wins that battlefield's points.
# For 4 battlefield and 10 soldiers, this might look like:
#
#  Player 1's bets (Attacker) :   4   2   3   1
#  --------------------------------------------
#  Player 2's bets (Defender) :   0   0   2   8
#
#
# Player 1 is assigned a score of 3, because the player won 3 battlefields.
# Player 2 scores 1 for winning 1 Battlefield
# Hence Player-2 is the winner.
#
# Without loss of generality here is how we are going to assign scores
# Win - 5 points
# Loose -
#

import random
import operator as op
from collections import defaultdict
from functools import reduce


class Blotto:
    def __init__(self,
                 n_sol,
                 n_bfs):
        """ Set the number of soldiers available and the number of battlefields """
        self.n_soldiers = int(n_sol)
        self.n_battlefields = int(n_bfs)
        self.master_dataset = []
        self.unique_strategies = defaultdict(list)
        self.unique_strategies_count = 0
        print("#Soldiers : {}".format(self.n_soldiers))
        print("#Battlefields : {}".format(self.n_battlefields))

    def compute_strategy_space_size(self):
        n = self.n_soldiers + self.n_battlefields - 1
        k = self.n_battlefields - 1
        r = min(k, n - k)
        N = reduce(op.mul, range(n, n - r, -1), 1)
        D = reduce(op.mul, range(1, r + 1), 1)
        return N // D

    def validate_strategy(self, strategy):
        is_valid = False
        # Validate the strategies
        assert sum(strategy) == self.n_soldiers
        # verify the strategy string
        value_str = ""
        for value in strategy:
            value_str += str(value) + "_"
        value_str = value_str[:-1]
        value_str_len = len(value_str)

        # check for the uniqueness of the strategy string and append if unique
        if value_str_len in self.unique_strategies.keys():
            if value_str not in self.unique_strategies[value_str_len]:
                self.unique_strategies[value_str_len].append(value_str)
                is_valid = True
        else:
            self.unique_strategies[value_str_len] = [value_str]
            is_valid = True

        return is_valid

    # Create a single random integer-valued strategy that sums to
    # No of soldiers with length equal to number of battlefields
    def create_strategy(self):
        # Default validity of the strategy created
        is_valid = False

        # run the loop until we get a valid unique strategy
        while not is_valid:
            # Create a random strategy
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
            # Shuffle the strategies and return
            random.shuffle(strategy)

            # Validate the strategy
            is_valid = self.validate_strategy(strategy)

        return strategy

    def create_complete_strategy_space(self):
        size = self.compute_strategy_space_size()
        l_all_strategies = self.create_strategy_space(size)
        return l_all_strategies

    def create_strategy_space(self,
                              n_strategies):
        # Empty list for storing list of strategies
        strategy_set = []
        # Keep going until we put n_strategies in strategy set
        while len(strategy_set) < n_strategies:
            strategy_set.append(self.create_strategy())
        return strategy_set

    def compute_scores(self,
                       player_1_strategy,
                       player_2_strategy):
        # Determine which player wins each battlefield.
        # number_of_soldiers(Attacker) > number_of_soldiers(Defender)
        #     Attacker wins
        # Otherwise
        #     Defender wins
        player_1_score = 0
        player_2_score = 0
        # Assign scores
        for i in range(0, self.n_battlefields):
            if player_1_strategy[i] > player_2_strategy[i]:
                player_1_score += 1
            else:
                player_2_score += 1
        return player_1_score, player_2_score

    def get_strategy_stats(self,
                           pl_strategy):
        # Calculates wins / losses that a strategy achieves
        # when compared against every selection in dataset
        #
        # Params:
        #   strategy : the strategy to compare
        #   dataset : pruned subset of valid strategy space for the game
        # Returns:  
        #   tuple : (no_of_wins, no_of_losses)
        #
        n_wins = 0
        for strategy in self.master_dataset:
            pl_strategy_score, strategy_score = self.compute_scores(pl_strategy,
                                                                    strategy)
            # Determine if given player strategy wins, draws, or loses
            if pl_strategy_score > strategy_score:
                n_wins += 1
        return n_wins

    @staticmethod
    def duplicate_strat(self, strat):
        cp_strat = []

        for s in strat:
            cp_strat.append(s)

        return cp_strat

    def mutation(self, strat):
        # Mutates given selection slightly, 
        # by decrementing one bet and incrementing
        # another up to 10 times, selected randomly

        deploy_strat = self.duplicate_strat(strat)

        # Pick a a number in [1,..,n_bfs] for number of mutations
        n_mutations = random.randrange(self.n_battlefields)

        for i in range(n_mutations - 1):
            # Decrement deployment in one battlefield 
            # and increment another 
            # (these can be the same battlefields)

            rand_idx_1 = random.randrange(self.n_battlefields)
            rand_idx_2 = random.randrange(self.n_battlefields)

            bfs_1 = deploy_strat[rand_idx_1]

            if bfs_1 > 0:
                deploy_strat[rand_idx_1] -= 1
                deploy_strat[rand_idx_2] += 1

        return deploy_strat


class Bot:
    def __init__(self, blotto_game):
        self.game = blotto_game
        # Learning Strategy Space size
        self.n_players = 60
        # Initialise strategies for players randomly
        self.player_strategies = []
        # print("Initial Player Strategies")
        # for i in range(len(self.player_strats)):
        #     print("Strategy #{} : {}".format(i + 1, self.player_strats[i]))

    def create_learning_strategy_space(self):

    def calc_strategy_score(self, player_strategy):
        return self.game.get_strategy_stats(player_strategy)

    def sorted_strategies(self):
        strategy_scores = [(pl_strat, self.calc_strategy_score(pl_strat)) for pl_strat in self.player_strategies]
        return sorted(strategy_scores, key=lambda strategy_score: strategy_score[1], reverse=True)

    def pl_strat_update(self):
        # Creates the next generation of strategies 
        # from the current one

        # Maintains a list of selections, ranked by their scores. 
        # Every time this list is updated, the top third of the list is maintained, 
        # another third is composed of mutants of the top third, 
        # and the final third is composed of random selections

        # Player Strategies ranked by score
        pl_strat_ranking = self.sorted_strategies()

        # Populate a new generation
        next_gen_pl = []

        for i in range(self.n_players // 3):
            # Keep the top 33% player strategies from the rankings
            next_gen_pl.append(pl_strat_ranking[i][0])

            # Generate a random strategy, for variety in the next generation
            rand_strat = self.game.random_strategy()
            next_gen_pl.append(rand_strat)

            # Create a mutant of the top 33% player strategies
            mutant_strat = self.game.mutation(pl_strat_ranking[i][0])
            next_gen_pl.append(mutant_strat)

        self.player_strats = next_gen_pl


print("Input the Number of Soldiers")
inp_n_soldiers = input("[User]: ")
print("Input the Number of Battlefronts")
inp_n_battlefronts = input("[User]: ")


# Instantiate Game and Bot
blotto_game = Blotto(inp_n_soldiers, inp_n_battlefronts)
n_total_strategies = blotto_game.compute_strategy_space_size()
print("Total Number of Strategies possible:", n_total_strategies)
l_strategy_space = blotto_game.create_complete_strategy_space()
# for s in l_strategy_space: print(s)
# print("Total:", len(l_strategy_space))
# bot = Bot(blotto_game)

"""
# Run 1000 iterations
for idx in range(1):
    # Print generation number
    print("Generation #{}".format(idx))

    # Create new generation of strategies
    bot.pl_strat_update()

    # Print the best strategy of the bot for
    # the current generation/iteration
    curr_best_strat = bot.player_strats[0]
    print("Current Best Strategy: {}".format(curr_best_strat))    
    curr_strat_stats = blotto_game.pl_strategy_stats(curr_best_strat, blotto_game.master_dataset)
    print("Current Best Strategy Performance Stats")
    print("---------------------------------------")
    print("Wins: {}".format(curr_strat_stats[0]))
    print("Ties: {}".format(curr_strat_stats[1]))
    print("Losses: {}".format(curr_strat_stats[2]))
    print("Current Best Strategy Score: {}".format(blotto_game.calc_final_score(curr_strat_stats)))


best_strat = bot.player_strats[0]
print("Best Strategy: {}".format(best_strat))    
strat_stats = blotto_game.pl_strategy_stats(best_strat, blotto_game.master_dataset)
print("Best Strategy Performance Stats")
print("---------------------------------------")
print("Wins: {}".format(strat_stats[0]))
print("Ties: {}".format(strat_stats[1]))
print("Losses: {}".format(strat_stats[2]))
print("Best Strategy Score: {}".format(blotto_game.calc_final_score(strat_stats)))
"""
