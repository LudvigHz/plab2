from rock_paper_scissors.SingleGame import SingleGame


class ManyGames:
    """
    Class for a series of single games, takes two opponents
    and a numnber of games to run.
    """

    def __init__(self, player1, player2, amount):
        self.player1 = player1
        self.player2 = player2
        self.amount = amount
        self.amount_played = 0

    def arrange_single_game(self):
        """Runs a single game with the two players in the tounament."""
        game = SingleGame(self.player1, self.player2)
        game.run_game()
        self.amount_played += 1
        print(game)

    def arrage_all_games(self):
        """Runs all games specified with the tournaments length."""
        while self.amount_played < self.amount:
            self.arrange_single_game()
        print(f"{self.player1} stats: {self.player1.get_all_results()}")
        print(f"{self.player2} stats: {self.player2.get_all_results()}")
