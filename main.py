import pygame
import sys
from entities import Player
from entities import Crystal
from game_logic import GameState
from game_logic import Wave
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
        elif event.type == pygame.KEYDOWN and current_state == PLAYING:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                player.attack_action()

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

        # Check for game over conditions
        if crystal.health <= 0 or player.health <= 0:
            current_state = GAME_OVER
            last_wave_number = game_state.current_wave.wave_number

        # Draw game objects
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (0, boundary_y), (SCREEN_WIDTH, boundary_y))
        player.draw(screen)
        crystal.draw(screen)
        game_state.draw(screen)

    elif current_state == GAME_OVER:
        handle_game_over()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
