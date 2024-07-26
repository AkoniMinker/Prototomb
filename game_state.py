from enemy import PlayerAggroEnemy
from tower import Tower
from wave import Wave


def check_player_collision(pellet, player):
    # Check if a pellet has collided with the player
    return (abs(pellet.x - player.x) < player.size and
            abs(pellet.y - player.y) < player.size)


def check_crystal_collision(enemy, crystal):
    # Check if an enemy has collided with the crystal
    return (abs(enemy.x - crystal.x) < crystal.size and
            abs(enemy.y - crystal.y) < crystal.size)


def is_on_screen(pellet):
    # Check if a pellet is still within the screen bounds
    return 0 <= pellet.x <= 800 and 0 <= pellet.y <= 600


class GameState:
    def __init__(self):
        self.towers = []  # List to store all towers
        self.enemies = []  # List to store all active enemies
        self.pellets = []  # List to store all active pellets
        self.current_wave = Wave(1)  # Initialize the first wave
        self.score = 0  # Player's score

    def add_tower(self, x, y, tower_type):
        # Add a new tower to the game
        self.towers.append(Tower(x, y, tower_type))

    def add_enemy(self, enemy):
        # Add a new enemy to the game
        self.enemies.append(enemy)

    def update(self, crystal, player):
        # Update the current wave (spawn new enemies if needed)
        self.current_wave.update(self)

        # Update towers
        for tower in self.towers:
            tower.attack(self.enemies)

        # Update enemies
        for enemy in self.enemies[:]:
            if isinstance(enemy, PlayerAggroEnemy):
                # PlayerAggroEnemy moves towards the player
                enemy.move(player.x, player.y)
                enemy.update()  # Update the enemy's cooldown
                # Check if the enemy shoots a pellet
                pellet = enemy.attack(player)
                if pellet:
                    self.pellets.append(pellet)
            else:
                # CrystalAggroEnemy moves towards the crystal
                enemy.move(crystal.x, crystal.y)

            # Check if the enemy has reached the crystal
            if check_crystal_collision(enemy, crystal):
                enemy.attack(crystal)
                self.enemies.remove(enemy)
            elif enemy.health <= 0:
                # Remove dead enemies and increase score
                self.enemies.remove(enemy)
                self.score += 10

        # Update pellets
        for pellet in self.pellets[:]:
            pellet.move()
            # Check if pellet hits the player
            if check_player_collision(pellet, player):
                player.take_damage(1)
                self.pellets.remove(pellet)
            elif not is_on_screen(pellet):
                # Remove pellets that are off-screen
                self.pellets.remove(pellet)

        # Check if the current wave is complete
        if self.current_wave.is_complete() and len(self.enemies) == 0:
            self.start_next_wave()

    def start_next_wave(self):
        # Start the next wave when the current one is complete
        self.current_wave = Wave(self.current_wave.wave_number + 1)

    def draw(self, screen):
        # Draw all game objects
        for tower in self.towers:
            tower.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for pellet in self.pellets:
            pellet.draw(screen)
        self.current_wave.draw(screen)
