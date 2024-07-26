import pygame
import random
from enemy import CrystalAggroEnemy, PlayerAggroEnemy

class Wave:
    def __init__(self, wave_number):
        self.wave_number = wave_number
        self.enemies_to_spawn = self.calculate_enemies()
        self.spawn_timer = 0
        self.spawn_delay = max(10, 60 - self.wave_number * 2)  # Decrease spawn delay as waves progress

    def calculate_enemies(self):
        return 3 + self.wave_number  # Increase enemies per wave

    def update(self, game_state):
        if self.enemies_to_spawn > 0:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                x = random.randint(0, 800)
                y = 0
                if random.random() < 0.5:
                    enemy = CrystalAggroEnemy(x, y, self.wave_number)
                else:
                    enemy = PlayerAggroEnemy(x, y, self.wave_number)
                game_state.add_enemy(enemy)
                self.enemies_to_spawn -= 1
                self.spawn_timer = 0

    def is_complete(self):
        return self.enemies_to_spawn == 0

    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Wave: {self.wave_number}", True, (255, 255, 255))
        screen.blit(text, (10, 10))