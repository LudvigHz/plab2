from rock_paper_scissors import actionTypes
from rock_paper_scissors.players.BasePlayer import BasePlayer


class MostNormal(BasePlayer):
    """
    Player that chooses actions based on opponents history.
    Chooses the opposite of the opponents most chosen action.
    """

    def __str__(self):
        return "Most normal"

    def choose_action(self, opponent):
        action_count = {
            actionTypes.ROCK: 0,
            actionTypes.PAPER: 0,
            actionTypes.SCISSORS: 0,
        }
        for action in opponent.action_history:
            action_count[action.action] += 1
        most_normal_action = sorted(
            action_count.items(), key=lambda kv: (kv[1], kv[0]), reverse=True
        )[0][0]

        super().choose_opposite_action(most_normal_action)
        return most_normal_action
