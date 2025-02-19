import random

import pygame

WIDTH, HEIGHT = 600, 400
SEGMENT_SIZE = 20
FPS = 10
FOOD_SPAWN_TIME = 3000

# Colors
SNAKE_COLOR = (0,255,0)
FOOD_COLOR = (255,0,0)
BG_COLOR = (0,0,0)
INTRO_BG_COLOR = (50,50,50)

# Init pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = (SEGMENT_SIZE, 0)
        self.grow = False

    def move(self):
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        # Check collision with walls or itself
        if new_head in self.body or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            return False
        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()  # Remove last segment unless eating food
        else:
            self.grow = False  # Reset growth flag
        return True

    def change_direction(self, new_direction):
        """ Prevent reversing direction """
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def eat_food(self):
        self.grow = True  # Signal that snake should grow on the next move

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, SNAKE_COLOR, (*segment, SEGMENT_SIZE, SEGMENT_SIZE))

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randrange(0, WIDTH, SEGMENT_SIZE), random.randrange(0, HEIGHT, SEGMENT_SIZE))

    def respawn(self):
        self.position = self.random_position()

    def draw(self, screen):
        pygame.draw.rect(screen, FOOD_COLOR, (*self.position, SEGMENT_SIZE, SEGMENT_SIZE))

# Timer
foodSpawner = pygame.USEREVENT + 1
pygame.time.set_timer(foodSpawner,2000)

# Game logic
def moveElements:
    # Snake movement
    if not snake.move():
        running = False

    # Check if snake eats food
    for food in foods[:]:
        if snake.body[0] == food.position:
            snake.eat_food()
            foods.remove(food)

def drawElements:
    snake.draw(screen)
    for food in foods:
        food.draw(screen)

# Game loop
snake = Snake()
foods = [Food()]

running = True
gameActive = False
while running:
    screen.fill(BG_COLOR)

    # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif gameActive:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -SEGMENT_SIZE))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, SEGMENT_SIZE))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-SEGMENT_SIZE, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((SEGMENT_SIZE, 0))
                if event.type == foodSpawner:
                    if len(foods) < 3:
                        foods.append(Food())
            else:
                if game.type == pygame and

    if gameActive:
        moveElements()
        drawElements()
    else:
        screen.fill(INTRO_BG_COLOR)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()




