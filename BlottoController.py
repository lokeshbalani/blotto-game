from Blotto import *

class BlottoController:
    def __init__(self, uinput=None):
        self.inp = uinput

    def game_mode(self, uinput):
        g_choice = {
            '1': "player_v_player",
            '2': "player_v_bot"
        }

        g_sel = g_choice[str(uinput)]
        print(g_sel)
        game = getattr(self, g_sel, lambda: "Invalid Game Option")

        return game()

    def player_v_player(self):
        return "Player vs Player"

    def player_v_bot(self):
        return "Player vs Bot"

print("BLOTTO GAME PORTAL")
print("Welcome to Blotto Game. Which mode would you like to play?")
print("1. PvP")
print("2. PvC")
print("3. Generate the 10 most probable winning strategies")

print("[BOT]: Hi! Select the game mode")
inp = input("[User]: ")
play = BlottoController().game_mode(inp)
print(play)
