import pygame
from health_bar import HealthBar


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
