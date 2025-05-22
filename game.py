import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# Load Images
def load_and_scale(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)

background_img = load_and_scale("assets/background.jpg", (WIDTH, HEIGHT))
player_img = load_and_scale("assets/player.png", (100, 100))
chicken_img = load_and_scale("assets/chicken.png", (100, 100))
bullet_img = pygame.image.load("assets/bullet.png")
upgrade_item_img = load_and_scale("assets/star.png", (50, 50))

# Classes
class Player:
    def __init__(self):
        self.image = player_img
        self.x = WIDTH // 2
        self.y = HEIGHT - 70
        self.bullets = []
        self.bullet_level = 1
        self.lives = 3

    def update_by_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.image.get_width() // 2
        self.y = mouse_y - self.image.get_height() // 2

    def shoot(self):
        center_x = self.x + self.image.get_width() // 2
        top_y = self.y
        spread = 10

        for i in range(self.bullet_level):
            offset = (i - self.bullet_level // 2) * spread
            dx = offset // 10
            self.bullets.append(Bullet(center_x - bullet_img.get_width() // 2, top_y, dx=dx))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Bullet:
    def __init__(self, x, y, dx=0, dy=-10):
        self.image = bullet_img
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

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
        c_center = (self.x + self.image.get_width() // 2, self.y + self.image.get_height() // 2)
        b_center = (bullet.x + bullet.image.get_width() // 2, bullet.y + bullet.image.get_height() // 2)
        return math.hypot(c_center[0] - b_center[0], c_center[1] - b_center[1]) < 50

    def hits_player(self, player):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()).colliderect(
            pygame.Rect(player.x, player.y, player.image.get_width(), player.image.get_height())
        )


class UpgradeItem:
    def __init__(self):
        self.image = upgrade_item_img
        self.x = random.randint(50, WIDTH - 50)
        self.y = -50
        self.speed = 3

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def is_collected_by(self, player):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()).colliderect(
            pygame.Rect(player.x, player.y, player.image.get_width(), player.image.get_height())
        )


# Helper Functions
def show_start_screen():
    screen.blit(background_img, (0, 0))
    title = font.render("CHICKEN INVADERS", True, (255, 255, 255))
    prompt = font.render("Press SPACE to Start", True, (200, 200, 200))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()


def spawn_chickens(n):
    return [Chicken() for _ in range(n)]


# Game Loop
def game_loop():
    player = Player()
    chickens = spawn_chickens(5)
    upgrade_items = []
    item_timer = 0
    wave, score = 1, 0
    global mouse_pressed
    mouse_pressed = False

    running = True
    while running:
        screen.blit(background_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update_by_mouse()

        if pygame.mouse.get_pressed()[0] and not mouse_pressed:
            mouse_pressed = True
            player.shoot()
        elif not pygame.mouse.get_pressed()[0]:
            mouse_pressed = False

        for bullet in player.bullets:
            bullet.move()
        player.bullets = [b for b in player.bullets if b.y > 0]

        for chicken in chickens:
            chicken.move()

        item_timer += 1
        if item_timer > FPS * 10:
            upgrade_items.append(UpgradeItem())
            item_timer = 0

        for item in upgrade_items[:]:
            item.move()
            item.draw()
            if item.is_collected_by(player):
                player.bullet_level += 1
                upgrade_items.remove(item)
            elif item.y > HEIGHT:
                upgrade_items.remove(item)

        new_chickens = []
        for chicken in chickens:
            if chicken.hits_player(player):
                player.lives -= 1
                continue
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

        if player.lives <= 0:
            running = False

        if not chickens:
            wave += 1
            chickens = spawn_chickens(5 + wave - 1)

        player.draw()
        for bullet in player.bullets:
            bullet.draw()
        for chicken in chickens:
            chicken.draw()

        screen.blit(font.render(f"Wave: {wave}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 50))
        screen.blit(font.render(f"Lives: {player.lives}", True, (255, 100, 100)), (10, 90))

        pygame.display.update()
        clock.tick(FPS)


# Main
if __name__ == "__main__":
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
