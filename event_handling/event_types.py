from defs import Direction

class Event:
    """
    Base class for all events.
    """

class GameQuitEvent(Event):
    """
    Event triggered to quit the game.
    """

class StartGameEvent(Event):
    """
    Event triggered to start a Playable instance.
    """

class MovementEvent(Event):
    """
    Event triggered when a user inputs a movement action.
    Contains the new direction resulting from the input.
    """
    action: Direction

    def __init__(self, action: Direction):
        self.action = action
