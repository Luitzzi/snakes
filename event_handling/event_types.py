class InputEvent:
    UP = "direction_north"
    RIGHT = "direction_east"
    DOWN = "direction_south"
    LEFT = "direction_west"

class EventType:
    GAME_QUIT = "game_quit"
    START_GAME = "start_game"
    INPUT_EVENT = InputEvent
