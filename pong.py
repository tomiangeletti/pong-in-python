import pygame
import sys
import random
import os

def ball_movement():
    global ball_speed_x, ball_speed_y, player_points, opponent_points, pong_sound, score_sound

    # Movement of the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y  

    # Ball collisions (if the ball collise with any border, we inverse it velocity)
    if ball.top  <= 0 or ball.bottom >= SCREEN_HEIGHT:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    # Check if its a goal!
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_points += 1
        ball_restart()
    if ball.right >= SCREEN_WIDTH:
        pygame.mixer.Sound.play(score_sound)
        opponent_points += 1
        ball_restart()

    # Collisions between rectangle and ball
    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
        pygame.mixer.Sound.play(pong_sound)

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
        pygame.mixer.Sound.play(pong_sound)
    
    

def player_animations():
    # The player rectangle cannot get out of the limits of the screen
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom  >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

def opponent_animations():
    # This is like an AI opponent (a like, yes.)
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom  >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH / 2, random.randint(100, SCREEN_HEIGHT - 100))
    ball_speed_x *= random.choice((1,-1))
    ball_speed_y *= random.choice((1,-1))

def restart_game():
    global player_points, opponent_points, ball_speed_x, ball_speed_y
    global ball, player, opponent, player_speed

    # Set default values.
    player_points = 0
    opponent_points = 0
    ball_speed_x = 7
    ball_speed_y = 7
    player_speed = 0
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.centery = (SCREEN_HEIGHT / 2)
    opponent.centery = (SCREEN_HEIGHT / 2)

def draw_menu():
    """This function draws the menu texts"""
    # Game title
    tittle = font_large.render("Pong", True, white)
    tittle_rect = tittle.get_rect(center=(SCREEN_WIDTH / 2, 150))
    screen.blit(tittle, tittle_rect)

    # Instructions
    instruction = font_medium.render("Presiona ESPACIO para jugar", True, white)
    instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH / 2, 350))
    screen.blit(instruction, instruction_rect)

    # Controls
    controls = font_medium.render("↑/↓ para mover las paletas", True, white)
    controls_rect = controls.get_rect(center=(SCREEN_WIDTH / 2, 450))
    screen.blit(controls, controls_rect)

def draw_game_over():
    global winner
    if winner == 'player':
        text = font_large.render("VICTORIA!", True, white)
    elif winner == 'opponent':
        text = font_large.render("DERROTA!", True, white)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 200))
    screen.blit(text, text_rect)

    # Options after game
    option1 = font_small.render("Presiona R para REVANCHA", True, white)
    option1_rect = option1.get_rect(center=(SCREEN_WIDTH/2, 450))
    screen.blit(option1, option1_rect)
    
    option2 = font_small.render("Presiona ESPACIO para MENÚ", True, white)
    option2_rect = option2.get_rect(center=(SCREEN_WIDTH/2, 500))
    screen.blit(option2, option2_rect)

def draw_game():
    pygame.draw.rect(screen, white, player)
    pygame.draw.rect(screen, white, opponent)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, white, (SCREEN_WIDTH/2,0), (SCREEN_WIDTH/2,SCREEN_HEIGHT))
    screen.blit(opponent_surface, (80, 20))
    screen.blit(player_surface, (660, 20))


# I dont remember this... sorry.
os.chdir(os.path.dirname(__file__))

# General setup
pygame.mixer.pre_init(44100,-16,2,512) # Parching the sound's delay
pygame.init()
clock = pygame.time.Clock()



# Main window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Icon

icon = pygame.image.load('assets/icon.png').convert_alpha()
pygame.display.set_icon(icon)

pygame.display.set_caption("Pong!")
pygame.mouse.set_visible(False)

# Definign rectangles. (Initial positions and the dimensions of the rectangle (30x30))
ball = pygame.Rect(SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT / 2 - 15, 30, 30)
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2 - 70, 10, 140)
opponent = pygame.Rect(10, SCREEN_HEIGHT /2 - 70, 10, 140)
white = (255,255,255)
bg_color = pygame.Color('grey12')

ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 9

player_points = 0
opponent_points = 0
POINTS_TO_WIN = 10

game_status = 'menu'
winner = ""

# Texts
font_type = pygame.font.SysFont("Verdana", 60)
font_large = pygame.font.SysFont("Verdana", 80, bold=True)
font_medium = pygame.font.SysFont("Verdana", 40)
font_small = pygame.font.SysFont("Verdana", 24)

# Sounds
pong_sound = pygame.mixer.Sound('sounds/pong.mp3')
score_sound = pygame.mixer.Sound('sounds/score.mp3')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_status == 'menu':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_game()
                    game_status = 'playing'
        elif game_status == 'playing':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7
            if player_points >= POINTS_TO_WIN:
                winner = 'player'
                game_status = 'game over'
            elif opponent_points >= POINTS_TO_WIN:
                winner = 'opponent'
                game_status = 'game over'
        elif game_status == 'game over':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_status = "menu"
                elif event.key == pygame.K_r:
                    restart_game()
                    game_status = "playing"
    if game_status == 'playing':
        ball_movement()
        player_animations()
        opponent_animations()
        player_surface = font_type.render(str(player_points), True, white)
        opponent_surface = font_type.render(str(opponent_points), True, white)
    
    screen.fill(bg_color)

    if game_status == 'playing':
        draw_game()
    elif game_status == 'menu':
        draw_menu()
    elif game_status == 'game over':
        draw_game_over()
    
    # Updating the window
    pygame.display.flip()
    clock.tick(60)