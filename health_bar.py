import pygame


class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        # Position of the health bar
        self.x = x
        self.y = y

        # Dimensions of the health bar
        self.width = width
        self.height = height

        # Maximum health value (full bar)
        self.max_health = max_health

        # Current health value (starts at max_health)
        self.current_health = max_health

    def update(self, current_health):
        # Update the current health, ensuring it stays between 0 and max_health
        self.current_health = max(0, min(current_health, self.max_health))

    def draw(self, screen):
        # Calculate the ratio of current health to max health
        ratio = self.current_health / self.max_health

        # Draw the background (red bar) representing total health
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

        # Draw the foreground (green bar) representing current health
        # The width of this bar is proportional to the health ratio
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, int(self.width * ratio), self.height))
