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
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255) # Invader bullet color
DARK_GREEN = (0, 100, 0) # Defined DARK_GREEN
LIGHT_GREY = (200, 200, 200)

# Fonts
font = pygame.font.Font('freesansbold.ttf', 24)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
option_font = pygame.font.Font('freesansbold.ttf', 36) # Font for continue/give up options

# --- Game Assets (Drawn Shapes for Player and Invaders) ---

# Player image (drawn spaceship)
player_img = pygame.Surface((50, 50), pygame.SRCALPHA) # Use SRCALPHA for transparency
pygame.draw.polygon(player_img, BLUE, [(0, 50), (50, 50), (25, 0)]) # Main body
pygame.draw.rect(player_img, LIGHT_GREY, (15, 40, 20, 10), border_radius=3) # Cockpit
pygame.draw.polygon(player_img, YELLOW, [(0, 50), (10, 40), (10, 50)]) # Left wing
pygame.draw.polygon(player_img, YELLOW, [(50, 50), (40, 40), (40, 50)]) # Right wing
pygame.draw.rect(player_img, RED, (20, 45, 10, 5)) # Engine exhaust

# Invader images (drawn alien shapes)
invader_imgs = {}

# Basic Invader (Green, rounded head with eyes)
basic_invader_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.ellipse(basic_invader_surface, DARK_GREEN, (0, 10, 40, 30)) # Body
pygame.draw.circle(basic_invader_surface, WHITE, (12, 18), 4) # Left eye
pygame.draw.circle(basic_invader_surface, WHITE, (28, 18), 4) # Right eye
pygame.draw.circle(basic_invader_surface, BLACK, (12, 18), 2) # Left pupil
pygame.draw.circle(basic_invader_surface, BLACK, (28, 18), 2) # Right pupil
invader_imgs["basic"] = basic_invader_surface

# Fast Invader (Red, sharp, dart-like)
fast_invader_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.polygon(fast_invader_surface, RED, [(0, 20), (40, 0), (40, 40)]) # Arrow/triangle shape
pygame.draw.rect(fast_invader_surface, YELLOW, (15, 15, 10, 10)) # Core
invader_imgs["fast"] = fast_invader_surface

# Tough Invader (Purple, robust with small arms)
tough_invader_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.rect(tough_invader_surface, PURPLE, (5, 5, 30, 30), border_radius=5) # Main body
pygame.draw.polygon(tough_invader_surface, DARK_GREEN, [(0, 15), (5, 10), (5, 20)]) # Left arm (CHANGED TO DARK_GREEN)
pygame.draw.polygon(tough_invader_surface, DARK_GREEN, [(40, 15), (35, 10), (35, 20)]) # Right arm (CHANGED TO DARK_GREEN)
pygame.draw.circle(tough_invader_surface, WHITE, (12, 12), 3)
pygame.draw.circle(tough_invader_surface, WHITE, (28, 12), 3)
invader_imgs["tough"] = tough_invader_surface

# Boss Invader (Orange, larger, more complex)
boss_invader_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
pygame.draw.ellipse(boss_invader_surface, ORANGE, (0, 20, 80, 40)) # Main body
pygame.draw.arc(boss_invader_surface, ORANGE, (10, 0, 60, 40), math.pi, 2 * math.pi, 0) # Top dome
pygame.draw.circle(boss_invader_surface, YELLOW, (25, 30), 8) # Left eye
pygame.draw.circle(boss_invader_surface, YELLOW, (55, 30), 8) # Right eye
pygame.draw.circle(boss_invader_surface, BLACK, (25, 30), 4) # Left pupil
pygame.draw.circle(boss_invader_surface, BLACK, (55, 30), 4) # Right pupil
pygame.draw.line(boss_invader_surface, ORANGE, (20, 60), (10, 75), 3) # Tentacle 1
pygame.draw.line(boss_invader_surface, ORANGE, (60, 60), (70, 75), 3) # Tentacle 2
invader_imgs["boss"] = boss_invader_surface

# Bullet image (player's bullet)
bullet_img = pygame.Surface((10, 20), pygame.SRCALPHA)
pygame.draw.rect(bullet_img, YELLOW, (0, 0, 10, 20), border_radius=2)

# Power-up images (drawn shapes)
powerup_imgs = {}

# Wideshot Power-up (Orange)
wideshot_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.circle(wideshot_surface, ORANGE, (10, 10), 8)
pygame.draw.line(wideshot_surface, WHITE, (5, 10), (15, 10), 2)
pygame.draw.line(wideshot_surface, WHITE, (10, 5), (10, 15), 2)
powerup_imgs["wideshot"] = wideshot_surface 

# Laser Power-up (Red)
laser_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.rect(laser_surface, RED, (5, 0, 10, 20), border_radius=2)
powerup_imgs["laser"] = laser_surface 

# Shield Power-up (Blue)
shield_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.circle(shield_surface, BLUE, (10, 10), 10, 2)
powerup_imgs["shield"] = shield_surface 

# Fever Power-up (Yellow)
fever_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.polygon(fever_surface, YELLOW, [(10, 0), (0, 20), (20, 20)]) # Star-like
powerup_imgs["fever"] = fever_surface 


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
        self.max_lives = 3 # Max lives for health bar calculation
        self.lives = self.max_lives # Current lives
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
        
        # Player Health Bar (Lives as Health)
        bar_width = self.width * 1.5 # Make it a bit wider than the player
        bar_height = 8
        bar_x = self.x + (self.width - bar_width) // 2 # Center it
        bar_y = self.y + self.height + 5 # Below the player

        # Draw background of health bar
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Draw current health
        current_health_width = (self.lives / self.max_lives) * bar_width
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_health_width, bar_height))
        # Draw border
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)


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

class Bullet: # Player's bullet
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

class InvaderBullet: # Invader's bullet
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8 # Increased radius for visibility
        self.color = MAGENTA # Distinct color for invader bullets
        self.speed = 5
        self.active = True

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


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
        # FURTHER ADJUSTED FIRE RATE for much less frequent shots
        self.fire_rate = random.randint(300, 720) # Frames between shots (5 to 12 seconds)
        self.last_shot_time = pygame.time.get_ticks()

        if self.type == "tough":
            self.health = 3
            self.x_change = 1 # Slower
            self.fire_rate = random.randint(500, 1000) # Tougher, even less frequent shots (8.3 to 16.6 seconds)
        elif self.type == "fast":
            self.x_change = 4 # Faster
            self.fire_rate = random.randint(250, 600) # Faster, but significantly less frequent (4.1 to 10 seconds)
        elif self.type == "boss":
            self.health = 10
            self.x_change = 0.5 # Very slow, but big
            self.y_change = 10 # Moves less vertically
            self.fire_rate = random.randint(240, 540) # Boss fires less frequently (4 to 9 seconds)

    def move(self):
        self.x += self.x_change
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.x_change *= -1 # Reverse direction
            self.y += self.y_change

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        # Optionally draw health bar for tough/boss invaders
        if self.health > 0: # Draw health bar as long as health is above 0
            health_bar_width = self.width
            health_bar_height = 5
            health_percentage = self.health / (3 if self.type == "tough" else (10 if self.type == "boss" else 1))
            pygame.draw.rect(screen, RED, (self.x, self.y - 10, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, health_bar_width * health_percentage, health_bar_height))
            pygame.draw.rect(screen, WHITE, (self.x, self.y - 10, health_bar_width, health_bar_height), 1) # Border


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
bullets = [] # Player bullets
invaders = []
power_up_items = []
invader_bullets = [] # List for invader bullets

score_value = 0
chain_count = 0
score_multiplier = 1
last_hit_time = 0
CHAIN_RESET_TIME = 120 # 2 seconds at 60 FPS

fever_mode = False
fever_timer = 0
FEVER_DURATION = 600 # 10 seconds at 60 FPS

# Game state management
GAME_STATE_PLAYING = 0
GAME_STATE_GAME_OVER_MENU = 1
current_game_state = GAME_STATE_PLAYING

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

# Function to reset the entire game state
def reset_game():
    global player, bullets, invaders, power_up_items, invader_bullets, score_value, chain_count, score_multiplier, fever_mode, fever_timer, current_game_state
    player = Player() # Re-initialize player
    bullets.clear()
    invaders.clear()
    power_up_items.clear()
    invader_bullets.clear()
    score_value = 0
    chain_count = 0
    score_multiplier = 1
    fever_mode = False
    fever_timer = 0
    create_invaders(6) # Re-spawn initial invaders
    current_game_state = GAME_STATE_PLAYING


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
    screen.blit(over_text, ((SCREEN_WIDTH - over_text.get_width()) // 2, (SCREEN_HEIGHT - over_text.get_height()) // 2 - 50))

    continue_text = option_font.render("Press C to Continue", True, GREEN)
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(continue_text, continue_rect)

    give_up_text = option_font.render("Press G to Give Up", True, RED)
    give_up_rect = give_up_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
    screen.blit(give_up_text, give_up_rect)

# --- Game Loop ---
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    draw_stars(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_game_state == GAME_STATE_PLAYING:
            # Handle player movement and shooting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_change = -player.speed
                elif event.key == pygame.K_RIGHT:
                    player.x_change = player.speed
                elif event.key == pygame.K_SPACE:
                    if player.power_up_type == "normal" or fever_mode:
                        bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2, player.y))
                    elif player.power_up_type == "wideshot":
                        bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2 - 20, player.y))
                        bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2, player.y))
                        bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2 + 20, player.y))
                    elif player.power_up_type == "laser":
                        bullets.append(Bullet(player.x + player.width // 2 - bullet_img.get_width() // 2, player.y, "laser"))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
        
        elif current_game_state == GAME_STATE_GAME_OVER_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: # Continue
                    reset_game()
                elif event.key == pygame.K_g: # Give Up
                    running = False

    # --- Update Game State ---
    if current_game_state == GAME_STATE_PLAYING:
        player.move()
        player.update_power_up()

        # Fever Mode update
        if fever_mode:
            fever_timer -= 1
            if fever_timer <= 0:
                fever_mode = False
                print("Fever Time Over!")

        # Invader movement and firing logic
        for invader_obj in list(invaders): # Iterate over a copy to allow removal
            invader_obj.move()

            current_time = pygame.time.get_ticks()
            if current_time - invader_obj.last_shot_time > invader_obj.fire_rate:
                invader_bullets.append(InvaderBullet(invader_obj.x + invader_obj.width // 2, invader_obj.y + invader_obj.height))
                invader_obj.last_shot_time = current_time


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
                    invader_bullets.clear() # Clear invader bullets on player hit
                    create_invaders(6) # Re-spawn initial invaders
                    chain_count = 0
                    score_multiplier = 1
                    fever_mode = False
                    fever_timer = 0
                    if player.lives <= 0:
                        current_game_state = GAME_STATE_GAME_OVER_MENU # Change state to game over menu
                        # No need to set running = False here, as we want to show the menu

            invader_obj.draw(screen)

        # Player Bullet movement and collision with invaders
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

        # Invader Bullet movement and collision with player
        for inv_bullet in list(invader_bullets):
            inv_bullet.move()
            inv_bullet.draw(screen)
            if not inv_bullet.active:
                invader_bullets.remove(inv_bullet)
                continue

            # Collision with player
            if is_collision(player.x, player.y, player.width, player.height,
                            inv_bullet.x - inv_bullet.radius, inv_bullet.y - inv_bullet.radius, # Adjust for circle's top-left
                            inv_bullet.radius * 2, inv_bullet.radius * 2):
                if not player.is_shielded:
                    player.lives -= 1
                    print(f"Player hit! Lives: {player.lives}")
                    if player.lives <= 0:
                        current_game_state = GAME_STATE_GAME_OVER_MENU # Change state to game over menu
                invader_bullets.remove(inv_bullet)
                continue

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
    if current_game_state == GAME_STATE_PLAYING:
        player.draw(screen)
        show_text(f"Score: {int(score_value)}", 10, 10)
        show_text(f"Lives: {player.lives}", 10, 40) # Keep lives text for clarity
        show_text(f"Chain: {chain_count}", 10, 70)
        show_text(f"Multiplier: {score_multiplier:.1f}x", 10, 100)
        if player.power_up_type != "normal":
            show_text(f"Power-up: {player.power_up_type.upper()} ({player.power_up_timer // 60 + 1}s)", SCREEN_WIDTH - 250, 10, YELLOW)
        if fever_mode:
            show_text(f"FEVER TIME! ({fever_timer // 60 + 1}s)", SCREEN_WIDTH // 2 - 100, 10, RED)
    elif current_game_state == GAME_STATE_GAME_OVER_MENU:
        game_over_screen()
        # No need for pygame.time.wait here, as we are waiting for user input

    pygame.display.update()
    clock.tick(60) # Limit to 60 FPS

pygame.quit()
