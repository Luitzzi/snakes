class SnakeDrawer:
    def __init__(self, snake_logic):
        self.snake_logic = snake_logic
        self.sprites = gui_utils.load_spritesheet("")

    def draw():
        for i, segment in enumerate(snake_logic.body):
            
