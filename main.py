import pygame
import random
import sys
import webbrowser

# --- Init ---
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DVD Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 36)
small_font = pygame.font.SysFont("Consolas", 24)

# --- Load Assets ---
logo_img = pygame.image.load("dvd_logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_img, (100, 50))

hit_sound = pygame.mixer.Sound("hit.wav")
wall_sound = pygame.mixer.Sound("wall.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

def random_color():
    return (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255))

def tint_image(image, tint_color):
    tinted = image.copy()
    tint = pygame.Surface(tinted.get_size()).convert_alpha()
    tint.fill(tint_color + (0,))
    tinted.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    return tinted

# --- Game Variables ---
logo_color = random_color()
logo_rect = logo_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
logo_dx = 4 * random.choice([-1, 1])
logo_dy = 4 * random.choice([-1, 1])
score = 0

PADDLE_W, PADDLE_H = 12, 120
left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
right_paddle = pygame.Rect(WIDTH - 42, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
paddle_speed = 6

game_over = False

def reset():
    global logo_rect, logo_dx, logo_dy, logo_color, score, game_over
    logo_rect.x = WIDTH // 2
    logo_rect.y = HEIGHT // 2
    logo_dx = 4 * random.choice([-1, 1])
    logo_dy = 4 * random.choice([-1, 1])
    logo_color = random_color()
    score = 0
    game_over = False

# --- Main Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.KEYDOWN:
            reset()

    keys = pygame.key.get_pressed()

    if not game_over:
        # Controls
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            left_paddle.y += paddle_speed

        # Right paddle AI
        if logo_rect.centery < right_paddle.centery:
            right_paddle.y -= paddle_speed
        elif logo_rect.centery > right_paddle.centery:
            right_paddle.y += paddle_speed

        left_paddle.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        right_paddle.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        # Move logo
        logo_rect.x += logo_dx
        logo_rect.y += logo_dy

        # Top/bottom bounce
        if logo_rect.top <= 0 or logo_rect.bottom >= HEIGHT:
            logo_dy *= -1
            logo_color = random_color()
            wall_sound.play()

        # Paddle bounce
        if logo_rect.colliderect(left_paddle) and logo_dx < 0:
            logo_dx *= -1
            logo_color = random_color()
            hit_sound.play()
            score += 1

        if logo_rect.colliderect(right_paddle) and logo_dx > 0:
            logo_dx *= -1
            logo_color = random_color()
            hit_sound.play()

        # Miss = game over
        if logo_rect.left <= 0:
            game_over = True
            gameover_sound.play()

    # --- Draw ---
    win.fill((0, 0, 0))

    pygame.draw.rect(win, (255, 255, 255), left_paddle)
    pygame.draw.rect(win, (255, 255, 255), right_paddle)

    tinted_logo = tint_image(logo_img, logo_color)
    win.blit(tinted_logo, logo_rect)

    score_text = font.render(f"Score: {score}", True, (200, 200, 255))
    win.blit(score_text, (20, 20))

    if game_over:
        # Game over text
        msg = font.render("GAME OVER - Press any key", True, (255, 80, 80))
        win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))

        # About info at bottom
        about_lines = [
            "Created by Kelsi Davis",
            "Website: geekastro.dev",
            "GitHub: github.com/Kelsidavis"
        ]
        for i, line in enumerate(about_lines):
            about_text = small_font.render(line, True, (160, 160, 255))
            win.blit(about_text, (WIDTH // 2 - about_text.get_width() // 2, HEIGHT - 90 + i * 25))

    pygame.display.update()
    clock.tick(60)
