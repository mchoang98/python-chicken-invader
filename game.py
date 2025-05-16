import pygame
import random
import math

# Khởi tạo pygame
pygame.init()

# Màn hình
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders")

# Load hình ảnh
background_img = pygame.image.load("assets/background.jpg")
# set background image size to screen size
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
player_img = pygame.image.load("assets/player.png")
chicken_img = pygame.image.load("assets/chicken.png")
# set chicken image size to 100x100
chicken_img = pygame.transform.scale(chicken_img, (100, 100))
bullet_img = pygame.image.load("assets/bullet.png")

# Font
font = pygame.font.SysFont("Arial", 28)

# Clock
clock = pygame.time.Clock()

# ----- CLASS ĐỊNH NGHĨA -----
class Player:
    def __init__(self):
        self.image = player_img
        self.x = WIDTH // 2
        self.y = HEIGHT - 70
        self.bullets = []

    def update_by_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.image.get_width() // 2
        self.y = mouse_y - self.image.get_height() // 2

    def shoot(self):
        bullet_x = self.x + self.image.get_width() // 2 - bullet_img.get_width() // 2
        bullet_y = self.y
        bullet = Bullet(bullet_x, bullet_y)
        self.bullets.append(bullet)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, x, y):
        self.image = bullet_img
        self.x = x
        self.y = y
        self.speed = 7

    def move(self):
        self.y -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Chicken:
    def __init__(self):
        self.image = chicken_img
        self.x = random.randint(50, WIDTH - 90)
        self.y = random.randint(30, 150)
        self.dx = random.choice([-1, 1]) * 2
        self.dy = 1

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x <= 0 or self.x >= WIDTH - self.image.get_width():
            self.dx *= -1
        if self.y > HEIGHT:
            self.y = -50
            self.x = random.randint(50, WIDTH - 90)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def is_hit(self, bullet):
        chicken_center_x = self.x + self.image.get_width() // 2
        chicken_center_y = self.y + self.image.get_height() // 2

        bullet_center_x = bullet.x + bullet.image.get_width() // 2
        bullet_center_y = bullet.y + bullet.image.get_height() // 2

        distance = math.hypot(chicken_center_x - bullet_center_x, chicken_center_y - bullet_center_y)
        return distance < 50  # 50 is the hit radius


# ----- GAME -----
def show_start_screen():
    screen.blit(background_img, (0, 0))
    title = font.render("CHICKEN INVADERS", True, (255, 255, 255))
    prompt = font.render("Press SPACE to Start", True, (200, 200, 200))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()

def game_loop():
    player = Player()
    chickens = []
    wave = 1
    score = 0
    chicken_count = 5

    def spawn_chickens(n):
        return [Chicken() for _ in range(n)]

    chickens = spawn_chickens(chicken_count)

    running = True
    while running:
        screen.blit(background_img, (0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Di chuyển + bắn
        player.update_by_mouse()
        # shoot by mouse button
        if pygame.mouse.get_pressed()[0]:
            player.shoot()

        # Cập nhật đạn
        for bullet in player.bullets:
            bullet.move()
        player.bullets = [b for b in player.bullets if b.y > 0]

        # Cập nhật gà
        for chicken in chickens:
            chicken.move()

        # Va chạm
        new_chickens = []
        for chicken in chickens:
            hit = False
            for bullet in player.bullets:
                if chicken.is_hit(bullet):
                    player.bullets.remove(bullet)
                    hit = True
                    score += 1
                    break
            if not hit:
                new_chickens.append(chicken)
        chickens = new_chickens

        # Vòng mới
        if not chickens:
            wave += 1
            chicken_count += 1
            chickens = spawn_chickens(chicken_count)

        # Vẽ
        player.draw()
        for bullet in player.bullets:
            bullet.draw()
        for chicken in chickens:
            chicken.draw()

        wave_text = font.render(f"Wave: {wave}", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(wave_text, (10, 10))
        screen.blit(score_text, (10, 50))

        pygame.display.update()
        clock.tick(60)

# ----- MAIN -----
showing_start = True
while showing_start:
    show_start_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            showing_start = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            showing_start = False
            game_loop()

pygame.quit()
