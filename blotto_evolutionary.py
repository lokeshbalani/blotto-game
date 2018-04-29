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
#  Player 1's bets:   4   2   3   1
#  ----------------------------------
#  Battlefields:      1   2   3   4
#  ----------------------------------
#  Player 2's bets:   0   0   2   8
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
import os


class Blotto:
    def __init__(self,
                 n_sol,
                 n_bfs):
        """ Set the number of soldiers available and the number of battlefields """
        self.n_soldiers = int(n_sol)
        self.n_battlefields = int(n_bfs)
        self.train_data = None
        self.r_dataset = self.random_strategy_set(5000)
        self.dataset = self.prepare_dataset(["./dataset/bf_strategies_1.csv",
                                             "./dataset/bf_strategies_2.csv"])
        print("#Soldiers : {}".format(self.n_soldiers))
        print("#Battlefields : {}".format(self.n_battlefields))

        # print("--------------------------------")
        # print("Random Generated Dataset")
        # print("--------------------------------")
        # for i in range(len(self.r_dataset)):
        #     print("Strategy #{} : {}".format(i + 1, self.r_dataset[i]))

        # print("--------------------------------")
        # print("Five Thirty Eight Dataset")
        # print("--------------------------------")
        # for i in range(len(self.dataset)):
        #     print("Strategy #{} : {}".format(i + 1, self.dataset[i]))


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
        self.player_strats = blotto_game.random_strategy_set(self.n_players)

        print("Initial Player Strategies")
        for i in range(len(self.player_strats)):
            print("Strategy #{} : {}".format(i + 1, self.player_strats[i]))

    def calc_pl_score(self, pl_strat):
        return self.game.calc_final_score(self.game.pl_strategy_stats(pl_strat, self.game.r_dataset))

    def pl_strat_sorted(self):
        pl_scores = [(pl_strat, self.calc_pl_score(pl_strat)) for pl_strat in self.player_strats]

        return sorted(pl_scores, key= lambda pl_score: pl_score[1], reverse=True)

    def pl_strat_update(self):
        # Creates the next generation of strategies 
        # from the current one

        # Maintains a list of selections, ranked by their scores. 
        # Every time this list is updated, the top third of the list is maintained, 
        # another third is composed of mutants of the top third, 
        # and the final third is composed of random selections

        # Player Straties ranked by score
        pl_strat_ranking = self.pl_strat_sorted()

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
bot = Bot(blotto_game)

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
    curr_strat_stats = blotto_game.pl_strategy_stats(curr_best_strat, blotto_game.r_dataset)
    print("Current Best Strategy Performance Stats")
    print("---------------------------------------")
    print("Wins: {}".format(curr_strat_stats[0]))
    print("Ties: {}".format(curr_strat_stats[1]))
    print("Losses: {}".format(curr_strat_stats[2]))
    print("Current Best Strategy Score: {}".format(blotto_game.calc_final_score(curr_strat_stats)))


best_strat = bot.player_strats[0]
print("Best Strategy: {}".format(best_strat))    
strat_stats = blotto_game.pl_strategy_stats(best_strat, blotto_game.r_dataset)
print("Best Strategy Performance Stats")
print("---------------------------------------")
print("Wins: {}".format(strat_stats[0]))
print("Ties: {}".format(strat_stats[1]))
print("Losses: {}".format(strat_stats[2]))
print("Best Strategy Score: {}".format(blotto_game.calc_final_score(strat_stats)))


