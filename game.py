import pygame
import random
import math

pygame.init()

# Màn hình game
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Chicken Invaders - Resize + Respawn")
clock = pygame.time.Clock()  # ⬅️ Add this

# Hình nền
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (800, 600))  # Resize to 800x600

# Player
player_img = pygame.image.load("assets/player.png")
player_y = 480

# Đạn
bullet_img = pygame.image.load("assets/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"

# Gà
chicken_img = []
chicken_x = []
chicken_y = []
chicken_x_change = []
chicken_y_change = []
num_of_chickens = 6

for i in range(num_of_chickens):
    original = pygame.image.load("assets/chicken.png")
    resized = pygame.transform.scale(original, (64, 64))  # Resize to 64x64
    chicken_img.append(resized)
    chicken_x.append(random.randint(0, 735))
    chicken_y.append(random.randint(50, 150))
    chicken_x_change.append(4)
    chicken_y_change.append(40)

# Score
score = 0
font = pygame.font.Font(None, 36)

def show_score():
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def player(x):
    screen.blit(player_img, (x, player_y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    bullet_center_x = x + player_img.get_width() // 2 - bullet_img.get_width() // 2
    screen.blit(bullet_img, (bullet_center_x, y))

def is_collision(ch_x, ch_y, blt_x, blt_y):
    distance = math.hypot(ch_x - blt_x, ch_y - blt_y)
    return distance < 27

# Game loop
running = True
player_x = 370

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Lấy vị trí chuột
    mouse_x, _ = pygame.mouse.get_pos()
    player_x = mouse_x - 32  # Căn giữa tàu

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Click chuột trái bắn
        if event.type == pygame.MOUSEBUTTONDOWN and bullet_state == "ready":
            bullet_x = player_x
            fire_bullet(bullet_x, bullet_y)

    # Đạn bay
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

    # Gà
    for i in range(num_of_chickens):
        chicken_x[i] += chicken_x_change[i]
        chicken_y[i] += int(5 * math.sin(pygame.time.get_ticks() * 0.005 + i))  # Wave effect
        if chicken_x[i] <= 0 or chicken_x[i] >= 736:
            chicken_x_change[i] *= -1


        # Va chạm
        if is_collision(chicken_x[i], chicken_y[i], bullet_x, bullet_y):
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            # Respawn ở vị trí mới
            chicken_x[i] = random.randint(0, 735)
            chicken_y[i] = random.randint(50, 150)

        screen.blit(chicken_img[i], (chicken_x[i], chicken_y[i]))

    player(player_x)
    show_score()
    pygame.display.update()
    clock.tick(100)  # ⬅️ Limit game to 30 FPS (you can lower to 20 or 15 if you want slower)

