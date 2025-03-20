from enum import Enum

class AgentAction(Enum):
    turn_left = [1, 0, 0]
    turn_right = [0, 0, 1]
    stay_straight = [0, 1, 0]
