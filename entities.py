import pygame
import math
from utils import Attack, HealthBar


# tower


class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.type = tower_type
        self.damage = 10  # Base damage for the tower
        self.range = 100  # Attack range in pixels
        self.color = (255, 0, 0)  # Red color for the tower
        self.size = 25  # Size of the tower in pixels
        self.attack_cooldown = 0  # Current cooldown timer
        self.max_attack_cooldown = 60  # Maximum cooldown (1 second at 60 FPS)

    def attack(self, enemies):
        # Check if the tower can attack (cooldown is 0)
        if self.attack_cooldown == 0:
            for enemy in enemies:
                # Calculate distance to the enemy
                distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if distance <= self.range:
                    # If enemy is in range, damage it and reset cooldown
                    enemy.take_damage(self.damage)
                    self.attack_cooldown = self.max_attack_cooldown
                    break  # Only attack one enemy per cooldown
        else:
            # Reduce cooldown timer
            self.attack_cooldown -= 1

    def draw(self, screen):
        # Draw the tower as a rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        # Draw the range circle (uncomment for debugging) pygame.draw.circle(screen, (255, 255, 255), (int(self.x +
        # self.size/2), int(self.y + self.size/2)), self.range, 1)

    def upgrade(self):
        # Placeholder for upgrade functionality
        self.damage += 5
        self.range += 20
        print(f"Tower upgraded! New damage: {self.damage}, New range: {self.range}")


# Could add different tower types as subclasses
# class ArrowTower(Tower):
#     def __init__(self, x, y):
#         super().__init__(x, y, "arrow")
#         self.damage = 15
#         self.range = 150
#
# class CannonTower(Tower):
#     def __init__(self, x, y):
#         super().__init__(x, y, "cannon")
#         self.damage = 30
#         self.range = 80
#         self.max_attack_cooldown = 90  # Slower attack speed


class Crystal:
    def __init__(self, x, y):
        # Initialize the crystal's position
        self.x = x
        self.y = y

        # Set the crystal's health attributes
        self.max_health = 100
        self.health = self.max_health

        # Set the crystal's appearance
        self.color = (0, 0, 255)  # Blue
        self.size = 30

        # Create a health bar for the crystal
        self.health_bar = HealthBar(self.x, self.y - 20, self.size, 5, self.max_health)

    def take_damage(self, amount):
        # Reduce the crystal's health by the damage amount
        self.health -= amount

        # Update the health bar to reflect the new health value
        self.health_bar.update(self.health)

        # Check if the crystal has been destroyed
        if self.health <= 0:
            print("Game Over: Crystal Destroyed!")

    def draw(self, screen):
        # Draw the crystal on the screen
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        # Draw the crystal's health bar
        self.health_bar.draw(screen)


# player


class Player:
    def __init__(self, x, y):
        # Initial position
        self.x = x
        self.y = y

        # Player attributes
        self.health = 100
        self.inventory = []
        self.color = (0, 255, 0)  # Green
        self.size = 20
        self.speed = 5  # Pixels per frame

        # Attack mechanism
        self.attack = Attack()
        self.attack_cooldown = 0
        self.max_attack_cooldown = 60  # 1 second at 60 FPS

        # Cooldown bar (initially None, created when attacking)
        self.cooldown_bar = None

        # Set the player's health attributes
        self.max_health = 100
        self.health = self.max_health

        # Create a health bar for the player
        self.health_bar = HealthBar(self.x, self.y - 20, self.size, 5, self.max_health)

    def move(self, dx, dy, boundary_y):
        # Normalize the movement vector
        length = math.hypot(dx, dy)
        if length != 0:
            dx, dy = dx / length, dy / length

        # Apply speed
        dx *= self.speed
        dy *= self.speed

        # Update position based on normalized input
        self.x += dx
        self.y += dy

        # Keep player within screen bounds and above the boundary
        self.x = max(0, min(self.x, 800 - self.size))
        self.y = max(0, min(self.y, boundary_y - self.size))

        # Update cooldown bar position if it exists
        if self.cooldown_bar:
            self.cooldown_bar.x = self.x
            self.cooldown_bar.y = self.y + self.size + 5

        # Update health bar position
        if self.health_bar:
            self.health_bar.x = self.x
            self.health_bar.y = self.y + self.size + 5

    def attack_action(self):
        # Initiate attack if cooldown is complete
        if self.attack_cooldown == 0:
            self.attack.start()
            self.attack_cooldown = self.max_attack_cooldown
            # Create cooldown bar when attack is initiated
            self.cooldown_bar = HealthBar(self.x, self.y + self.size + 5, self.size, 3, self.max_attack_cooldown)

    def update(self):
        # Update attack state
        self.attack.update()

        # Handle attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            self.cooldown_bar.update(self.max_attack_cooldown - self.attack_cooldown)
        elif self.cooldown_bar:
            # Remove cooldown bar when cooldown is complete
            self.cooldown_bar = None

    def collect_item(self, item):
        # Add item to player's inventory
        self.inventory.append(item)

    def draw(self, screen):
        # Draw player
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        # Draw attack effect
        self.attack.draw(screen, self.x + self.size / 2, self.y + self.size / 2)

        # Draw cooldown bar if it exists
        if self.cooldown_bar:
            self.cooldown_bar.draw(screen)

        # Draw a health bar if it exists
        if self.health_bar:
            self.health_bar.draw(screen)

    def check_attack_collision(self, enemies):
        # Check if attack hits any enemies
        self.attack.check_collision(self.x + self.size / 2, self.y + self.size / 2, enemies)

    def take_damage(self, amount):
        # Reduce player health when hit
        self.health -= amount

        # Update the health bar to reflect the new health value
        self.health_bar.update(self.health)

        # Check if the player has been destroyed
        if self.health <= 0:
            print("Game Over: Player Killed!")


# enemy

class Enemy:
    def __init__(self, x, y, speed, health, color, size, damage):
        # Base class for all enemy types
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.color = color
        self.size = size
        self.damage = damage

    def move(self, target_x, target_y):
        # Calculate direction towards target
        dx = target_x - self.x
        dy = target_y - self.y
        # Calculate distance to target
        distance = math.hypot(dx, dy)
        if distance > self.speed:
            # Move towards target at constant speed
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def attack(self, target):
        # To be implemented in subclasses
        pass

    def take_damage(self, amount):
        # Reduce health when damaged
        self.health -= amount

    def draw(self, screen):
        # Draw enemy as a colored rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))


class CrystalAggroEnemy(Enemy):
    def __init__(self, x, y, wave_number):
        # Crystal-focused enemy: slower, more health
        health = 3 + (wave_number - 1) // 5  # Health increases every 5 waves
        super().__init__(x, y, speed=1, health=health, color=(255, 0, 0), size=20, damage=1)

    def attack(self, crystal):
        # Damage the crystal when in range
        crystal.take_damage(self.damage)


class PlayerAggroEnemy(Enemy):
    def __init__(self, x, y, wave_number):
        # Player-focused enemy: faster, less health, ranged attack
        health = 2 + (wave_number - 1) // 5  # Health increases every 5 waves
        super().__init__(x, y, speed=2, health=health, color=(255, 165, 0), size=15, damage=1)
        self.attack_cooldown = 0
        self.attack_rate = 30  # Attack every 30 frames (0.5 seconds at 60 FPS)

    def attack(self, player):
        if self.attack_cooldown <= 0:
            # Create a pellet aimed at the player
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.hypot(dx, dy)
            direction = (dx / distance, dy / distance)
            self.attack_cooldown = self.attack_rate
            return Pellet(self.x, self.y, direction)
        return None

    def update(self):
        # Manage attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1


class Pellet:
    def __init__(self, x, y, direction):
        # Projectile fired by PlayerAggroEnemy
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 5
        self.size = 5
        self.color = (255, 255, 255)

    def move(self):
        # Move pellet in its direction
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

    def draw(self, screen):
        # Draw pellet as a small circle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
