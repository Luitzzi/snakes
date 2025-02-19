import pygame
import random

# General settings
WIDTH = 8
HEIGHT = 8
SEGMENT_SIZE = 1
FPS = 10

# Colors
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BG_COLOR = (0, 0, 0)
INTRO_BG_COLOR = (50, 50, 50)

# Init pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# Snake
snake = [(2, 2), (2, 3)]
direction = (SEGMENT_SIZE, 0)


# Food
def spawn_food():
    return (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))


food = spawn_food()

# Game logic
running = True
while running:
    screen.fill(BG_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, SEGMENT_SIZE):
                snake.change_direction((0, -SEGMENT_SIZE))
            elif event.key == pygame.K_DOWN and direction != (0, -SEGMENT_SIZE):
                snake.change_direction((0, SEGMENT_SIZE))
            elif event.key == pygame.K_LEFT and direction != (SEGMENT_SIZE, 0):
                snake.change_direction((-SEGMENT_SIZE, 0))
            elif event.key == pygame.K_RIGHT and direction != (-SEGMENT_SIZE, 0):
                snake.change_direction((SEGMENT_SIZE, 0))

    # Move snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    if (
        new_head in snake
        or new_head[0] < 0
        or new_head[0] >= WIDTH
        or new_head[1] < 0
        or new_head[1] >= WIDTH
    ):
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        spawn_food()
    else:
        snake.pop()

pygame.quit()
