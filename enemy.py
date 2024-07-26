import math
import pygame


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
