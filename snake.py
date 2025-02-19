import pygame
import random

# General settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
WIDTH = 116
HEIGHT = 12
TILE_SIZE = int(min(SCREEN_WIDTH / WIDTH, SCREEN_HEIGHT / HEIGHT))
OFFSET_X = int((SCREEN_WIDTH - WIDTH * TILE_SIZE) / 2)
OFFSET_Y = int((SCREEN_HEIGHT - HEIGHT * TILE_SIZE) / 2)
FIELD_RECT = pygame.Rect(OFFSET_X, OFFSET_Y, WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE)

# Colors
SNAKE_COLOR = (50, 100, 150)
FOOD_COLOR = (200, 60, 40)
FIELD_COLOR = (200, 220, 150)
INTRO_BG_COLOR = (50, 50, 70)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# Snake
snake = [(2, 2), (2, 3)]
direction = (1, 0)


# GUI
def n_x(x):
    return OFFSET_X + x


def n_y(y):
    return OFFSET_Y + y


def draw_tile(x, y, color):
    draw_rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, color)


def draw_rect(x, y, w, h, color):
    rect = pygame.Rect(x + OFFSET_X, y + OFFSET_Y, w, h)
    pygame.draw.rect(screen, color, rect)


# Food
def spawn_food():
    return (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))


food = spawn_food()

# Game logic
running = True
while running:
    screen.fill(INTRO_BG_COLOR)
    pygame.draw.rect(screen, FIELD_COLOR, FIELD_RECT)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                snake.change_direction((1, 0))

    # Move snake
    """
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    if (
        new_head in snake
        or new_head[0] < 0
        or new_head[0] >= WIDTH
        or new_head[1] < 0
        or new_head[1] >= WIDTH
    ):
        running = False
        pass

    if new_head == food:
        spawn_food()
    else:
        snake.pop()

    """

    draw_tile(1, 1, SNAKE_COLOR)
    draw_tile(4, 4, FOOD_COLOR)
    # snake.insert(0, new_head)

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
