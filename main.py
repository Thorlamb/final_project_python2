import pygame
import sys

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
FPS = 60

# Colors
BLACK = (20, 20, 20)
WHITE = (240, 240, 240)
GRAY = (70, 70, 70)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong (Pygame)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier", 32, bold=True)

# Game Objects
player_a = pygame.Rect(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player_b = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Speeds
PADDLE_SPEED = 7
ball_speed_x = 5
ball_speed_y = 5

# Scores
score_a = 0
score_b = 0

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1  # Serve to the scorer

# Main Loop
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Input Handling
    keys = pygame.key.get_pressed()
    
    # Player A (W/S)
    if keys[pygame.K_w] and player_a.top > 0:
        player_a.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_a.bottom < HEIGHT:
        player_a.y += PADDLE_SPEED

    # Player B (Up/Down)
    if keys[pygame.K_UP] and player_b.top > 0:
        player_b.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_b.bottom < HEIGHT:
        player_b.y += PADDLE_SPEED

    # 3. Ball Physics & Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Top/Bottom boundary bounce
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Paddle collisions
    if ball.colliderect(player_a) and ball_speed_x < 0:
        ball.left = player_a.right
        ball_speed_x *= -1

    if ball.colliderect(player_b) and ball_speed_x > 0:
        ball.right = player_b.left
        ball_speed_x *= -1

    # Scoring
    if ball.left <= 0:
        score_b += 1
        reset_ball()
    elif ball.right >= WIDTH:
        score_a += 1
        reset_ball()

    # 4. Rendering
    screen.fill(BLACK)

    # Center dashed line
    for y in range(0, HEIGHT, 30):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 2, y, 4, 15))

    # Draw game objects
    pygame.draw.rect(screen, WHITE, player_a)
    pygame.draw.rect(screen, WHITE, player_b)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw scores
    score_surface = font.render(f"{score_a}   {score_b}", True, WHITE)
    screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 20))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()