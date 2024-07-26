import pygame
import math
from attack import Attack
from health_bar import HealthBar


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
