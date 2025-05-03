import pygame
import time
import random
import os

# Initialize Pygame
pygame.init()

# Load resources
BACKGROUND_IMG = pygame.image.load("C:\\PROJECTS GITHUB\\Snake gane\\background.jpg")
EAT_SOUND = pygame.mixer.Sound("C:\\PROJECTS GITHUB\\Snake gane\\Eatind sound effect.wav")

# Game window
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 60)

# Clock
clock = pygame.time.Clock()

# Best scores
BEST_SCORES = {'Easy': 0, 'Medium': 0, 'Hard': 0}

# Difficulty settings
DIFFICULTY_SPEED = {'Easy': 10, 'Medium': 15, 'Hard': 25}

def draw_snake(snake_list, direction, CELL_SIZE):
    for i, pos in enumerate(snake_list):
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        
        if i == 0:  # Drawing eyes on the head
            if direction == "UP":
                eyes = [(pos[0]+4, pos[1]+4), (pos[0]+16, pos[1]+4)]
            elif direction == "DOWN":
                eyes = [(pos[0]+4, pos[1]+16), (pos[0]+16, pos[1]+16)]
            elif direction == "LEFT":
                eyes = [(pos[0]+4, pos[1]+4), (pos[0]+4, pos[1]+16)]
            elif direction == "RIGHT":
                eyes = [(pos[0]+16, pos[1]+4), (pos[0]+16, pos[1]+16)]
            for eye in eyes:
                pygame.draw.circle(screen, BLACK, eye, 3)

def message_center(text, color, y_offset=0, big=False):
    msg = big_font.render(text, True, color) if big else font.render(text, True, color)
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(msg, rect)

def show_score(score, best, difficulty):
    score_text = font.render(f"Score: {score}    Best ({difficulty}): {best}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_loop(difficulty):
    global BEST_SCORES

    x, y = WIDTH//2, HEIGHT//2
    dx, dy = 0, 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - CELL_SIZE) / 20.0) * 20.0
    food_y = round(random.randrange(0, HEIGHT - CELL_SIZE) / 20.0) * 20.0

    score = 0
    glow_frames = 0

    speed = DIFFICULTY_SPEED[difficulty]

    game_exit = False
    game_over = False
    direction = "UP"

    while not game_exit:
        while game_over:
            screen.blit(BACKGROUND_IMG, (0, 0))
            message_center("Game Over", RED, -40, big=True)
            message_center("Press Enter to Play Again or Q to Quit", WHITE, 20)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_RETURN:
                        game_loop(difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL_SIZE, 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL_SIZE, 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL_SIZE
                    direction = "UP"
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL_SIZE
                    direction = "DOWN"

        x += dx
        y += dy

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_over = True

        screen.blit(BACKGROUND_IMG, (0, 0))

        if glow_frames > 0:
            pygame.draw.rect(screen, YELLOW, [food_x, food_y, CELL_SIZE, CELL_SIZE])
            glow_frames -= 1
        else:
            pygame.draw.rect(screen, RED, [food_x, food_y, CELL_SIZE, CELL_SIZE])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True

        draw_snake(snake_list, direction, CELL_SIZE)
        show_score(score, BEST_SCORES[difficulty], difficulty)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - CELL_SIZE) / 20.0) * 20.0
            food_y = round(random.randrange(0, HEIGHT - CELL_SIZE) / 20.0) * 20.0
            snake_length += 1
            score += 1
            glow_frames = 5
            EAT_SOUND.play()

        if score > BEST_SCORES[difficulty]:
            BEST_SCORES[difficulty] = score

        clock.tick(speed)

    pygame.quit()
    quit()

def main_menu():
    selected = 0
    options = ['Easy', 'Medium', 'Hard']

    while True:
        screen.blit(BACKGROUND_IMG, (0, 0))
        message_center("SNAKE GAME", GREEN, -100, big=True)

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            message_center(option, color, -30 + i * 40)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    game_loop(options[selected])

main_menu()
