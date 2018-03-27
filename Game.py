from Blotto import *
from Castle import *

class Game:
    def __init__(self, uinput=None):
        self.inp = uinput

    def game_to_play(self, uinput):
        g_choice = {
            '1': "blotto",
            '2': "castle"
        }

        g_sel = "play_" + g_choice[uinput]
        print(g_sel)
        game = getattr(self, g_sel, lambda: "Invalid Game")

        return game()

    def play_blotto(self):
        return "Blotto"

    def play_castle(self):
        return "Castle"

game_controller = Game()

print("TEAM 10 GAME PORTAL")
print("Welcome our game portal. Which game would you like to play?")
print("1. Classic Colonel Blotto Game")
print("2. Castle Puzzle")

while True:
    print("[BOT]: Hi! Which Game would you like to play?")
    inp = input("[User]: ")
    g_sel = game_controller.game_to_play(inp)
    print(g_sel)
