import pygame
import random
from entities import CrystalAggroEnemy, PlayerAggroEnemy, Tower


class Wave:  # Represents a wave of enemies
    def __init__(self, wave_number):
        self.wave_number = wave_number
        self.enemies_to_spawn = self.calculate_enemies()
        self.spawn_timer = 0
        self.spawn_delay = max(10, 60 - self.wave_number * 2)  # Decrease spawn delay as waves progress

    def calculate_enemies(self):  # Calculate the number of enemies for this wave
        return 3 + self.wave_number  # Increase enemies per wave

    def update(self, game_state):  # Update wave state and spawn enemies
        if self.enemies_to_spawn > 0:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_enemy(game_state)
                self.enemies_to_spawn -= 1
                self.spawn_timer = 0

    def spawn_enemy(self, game_state):  # Spawn a single enemy
        x = random.randint(0, 800)
        y = 0
        if random.random() < 0.5:
            enemy = CrystalAggroEnemy(x, y, self.wave_number)
        else:
            enemy = PlayerAggroEnemy(x, y, self.wave_number)
        game_state.add_enemy(enemy)

    def is_complete(self):  # Check if the wave is complete
        return self.enemies_to_spawn == 0

    def draw(self, screen):  # Draw wave information
        font = pygame.font.Font(None, 36)
        text = font.render(f"Wave: {self.wave_number}", True, (255, 255, 255))
        screen.blit(text, (10, 10))


def update_crystal_aggro_enemy(enemy, crystal):  # Update CrystalAggroEnemy
    enemy.move(crystal.x, crystal.y)


class GameState:  # Represents the current state of the game
    def __init__(self):
        self.towers = []  # List to store all towers
        self.enemies = []  # List to store all active enemies
        self.pellets = []  # List to store all active pellets
        self.current_wave = Wave(1)  # Initialize the first wave
        self.score = 0  # Player's score

    def add_tower(self, x, y, tower_type):  # Add a new tower to the game
        self.towers.append(Tower(x, y, tower_type))

    def add_enemy(self, enemy):  # Add a new enemy to the game
        self.enemies.append(enemy)

    def update(self, crystal, player):  # Update game state
        self.current_wave.update(self)
        self.update_towers()
        self.update_enemies(crystal, player)
        self.update_pellets(player)
        self.check_wave_completion()

    def update_towers(self):  # Update all towers
        for tower in self.towers:
            tower.attack(self.enemies)

    def update_enemies(self, crystal, player):  # Update all enemies
        for enemy in self.enemies[:]:
            if isinstance(enemy, PlayerAggroEnemy):
                self.update_player_aggro_enemy(enemy, player)
            else:
                update_crystal_aggro_enemy(enemy, crystal)

            if self.check_crystal_collision(enemy, crystal):
                enemy.attack(crystal)
                self.enemies.remove(enemy)
            elif enemy.health <= 0:
                self.enemies.remove(enemy)
                self.score += 10

    def update_player_aggro_enemy(self, enemy, player):  # Update PlayerAggroEnemy
        enemy.move(player.x, player.y)
        enemy.update()
        pellet = enemy.attack(player)
        if pellet:
            self.pellets.append(pellet)

    def update_pellets(self, player):  # Update all pellets
        for pellet in self.pellets[:]:
            pellet.move()
            if self.check_player_collision(pellet, player):
                player.take_damage(1)
                self.pellets.remove(pellet)
            elif not self.is_on_screen(pellet):
                self.pellets.remove(pellet)

    def check_wave_completion(self):  # Check if the current wave is complete
        if self.current_wave.is_complete() and len(self.enemies) == 0:
            self.start_next_wave()

    def start_next_wave(self):  # Start the next wave
        self.current_wave = Wave(self.current_wave.wave_number + 1)

    @staticmethod
    def check_player_collision(pellet, player):  # Check if a pellet has collided with the player
        return (abs(pellet.x - player.x) < player.size and
                abs(pellet.y - player.y) < player.size)

    @staticmethod
    def check_crystal_collision(enemy, crystal):  # Check if an enemy has collided with the crystal
        return (abs(enemy.x - crystal.x) < crystal.size and
                abs(enemy.y - crystal.y) < crystal.size)

    @staticmethod
    def is_on_screen(pellet):  # Check if a pellet is still within the screen bounds
        return 0 <= pellet.x <= 800 and 0 <= pellet.y <= 600

    def draw(self, screen):  # Draw all game objects
        for tower in self.towers:
            tower.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for pellet in self.pellets:
            pellet.draw(screen)
        self.current_wave.draw(screen)
