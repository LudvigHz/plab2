import random

from rock_paper_scissors import Action, actionTypes, players


class Random(players.BasePlayer):
    """
    Player which chooses actions randomly.
    """

    def __str__(self):
        return "Random"

    def choose_action(self, opponent):
        action = [actionTypes.PAPER, actionTypes.PAPER, actionTypes.SCISSORS][
            random.randint(0, 2)
        ]

        super().choose_action(action)
        return action
