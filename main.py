import pygame
import sys
import os
import random

#Initialize Pygame
pygame.init()

#Game Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
FPS = 60

#Colors
BLACK = (20, 20, 20)
WHITE = (240, 240, 240)
GRAY = (100, 100, 100)
HIGHLIGHT = (200, 50, 50)
GOLD = (255, 215, 0)
GREEN = (50, 200, 50)   #Color for Expand power-up
ORANGE = (255, 140, 0)  #Color for Speed power-up

#Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong (Pygame)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier", 32, bold=True)
menu_font = pygame.font.SysFont("Courier", 48, bold=True)
small_font = pygame.font.SysFont("Courier", 18)

#Game Objects
player_a = pygame.Rect(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player_b = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player_c = pygame.Rect(150, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player_d = pygame.Rect(WIDTH - 150 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

#Speeds & States
PADDLE_SPEED = 7
BALL_START_SPEED = 5
ball_speed_x = BALL_START_SPEED
ball_speed_y = BALL_START_SPEED
ai_speed = 5

state = "MENU"
game_mode = "1V1"
score_a = 0
score_b = 0
powerups_enabled = False

#Menus
main_menu = ["1. Play vs AI", "2. 1v1 Mode", "3. 4 Player Mode", "4. Power-Ups: [OFF]"]
ai_menu = ["Easy", "Medium", "Hard"]
selected_option = 0

#Power-Up Variables
powerup_box = None
powerup_type = None #"BIG" or "SPEED"
last_hit = None
powerup_timer = 0
SPAWN_INTERVAL = 7000 #7 seconds between spawns
BUFF_DURATION = 10000 #10 seconds for paddle buff
buff_end_times = {"A": 0, "B": 0, "C": 0, "D": 0}

#High Score System
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try: return int(f.read())
            except: return 0
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_high_score()

def reset_ball():
    global ball_speed_x, ball_speed_y, last_hit, powerup_box
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = BALL_START_SPEED if ball_speed_x < 0 else -BALL_START_SPEED
    ball_speed_y = BALL_START_SPEED if ball_speed_y > 0 else -BALL_START_SPEED
    last_hit = None
    powerup_box = None #Clear powerup on score

def reset_game():
    global score_a, score_b, powerup_timer
    score_a = 0
    score_b = 0
    player_a.height = player_b.height = player_c.height = player_d.height = PADDLE_HEIGHT
    player_a.centery = player_b.centery = player_c.centery = player_d.centery = HEIGHT // 2
    for key in buff_end_times:
        buff_end_times[key] = 0
    powerup_timer = pygame.time.get_ticks()
    reset_ball()

#Main Loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    
    #1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if state == "MENU":
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(main_menu)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(main_menu)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        state = "AI_MENU"
                        selected_option = 0
                    elif selected_option == 1:
                        game_mode = "1V1"
                        state = "PLAYING"
                        reset_game()
                    elif selected_option == 2:
                        game_mode = "4P"
                        state = "PLAYING"
                        reset_game()
                    elif selected_option == 3:
                        #Toggle Power-ups
                        powerups_enabled = not powerups_enabled
                        status = "[ON]" if powerups_enabled else "[OFF]"
                        main_menu[3] = f"4. Power-Ups: {status}"
                        
            elif state == "AI_MENU":
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(ai_menu)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(ai_menu)
                elif event.key == pygame.K_ESCAPE:
                    state = "MENU"
                    selected_option = 0
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0: ai_speed = 3
                    elif selected_option == 1: ai_speed = 5
                    elif selected_option == 2: ai_speed = 8.5
                    game_mode = "AI"
                    state = "PLAYING"
                    reset_game()

    #2. Menu Rendering
    if state == "MENU":
        screen.fill(BLACK)
        title = menu_font.render("PING PONG", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        for i, option in enumerate(main_menu):
            color = HIGHLIGHT if i == selected_option else WHITE
            if i == 3 and powerups_enabled and i != selected_option: color = GREEN
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 60))
            
        controls = small_font.render("Use UP/DOWN to navigate, ENTER to select", True, GRAY)
        screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 50))
        
    elif state == "AI_MENU":
        screen.fill(BLACK)
        title = menu_font.render("SELECT DIFFICULTY", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        for i, option in enumerate(ai_menu):
            color = HIGHLIGHT if i == selected_option else WHITE
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 60))
            
        esc_text = small_font.render("Press ESC to return to Main Menu", True, GRAY)
        screen.blit(esc_text, (WIDTH // 2 - esc_text.get_width() // 2, HEIGHT - 50))

    #3. Game Logic
    elif state == "PLAYING":
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            state = "MENU"
            selected_option = 0
        
        #Power-up Buff Expirations
        if current_time > buff_end_times["A"]: player_a.height = PADDLE_HEIGHT
        if current_time > buff_end_times["B"]: player_b.height = PADDLE_HEIGHT
        if current_time > buff_end_times["C"]: player_c.height = PADDLE_HEIGHT
        if current_time > buff_end_times["D"]: player_d.height = PADDLE_HEIGHT

        #Power-up Spawning Logic
        if powerups_enabled and powerup_box is None:
            if current_time - powerup_timer > SPAWN_INTERVAL:
                powerup_box = pygame.Rect(random.randint(250, 550), random.randint(100, 500), 25, 25)
                powerup_type = random.choice(["BIG", "SPEED"])
                powerup_timer = current_time

        #Power-up Collision Logic
        if powerups_enabled and powerup_box and ball.colliderect(powerup_box):
            if last_hit:
                if powerup_type == "BIG":
                    buff_end_times[last_hit] = current_time + BUFF_DURATION
                    if last_hit == "A": player_a.height = PADDLE_HEIGHT * 2
                    if last_hit == "B": player_b.height = PADDLE_HEIGHT * 2
                    if last_hit == "C": player_c.height = PADDLE_HEIGHT * 2
                    if last_hit == "D": player_d.height = PADDLE_HEIGHT * 2
                elif powerup_type == "SPEED":
                    ball_speed_x *= 1.5
                    ball_speed_y *= 1.5
            
            #Remove powerup and reset timer
            powerup_box = None
            powerup_timer = current_time

        #Movement Logic
        if keys[pygame.K_w] and player_a.top > 0: player_a.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player_a.bottom < HEIGHT: player_a.y += PADDLE_SPEED

        if game_mode == "AI":
            if player_b.centery < ball.centery and player_b.bottom < HEIGHT: player_b.y += ai_speed
            if player_b.centery > ball.centery and player_b.top > 0: player_b.y -= ai_speed
        else:
            if keys[pygame.K_UP] and player_b.top > 0: player_b.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and player_b.bottom < HEIGHT: player_b.y += PADDLE_SPEED

        if game_mode == "4P":
            if keys[pygame.K_r] and player_c.top > 0: player_c.y -= PADDLE_SPEED
            if keys[pygame.K_f] and player_c.bottom < HEIGHT: player_c.y += PADDLE_SPEED
            if keys[pygame.K_i] and player_d.top > 0: player_d.y -= PADDLE_SPEED
            if keys[pygame.K_k] and player_d.bottom < HEIGHT: player_d.y += PADDLE_SPEED

        #Ball Physics
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        #Paddle Collisions & Last Hit Tracking
        if ball.colliderect(player_a) and ball_speed_x < 0:
            ball.left = player_a.right
            ball_speed_x *= -1
            last_hit = "A"
        if ball.colliderect(player_b) and ball_speed_x > 0:
            ball.right = player_b.left
            ball_speed_x *= -1
            last_hit = "B"
            
        if game_mode == "4P":
            if ball.colliderect(player_c) and ball_speed_x < 0:
                ball.left = player_c.right
                ball_speed_x *= -1
                last_hit = "C"
            if ball.colliderect(player_d) and ball_speed_x > 0:
                ball.right = player_d.left
                ball_speed_x *= -1
                last_hit = "D"

        #Scoring Logic
        if ball.left <= 0:
            score_b += 1
            powerup_timer = current_time #Delay spawn after score
            reset_ball()
        elif ball.right >= WIDTH:
            score_a += 1
            if game_mode == "AI" and score_a > high_score:
                high_score = score_a
                save_high_score(high_score)
            powerup_timer = current_time #Delay spawn after score
            reset_ball()

        #Rendering
        screen.fill(BLACK)

        for y in range(0, HEIGHT, 30):
            pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 2, y, 4, 15))

        #Draw Power-Up Box
        if powerups_enabled and powerup_box:
            p_color = GREEN if powerup_type == "BIG" else ORANGE
            pygame.draw.rect(screen, p_color, powerup_box)
            #Draw a small symbol inside
            symbol = "+" if powerup_type == "BIG" else ">>"
            p_text = small_font.render(symbol, True, BLACK)
            screen.blit(p_text, (powerup_box.centerx - p_text.get_width()//2, powerup_box.centery - p_text.get_height()//2))

        #Draw Paddles and Ball
        pygame.draw.rect(screen, WHITE, player_a)
        pygame.draw.rect(screen, WHITE, player_b)
        if game_mode == "4P":
            pygame.draw.rect(screen, GRAY, player_c)
            pygame.draw.rect(screen, GRAY, player_d)
        pygame.draw.ellipse(screen, WHITE, ball)

        #Draw UI
        score_surface = font.render(f"{score_a}   {score_b}", True, WHITE)
        screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 20))
        esc_surface = small_font.render("Press ESC for Menu", True, GRAY)
        screen.blit(esc_surface, (10, 10))

        if game_mode == "AI":
            hs_surface = small_font.render(f"High Score: {high_score}", True, GOLD)
            screen.blit(hs_surface, (WIDTH - hs_surface.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()