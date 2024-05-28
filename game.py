import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Set display dimensions
display_width = 800
display_height = 600

# Set up the display
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Car Racing Game')

# Load car image
car_img = pygame.image.load('car.png')
car_width = car_img.get_width()

# Function to display car
def car(x, y):
    game_display.blit(car_img, (x, y))

# Function to display obstacles
def obstacles(obs_x, obs_y, obs_w, obs_h, color):
    pygame.draw.rect(game_display, color, [obs_x, obs_y, obs_w, obs_h])

# Function to display text on screen
def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((display_width/2), (display_height/2))
    game_display.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def crash():
    message_display('You Crashed')

# Main game loop
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0

    obs_startx = random.randrange(0, display_width)
    obs_starty = -600
    obs_speed = 7
    obs_width = 100
    obs_height = 100

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        game_display.fill(white)

        obstacles(obs_startx, obs_starty, obs_width, obs_height, black)
        obs_starty += obs_speed
        car(x, y)

        if x > display_width - car_width or x < 0:
            crash()

        if obs_starty > display_height:
            obs_starty = 0 - obs_height
            obs_startx = random.randrange(0, display_width)

        if y < obs_starty + obs_height:
            if x > obs_startx and x < obs_startx + obs_width or x + car_width > obs_startx and x + car_width < obs_startx + obs_width:
                crash()

        pygame.display.update()

# Start the game
game_loop()
pygame.quit()
quit()
