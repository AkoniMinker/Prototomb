import pygame
import sys
from entities import Player, Crystal
from game_logic import GameState, Wave
from utils import Shop

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense Prototype")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize game objects
crystal = Crystal(400, 500)
boundary_y = crystal.y - 50  # Set the boundary 50 pixels above the crystal
player = Player(400, boundary_y - 30)  # Start the player above the boundary
game_state = GameState()
shop = Shop()

# Game states
PLAYING = 0
GAME_OVER = 1

# Initialize game state
current_state = PLAYING
game_over_timer = 180  # 3 seconds at 60 FPS
last_wave_number = 1

# Load sounds
player_attack_sound = pygame.mixer.Sound('p_attack.mp3')
crystal_damaged_sound = pygame.mixer.Sound('c_damaged.mp3')

# Create surfaces (boundaries)
surfaces = [
    pygame.Rect(0, 50, 10, SCREEN_HEIGHT - 100),  # Left vertical line
    pygame.Rect(SCREEN_WIDTH - 10, 50, 10, SCREEN_HEIGHT - 100),  # Right vertical line
    pygame.Rect(50, 50, 250, 10),  # Top left horizontal line
    pygame.Rect(SCREEN_WIDTH - 300, 50, 250, 10),  # Top right horizontal line
    pygame.Rect(50, SCREEN_HEIGHT - 60, SCREEN_WIDTH - 100, 10),  # Bottom horizontal line
    pygame.Rect(200, 150, 150, 100),  # Left box
    pygame.Rect(SCREEN_WIDTH - 350, 150, 150, 100),  # Right box
]

# Create diagonal lines for boxes
left_diagonal = ((200, 250), (350, 150))
right_diagonal = ((SCREEN_WIDTH - 350, 250), (SCREEN_WIDTH - 200, 150))


# Create quit button
quit_button = pygame.Rect(SCREEN_WIDTH - 40, 10, 30, 30)


def reset_game(from_last_wave=False):
    global crystal, player, game_state, current_state, game_over_timer, last_wave_number

    if from_last_wave:
        wave_number = last_wave_number
    else:
        wave_number = 1

    crystal = Crystal(400, 500)
    player = Player(400, boundary_y - 30)
    game_state = GameState()
    game_state.current_wave = Wave(wave_number)
    current_state = PLAYING
    game_over_timer = 180


def handle_game_over():
    global game_over_timer, current_state, last_wave_number

    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    if game_over_timer > 0:
        timer_text = font.render(str(game_over_timer // 60 + 1), True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, SCREEN_HEIGHT // 2))
        game_over_timer -= 1
    else:
        restart_text = font.render("Press Spacebar to Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

        last_wave_text_line1 = font.render("Press Enter to Restart", True, WHITE)
        screen.blit(last_wave_text_line1,
                    (SCREEN_WIDTH // 2 - last_wave_text_line1.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        last_wave_text_line2 = font.render("from the last wave", True, WHITE)
        screen.blit(last_wave_text_line2,
                    (SCREEN_WIDTH // 2 - last_wave_text_line2.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

        key_presses = pygame.key.get_pressed()
        if key_presses[pygame.K_SPACE]:
            reset_game()
        elif key_presses[pygame.K_RETURN]:
            reset_game(from_last_wave=True)


# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN) and (player.attack_cooldown == 0) and current_state == PLAYING:
                player.attack_action()
                player_attack_sound.play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.collidepoint(event.pos):
                running = False

    if current_state == PLAYING:
        # Get pressed keys for continuous movement
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] or keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP] or keys[pygame.K_s] - keys[pygame.K_w]

        # Move player
        player.move(dx, dy, boundary_y)

        # Update player state
        player.update()
        player.check_attack_collision(game_state.enemies)

        # Update game state
        game_state.update(crystal, player)

        # Check for crystal damage
        if crystal.health < crystal.last_health:
            crystal_damaged_sound.play()
        crystal.last_health = crystal.health

        # Check for game over conditions
        if crystal.health <= 0 or player.health <= 0:
            current_state = GAME_OVER
            last_wave_number = game_state.current_wave.wave_number

        # Draw game objects
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (0, boundary_y), (SCREEN_WIDTH, boundary_y)) # boundary between player and crystal
        for surface in surfaces:
            pygame.draw.rect(screen, WHITE, surface)
        pygame.draw.line(screen, WHITE, *left_diagonal, 2)
        pygame.draw.line(screen, WHITE, *right_diagonal, 2)
        player.draw(screen)
        crystal.draw(screen)
        game_state.draw(screen)

        # Draw quit button
        pygame.draw.rect(screen, RED, quit_button)
        quit_x = quit_button.x + 5
        quit_y = quit_button.y + 5
        pygame.draw.line(screen, WHITE, (quit_x, quit_y), (quit_x + 20, quit_y + 20), 2)
        pygame.draw.line(screen, WHITE, (quit_x, quit_y + 20), (quit_x + 20, quit_y), 2)

    elif current_state == GAME_OVER:
        handle_game_over()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
