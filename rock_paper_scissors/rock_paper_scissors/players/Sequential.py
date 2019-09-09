from rock_paper_scissors import actionTypes
from rock_paper_scissors.players.BasePlayer import BasePlayer


class Sequential(BasePlayer):
    """
    Sequential player, chooses actions sequentially.
    """

    def __str__(self):
        return "Sequential"

    def __init__(self):
        super().__init__()
        self.current_index = 0
        self.action_sequence = [
            actionTypes.ROCK,
            actionTypes.PAPER,
            actionTypes.SCISSORS,
        ]

    def choose_action(self, opponent):
        super().choose_action(self.action_sequence[self.current_index])
        if self.current_index == 2:
            self.current_index = 0
        else:
            self.current_index += 1
