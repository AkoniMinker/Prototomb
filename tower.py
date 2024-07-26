import pygame
import math


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
