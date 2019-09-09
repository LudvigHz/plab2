from rock_paper_scissors import actionTypes


class Action:
    def __init__(self, action):
        if action not in [actionTypes.PAPER, actionTypes.ROCK, actionTypes.SCISSORS]:
            raise Exception("Illegal argument, action must be one of actionTypes")
        self.action = action

    def __str__(self):
        return self.action

    def __eq__(self, o):
        return self.action == o.action

    def __gt__(self, o):
        if self.action == actionTypes.PAPER:
            return o.action == actionTypes.ROCK
        elif self.action == actionTypes.ROCK:
            return o.action == actionTypes.SCISSORS
        else:
            return o.action == actionTypes.PAPER
