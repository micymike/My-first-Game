import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Initialize the mixer
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("Sia - Unstoppable (Official Video - Live from the Nostalgic For The Present Tour)-160.mp3")
pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely

# Initialize font module
pygame.font.init()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (50, 50, 50)
dark_gray = (40, 40, 40)

# Set display dimensions
display_width = 800
display_height = 600

# Set up the display
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Mike Racing Game')

# Road properties
road_width = 300
road_left_edge = (display_width - road_width) // 2
road_right_edge = road_left_edge + road_width

# Load and resize car image
car_img = pygame.image.load('car2.png')
car_img = pygame.transform.scale(car_img, (50, 100))  # Resize car image to 50x100 pixels
car_width = car_img.get_width()


# Load and resize background images
background_img = pygame.image.load('background.jpg')
background_img = pygame.transform.scale(background_img, (road_right_edge - road_left_edge, display_height))

# Road properties
road_width = 300
road_left_edge = (display_width - road_width) // 2
road_right_edge = road_left_edge + road_width

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
    text_rect.center = ((display_width / 2), (display_height / 2))
    game_display.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)

def crash(score):
    message_display('Oops!! You Crashed')
    time.sleep(2)
    game_display.fill(white)
    large_text = pygame.font.Font('freesansbold.ttf', 75)
    text_surf, text_rect = text_objects("Score: " + str(score), large_text)
    text_rect.center = ((display_width / 2), (display_height / 3))
    game_display.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)

# Function to create buttons
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(game_display, ic, (x, y, w, h))

    small_text = pygame.font.Font('freesansbold.ttf', 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(text_surf, text_rect)

# Function to pause the game
def paused():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 75)
        text_surf, text_rect = text_objects("Paused", large_text)
        text_rect.center = ((display_width / 2), (display_height / 3))
        game_display.blit(text_surf, text_rect)

        button("Continue", 150, 450, 150, 50, green, blue, unpause)
        button("Quit", 550, 450, 100, 50, red, blue, pygame.quit)

        pygame.display.update()

def unpause():
    global pause
    pause = False

# Start game function
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = text_objects("Car Racing", large_text)
        text_rect.center = ((display_width / 2), (display_height / 2))
        game_display.blit(text_surf, text_rect)

        button("Play", 350, 450, 100, 50, green, blue, game_loop)

        pygame.display.update()

# Main game loop
def game_loop():
    global pause
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0

    obs_startx = random.randrange(road_left_edge, road_right_edge - 100)
    obs_starty = -600
    obs_speed = 2
    obs_width = 50
    obs_height = 50

    score = 0

    # Scrolling road lines
    lane_line_height = 40
    lane_line_gap = 20
    lane_lines = []
    for i in range(0, display_height, lane_line_height + lane_line_gap):
        lane_lines.append(i)

    game_exit = False
    crashed = False

    while not game_exit:
        while crashed:
            game_display.fill(white)
            large_text = pygame.font.Font('freesansbold.ttf', 75)
            text_surf, text_rect = text_objects("Ooops!! You Crashed", large_text)
            text_rect.center = ((display_width / 2), (display_height / 3))
            game_display.blit(text_surf, text_rect)

            small_text = pygame.font.Font('freesansbold.ttf', 50)
            text_surf, text_rect = text_objects("Score: " + str(score), small_text)
            text_rect.center = ((display_width / 2), (display_height / 2))
            game_display.blit(text_surf, text_rect)

            button("Play Again", 150, 450, 150, 50, green, blue, game_loop)
            button("Quit", 550, 450, 100, 50, red, blue, pygame.quit)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Adjust the boundary based on the road edges
                    if x > road_left_edge:
                        x_change = -1
                if event.key == pygame.K_RIGHT:
                    # Adjust the boundary based on the road edges
                    if x + car_width < road_right_edge:
                        x_change = 1
                if event.key == pygame.K_p:
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        game_display.fill(white)

        # Draw background images
        game_display.blit(background_img, (0, 0))  # Left side background
        game_display.blit(background_img, (road_right_edge, 0))  # Right side background

        # Draw road
        pygame.draw.rect(game_display, gray, [road_left_edge, 0, road_width, display_height])
        pygame.draw.line(game_display, white, (road_left_edge, 0), (road_left_edge, display_height), 5)
        pygame.draw.line(game_display, white, (road_right_edge, 0), (road_right_edge, display_height), 5)

        # Draw scrolling lane lines
        for i in range(len(lane_lines)):
            lane_lines[i] += obs_speed
            if lane_lines[i] > display_height:
                lane_lines[i] = -lane_line_height
            pygame.draw.line(game_display, white, (display_width // 2, lane_lines[i]), (display_width // 2, lane_lines[i] + lane_line_height), 5)

        obstacles(obs_startx, obs_starty, obs_width, obs_height, black)
        obs_starty += obs_speed
        car(x, y)

        if obs_starty > display_height:
            obs_starty = 0 - obs_height
            obs_startx = random.randrange(road_left_edge, road_right_edge - 100)
            score += 1  # Increase score when an obstacle is avoided
            obs_speed += 0.1

        if y < obs_starty + obs_height:
            if x > obs_startx and x < obs_startx + obs_width or x + car_width > obs_startx and x + car_width < obs_startx + obs_width:
                crashed = True

        # Display score
        font = pygame.font.SysFont(None, 35)
        score_text = font.render("Score: " + str(score), True, white)
        game_display.blit(score_text, (10, 10))

        # Display Pause button
        button("Pause", 700, 10, 80, 30, blue, green, paused)

        pygame.display.update()

# Start the game
game_intro()
pygame.quit()
quit()
