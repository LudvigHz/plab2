"""
Single game module.
contains the class for SingleGame
"""

class SingleGame:
    """
    A class for a single game, takes two players.
    """

    def __init__(self, player1, player2):
        self.player1, self.player2 = player1, player2
        self.winner = None

    def run_game(self):
        self.player1.choose_action(self.player2)
        self.player2.choose_action(self.player1)
        self.player1.receive_result(self.player2)
        self.player2.receive_result(self.player1)

        if self.player1.game_history[-1]["result"] == 2:
            self.winner = self.player1
        elif self.player2.game_history[-1]["result"] == 2:
            self.winner = self.player2

    def __str__(self):
        if self.winner == None:
            win_string = "Tie"
        else:
            win_string = f"{self.winner.get_name()} wins"
        return (
            f"{self.player1.get_name()}: {self.player1.last_action}.\t"
            f"{self.player2.get_name()}: {self.player2.last_action}\t -> {win_string}"
        )
