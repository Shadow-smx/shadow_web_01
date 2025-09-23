import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders Extreme")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font('freesansbold.ttf', 24)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

# --- Game Assets (Placeholders - Replace with actual images) ---
# For a real game, you'd load actual images for these.
# For now, we'll draw simple shapes or use text.

# Player image (placeholder)
player_img = pygame.Surface((50, 50))
player_img.fill(BLUE) # Blue square for player
pygame.draw.polygon(player_img, WHITE, [(25, 0), (0, 50), (50, 50)]) # Simple triangle for player

# Invader images (placeholders for different types)
invader_imgs = {
    "basic": pygame.Surface((40, 40)),
    "fast": pygame.Surface((40, 40)),
    "tough": pygame.Surface((40, 40)),
    "boss": pygame.Surface((80, 80)) # Larger for boss
}
invader_imgs["basic"].fill(GREEN)
invader_imgs["fast"].fill(RED)
invader_imgs["tough"].fill(PURPLE)
invader_imgs["boss"].fill(ORANGE)

# Bullet image (placeholder)
bullet_img = pygame.Surface((10, 20))
bullet_img.fill(YELLOW)

# Power-up images (placeholders)
powerup_imgs = {
    "wideshot": pygame.Surface((20, 20)),
    "laser": pygame.Surface((20, 20)),
    "shield": pygame.Surface((20, 20)),
    "fever": pygame.Surface((20, 20))
}
powerup_imgs["wideshot"].fill(ORANGE)
powerup_imgs["laser"].fill(RED)
powerup_imgs["shield"].fill(BLUE)
powerup_imgs["fever"].fill(YELLOW)

# --- Game Classes ---

class Player:
    def __init__(self):
        self.image = player_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.x_change = 0
        self.speed = 5
        self.lives = 3
        self.power_up_type = "normal" # normal, wideshot, laser, shield
        self.power_up_timer = 0
        self.power_up_duration = 300 # 5 seconds at 60 FPS
        self.is_shielded = False

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x = 0
        elif self.x >= SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.is_shielded:
            pygame.draw.circle(screen, BLUE, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2 + 10, 3)

    def activate_power_up(self, power_up_type):
        self.power_up_type = power_up_type
        self.power_up_timer = self.power_up_duration
        self.is_shielded = (power_up_type == "shield")
        print(f"Power-up: {power_up_type} activated!")

    def update_power_up(self):
        if self.power_up_timer > 0:
            self.power_up_timer -= 1
        else:
            self.power_up_type = "normal"
            self.is_shielded = False

class Bullet:
    def __init__(self, x, y, bullet_type="normal"):
        self.image = bullet_img
        self.x = x
        self.y = y
        self.speed = 10
        self.state = "ready" # ready, fire
        self.type = bullet_type

    def fire(self, screen):
        self.state = "fire"
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= self.speed

class Invader:
    def __init__(self, invader_type, x, y):
        self.type = invader_type
        self.image = invader_imgs[invader_type]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.x_change = 2
        self.y_change = 30
        self.health = 1 # Basic invaders have 1 health
        if self.type == "tough":
            self.health = 3
            self.x_change = 1 # Slower
        elif self.type == "fast":
            self.x_change = 4 # Faster
        elif self.type == "boss":
            self.health = 10
            self.x_change = 0.5 # Very slow, but big
            self.y_change = 10 # Moves less vertically

    def move(self):
        self.x += self.x_change
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.x_change *= -1 # Reverse direction
            self.y += self.y_change

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        # Optionally draw health bar for tough/boss invaders
        if self.health > 1:
            pygame.draw.rect(screen, RED, (self.x, self.y - 10, self.width, 5))
            pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.width * (self.health / (3 if self.type == "tough" else 10)), 5))


class PowerUpItem:
    def __init__(self, power_up_type, x, y):
        self.type = power_up_type
        self.image = powerup_imgs[power_up_type]
        self.x = x
        self.y = y
        self.speed = 2 # Drops slowly
        self.active = True

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.active = False # Remove if off screen

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

# --- Game Variables ---
player = Player()
bullets = []
invaders = []
power_up_items = []

score_value = 0
chain_count = 0
score_multiplier = 1
last_hit_time = 0
CHAIN_RESET_TIME = 120 # 2 seconds at 60 FPS

fever_mode = False
fever_timer = 0
FEVER_DURATION = 600 # 10 seconds at 60 FPS

# Starfield background
stars = []
for _ in range(100):
    stars.append([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(1, 3)]) # x, y, speed

def draw_stars(screen):
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2] // 2)
        star[1] += star[2] # Move star down
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)

def create_invaders(num):
    invader_types = ["basic", "fast", "tough"]
    for _ in range(num):
        type = random.choice(invader_types)
        x = random.randint(0, SCREEN_WIDTH - invader_imgs[type].get_width())
        y = random.randint(50, 150)
        invaders.append(Invader(type, x, y))

def create_boss_invader():
    x = (SCREEN_WIDTH - invader_imgs["boss"].get_width()) // 2
    y = 50
    invaders.append(Invader("boss", x, y))

# Initial invaders
create_invaders(6)

# Collision detection (AABB - Axis-Aligned Bounding Box)
def is_collision(obj1_x, obj1_y, obj1_width, obj1_height, obj2_x, obj2_y, obj2_width, obj2_height):
    return (obj1_x < obj2_x + obj2_width and
            obj1_x + obj1_width > obj2_x and
            obj1_y < obj2_y + obj2_height and
            obj1_y + obj1_height > obj2_y)

def show_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def game_over_screen():
    over_text = game_over_font.render("GAME OVER", True, WHITE)
    screen.blit(over_text, ((SCREEN_WIDTH - over_text.get_width()) // 2, (SCREEN_HEIGHT - over_text.get_height()) // 2))

# --- Game Loop ---
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    draw_stars(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -player.speed
            if event.key == pygame.K_RIGHT:
                player.x_change = player.speed
            if event.key == pygame.K_SPACE:
                if player.power_up_type == "normal" or fever_mode:
                    bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2, player.y))
                elif player.power_up_type == "wideshot":
                    bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2 - 20, player.y))
                    bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2, player.y))
                    bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2 + 20, player.y))
                elif player.power_up_type == "laser":
                    # Laser is a continuous beam, so we'll just add one special bullet for simplicity
                    # In a real game, this would be a persistent effect
                    bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2, player.y, "laser"))


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0

    # --- Update Game State ---
    player.move()
    player.update_power_up()

    # Fever Mode update
    if fever_mode:
        fever_timer -= 1
        if fever_timer <= 0:
            fever_mode = False
            print("Fever Time Over!")

    # Invader movement and collision with player
    for invader_obj in list(invaders): # Iterate over a copy to allow removal
        invader_obj.move()

        # Invader reaches bottom or collides with player
        if invader_obj.y + invader_obj.height >= SCREEN_HEIGHT - player.height - 20 or \
           is_collision(player.x, player.y, player.width, player.height,
                        invader_obj.x, invader_obj.y, invader_obj.width, invader_obj.height):
            if not player.is_shielded:
                player.lives -= 1
                invaders.remove(invader_obj)
                # Reset game state for next life (optional, but common in Space Invaders)
                bullets.clear()
                power_up_items.clear()
                invaders.clear()
                create_invaders(6) # Re-spawn initial invaders
                chain_count = 0
                score_multiplier = 1
                fever_mode = False
                fever_timer = 0
                if player.lives <= 0:
                    running = False # Game Over

        invader_obj.draw(screen)

    # Bullet movement and collision with invaders
    for bullet_obj in list(bullets): # Iterate over a copy
        bullet_obj.move()
        bullet_obj.fire(screen) # Draw bullet as it moves

        if bullet_obj.y < 0:
            bullets.remove(bullet_obj)
            continue

        for invader_obj in list(invaders):
            if is_collision(bullet_obj.x, bullet_obj.y, bullet_obj.image.get_width(), bullet_obj.image.get_height(),
                            invader_obj.x, invader_obj.y, invader_obj.width, invader_obj.height):
                # Remove bullet on hit (unless it's a laser)
                if bullet_obj.type != "laser":
                    if bullet_obj in bullets: # Check if it's still in list (might be removed by another collision)
                        bullets.remove(bullet_obj)

                invader_obj.health -= 1
                last_hit_time = pygame.time.get_ticks() # Record time of last hit

                if invader_obj.health <= 0:
                    # Invader destroyed
                    invaders.remove(invader_obj)
                    chain_count += 1
                    score_value += 10 * score_multiplier

                    # Randomly drop a power-up
                    if random.random() < 0.2: # 20% chance to drop power-up
                        power_up_types = ["wideshot", "laser", "shield", "fever"]
                        dropped_type = random.choice(power_up_types)
                        power_up_items.append(PowerUpItem(dropped_type, invader_obj.x, invader_obj.y))

                    # Increase multiplier based on chain
                    if chain_count % 5 == 0 and chain_count > 0:
                        score_multiplier += 0.5
                        print(f"Multiplier increased to {score_multiplier}x!")

                break # Only one invader can be hit per bullet (for normal/wideshot)

    # Power-up item movement and collision with player
    for item in list(power_up_items):
        item.move()
        item.draw(screen)
        if is_collision(player.x, player.y, player.width, player.height,
                        item.x, item.y, item.image.get_width(), item.image.get_height()):
            player.activate_power_up(item.type)
            if item.type == "fever":
                fever_mode = True
                fever_timer = FEVER_DURATION
                print("FEVER TIME!")
            power_up_items.remove(item)

    # Chain reset logic
    if pygame.time.get_ticks() - last_hit_time > CHAIN_RESET_TIME and chain_count > 0:
        chain_count = 0
        score_multiplier = 1
        print("Chain reset!")

    # Spawn new invaders if all are destroyed
    if not invaders:
        if random.random() < 0.1: # Small chance to spawn a boss
            create_boss_invader()
        else:
            create_invaders(min(6 + score_value // 100, 15)) # More invaders as score increases

    # --- Draw all elements ---
    player.draw(screen)
    show_text(f"Score: {int(score_value)}", 10, 10)
    show_text(f"Lives: {player.lives}", 10, 40)
    show_text(f"Chain: {chain_count}", 10, 70)
    show_text(f"Multiplier: {score_multiplier:.1f}x", 10, 100)
    if player.power_up_type != "normal":
        show_text(f"Power-up: {player.power_up_type.upper()} ({player.power_up_timer // 60 + 1}s)", SCREEN_WIDTH - 250, 10, YELLOW)
    if fever_mode:
        show_text(f"FEVER TIME! ({fever_timer // 60 + 1}s)", SCREEN_WIDTH // 2 - 100, 10, RED)

    if player.lives <= 0:
        game_over_screen()
        # Optionally, add a delay or a way to restart the game
        # For now, it will just close after a short while.
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

    pygame.display.update()
    clock.tick(60) # Limit to 60 FPS

pygame.quit()