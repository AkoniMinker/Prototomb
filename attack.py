import pygame
import math


class Attack:
    def __init__(self):
        self.radius = 0
        self.max_radius = 100  # Maximum radius of the attack circle
        self.is_active = False
        self.speed = 5  # Speed at which the attack circle expands
        self.color = (255, 165, 0)  # Orange color for the attack circle

    def start(self):
        # Initiate the attack if it's not already active
        if not self.is_active:
            self.is_active = True
            self.radius = 0

    def update(self):
        # Expand the attack circle if it's active
        if self.is_active:
            self.radius += self.speed
            # Deactivate the attack when it reaches max radius
            if self.radius >= self.max_radius:
                self.is_active = False
                self.radius = 0

    def draw(self, screen, center_x, center_y):
        # Draw the attack circle if it's active
        if self.is_active:
            # Calculate alpha (transparency) based on current radius
            # This creates a fading effect as the circle expands
            alpha = max(0, 255 - int(255 * self.radius / self.max_radius))
            attack_color = (*self.color, alpha)

            # Draw a circle with the calculated color and current radius
            pygame.draw.circle(screen, attack_color, (int(center_x), int(center_y)),
                               int(self.radius), 2)  # 2 is the width of the circle outline

    def check_collision(self, center_x, center_y, enemies):
        # Check if the attack collides with any enemies
        if self.is_active:
            for enemy in enemies[:]:  # Use a copy of the list to safely remove enemies
                # Calculate the center of the enemy
                enemy_center = (enemy.x + enemy.size / 2, enemy.y + enemy.size / 2)
                # Calculate distance between attack center and enemy center
                distance = math.hypot(center_x - enemy_center[0], center_y - enemy_center[1])
                # If the enemy is within the attack radius, remove it
                if distance <= self.radius:
                    enemies.remove(enemy)
