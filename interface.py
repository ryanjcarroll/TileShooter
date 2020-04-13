
class Interface:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player

    def update(self):
        self.draw_player_hp()

    def draw_player_hp(self):
        