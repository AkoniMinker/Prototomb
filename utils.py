import pygame
import math


# shop
class Shop:
    def __init__(self):
        # Dictionary to store available items and their costs
        self.items = {
            "Basic Tower": 100,
            "Health Potion": 50,
            "Damage Boost": 75
        }

    def buy_item(self, item_name, player):
        # Check if the requested item is available in the shop
        if item_name in self.items:
            # Get the cost of the item
            cost = self.items[item_name]

            # Check if the player has enough points to buy the item
            if player.score >= cost:
                # Deduct the cost from the player's score
                player.score -= cost

                # Add the item to the player's inventory
                player.collect_item(item_name)

                # Inform the player that the item was bought successfully
                print(f"Bought {item_name}")
            else:
                # Inform the player that they don't have enough points
                print("Not enough points to buy this item")
        else:
            # Inform the player that the requested item is not available
            print("Item not available in the shop")


# attack

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


# health bar

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
