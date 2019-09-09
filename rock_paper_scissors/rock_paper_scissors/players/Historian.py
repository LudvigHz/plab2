import random

from rock_paper_scissors.Action import Action
from rock_paper_scissors.players.BasePlayer import BasePlayer

from .. import actionTypes


class Historian(BasePlayer):
    def __init__(self, memory):
        super().__init__()
        self.memory = memory

    def __str__(self):
        return "Historian"

    def choose_action(self, opponent):
        next_action = [actionTypes.PAPER, actionTypes.ROCK, actionTypes.SCISSORS][
            random.randint(0, 2)
        ]

        action_count = {
            actionTypes.ROCK: 0,
            actionTypes.PAPER: 0,
            actionTypes.SCISSORS: 0,
        }
        if len(opponent.action_history) > self.memory:
            sub_sequence = opponent.action_history[-self.memory :]
            for i in range(len(opponent.action_history[: -self.memory])):
                if opponent.action_history[i : i + self.memory] == sub_sequence:
                    action_count[opponent.action_history[i + self.memory].action] += 1

            next_action = sorted(
                action_count.items(), key=lambda kv: (kv[1], kv[0]), reverse=True
            )[0][0]

        super().choose_opposite_action(next_action)
