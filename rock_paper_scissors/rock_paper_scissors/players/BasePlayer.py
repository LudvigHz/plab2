import matplotlib.pyplot as plt
import numpy as np

from rock_paper_scissors import actionTypes
from rock_paper_scissors.Action import Action


class BasePlayer:
    """
    Base class for a player.
    """

    def __init__(self):
        self.action_history = []
        self.game_history = []
        self.last_action = None

    def get_name(self):
        """Returns name of the player."""
        return self.__str__()

    def choose_action(self, action):
        """Chooses the action specified from arg action"""
        self.last_action = Action(action)
        self.action_history.append(self.last_action)

    def calculate_result(self, own_action, opponent_action):
        """Calculates the result of a game, based on the actions"""
        if own_action > opponent_action:
            return 2
        elif own_action == opponent_action:
            return 1
        else:
            return 0

    def choose_opposite_action(self, action):
        """Same as choose_action but chooses the opposite (beating) action"""
        if action == actionTypes.ROCK:
            opposite = actionTypes.PAPER
        elif action == actionTypes.PAPER:
            opposite = actionTypes.SCISSORS
        else:
            opposite = actionTypes.ROCK
        self.last_action = Action(opposite)
        self.action_history.append(self.last_action)

    def receive_result(self, player):
        """Receive the result and save it to players history"""
        hist_object = {
            "player_move": self.last_action,
            "opponent_move": player.last_action,
            "opponent": player,
            "result": self.calculate_result(self.last_action, player.last_action),
        }
        self.game_history.append(hist_object)

    def get_all_results(self):
        """Returns a dict with win/loss/tie statistics for the player"""
        wins = list(
            filter(
                lambda a: a is not None,
                [r["result"] if r["result"] == 2 else None for r in self.game_history],
            )
        )
        ties = list(
            filter(
                lambda a: a is not None,
                [r["result"] if r["result"] == 1 else None for r in self.game_history],
            )
        )
        losses = list(
            filter(
                lambda a: a is not None,
                [r["result"] if r["result"] == 0 else None for r in self.game_history],
            )
        )

        return {"wins": len(wins), "ties": len(ties), "losses": len(losses)}

    def create_plot(self):
        """Create a plot showing evolution of the average score"""
        results = [item["result"] for item in self.game_history]
        avg_results = []
        for i in range(1, len(results)):
            avg_results.append(np.mean(results[:i]))

        num_games = range(1, len(self.game_history))
        plt.figure()
        plt.title(self.__str__() + " results")
        plt.xlabel("Number of games")
        plt.ylabel("Score")
        plt.ylim((0, 2))
        plt.plot(num_games, avg_results)
        plt.show()
