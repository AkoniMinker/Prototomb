import pygame
import sys
from entities import Player, Crystal
from game_logic import GameState, Wave
# For Later Use: from utils import Shop

pygame.init()  # Initialize Pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game states
PLAYING = 0
GAME_OVER = 1


class Game:  # Main game class
    def __init__(self):
        [self.game_state, self.last_wave_number, self.game_over_timer, self.current_state, self.game_stat, self.player,
         self.crystal] = [
            None, None, None, None, None, None, None]  # I hate Pycharm Errors
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense Prototype")
        self.clock = pygame.time.Clock()
        self.reset_game()
        # Load sounds
        self.player_attack_sound = pygame.mixer.Sound('p_attack.mp3')
        self.crystal_damaged_sound = pygame.mixer.Sound('c_damaged.mp3')
        self.quit_button = pygame.Rect(SCREEN_WIDTH - 40, 10, 30, 30)  # Create quit button

    def reset_game(self, from_last_wave=False):  # Reset the game state
        self.crystal = Crystal(400, 500)
        boundary_y = self.crystal.y - 50
        self.player = Player(400, boundary_y - 30)
        self.game_state = GameState()
        if from_last_wave:
            self.game_state.current_wave = Wave(self.last_wave_number)
        else:
            self.game_state.current_wave = Wave(1)
        self.current_state = PLAYING
        self.game_over_timer = 3 * FPS  # 3 seconds
        self.last_wave_number = 1

    def handle_events(self):  # Handle game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key in (
                        pygame.K_SPACE,
                        pygame.K_RETURN) and self.player.attack_cooldown == 0 and self.current_state == PLAYING:
                    self.player.attack_action()
                    self.player_attack_sound.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button.collidepoint(event.pos):
                    return False
        return True

    def update(self):  # Update game state
        if self.current_state == PLAYING:
            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] or keys[pygame.K_d] - keys[pygame.K_a]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP] or keys[pygame.K_s] - keys[pygame.K_w]
            self.player.move(dx, dy, self.crystal.y - 50)
            self.player.update()
            self.player.check_attack_collision(self.game_state.enemies)
            self.game_state.update(self.crystal, self.player)
            if self.crystal.health < self.crystal.last_health:
                self.crystal_damaged_sound.play()
            self.crystal.last_health = self.crystal.health
            if self.crystal.health <= 0 or self.player.health <= 0:
                self.current_state = GAME_OVER
                self.last_wave_number = self.game_state.current_wave.wave_number

    def draw(self):  # Draw game objects
        self.screen.fill(BLACK)
        if self.current_state == PLAYING:
            pygame.draw.line(self.screen, WHITE, (0, self.crystal.y - 50), (SCREEN_WIDTH, self.crystal.y - 50))
            self.player.draw(self.screen)
            self.crystal.draw(self.screen)
            self.game_state.draw(self.screen)
            self.draw_quit_button()
        elif self.current_state == GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_quit_button(self):  # Draw the quit button
        pygame.draw.rect(self.screen, RED, self.quit_button)
        quit_x, quit_y = self.quit_button.x + 5, self.quit_button.y + 5
        pygame.draw.line(self.screen, WHITE, (quit_x, quit_y), (quit_x + 20, quit_y + 20), 2)
        pygame.draw.line(self.screen, WHITE, (quit_x, quit_y + 20), (quit_x + 20, quit_y), 2)

    def draw_game_over(self):  # Draw the game over screen
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, RED)
        self.screen.blit(game_over_text,
                         (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        if self.game_over_timer > 0:
            timer_text = font.render(str(self.game_over_timer // FPS + 1), True, WHITE)
            self.screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, SCREEN_HEIGHT // 2))
            self.game_over_timer -= 1
        else:
            restart_text = font.render("Press Spacebar to Restart", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

            last_wave_text_line1 = font.render("Press Enter to Restart", True, WHITE)
            self.screen.blit(last_wave_text_line1,
                             (SCREEN_WIDTH // 2 - last_wave_text_line1.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

            last_wave_text_line2 = font.render("from the last wave", True, WHITE)
            self.screen.blit(last_wave_text_line2,
                             (SCREEN_WIDTH // 2 - last_wave_text_line2.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

            key_presses = pygame.key.get_pressed()
            if key_presses[pygame.K_SPACE]:
                self.reset_game()
            elif key_presses[pygame.K_RETURN]:
                self.reset_game(from_last_wave=True)

    def run(self):  # Main game loop
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
