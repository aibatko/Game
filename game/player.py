import random
import pygame
from pygame.locals import K_a, K_d, K_w

from . import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color=None):
        super().__init__()
        # pick a random shirt color if one is not provided
        self.color = color or random.choice(settings.PLAYER_COLORS)

        # create a simple pixel art player with transparent background
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        # head
        pygame.draw.rect(self.image, settings.YELLOW, (15, 5, 10, 10))
        # body
        pygame.draw.rect(self.image, self.color, (12, 20, 16, 20))
        # arms
        pygame.draw.rect(self.image, settings.BLACK, (8, 20, 4, 15))
        pygame.draw.rect(self.image, settings.BLACK, (28, 20, 4, 15))
        # legs
        pygame.draw.rect(self.image, settings.BLACK, (14, 40, 6, 15))
        pygame.draw.rect(self.image, settings.BLACK, (20, 40, 6, 15))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        # slightly higher jump to make parkour easier
        self.jump_power = 14
        self.on_ground = False
        self.direction = 1  # 1=right, -1=left
        self.max_health = settings.MAX_HEALTH
        self.health = self.max_health

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[K_a]:
            self.vel_x = -self.speed
            self.direction = -1
        if keys[K_d]:
            self.vel_x = self.speed
            self.direction = 1
        if keys[K_w] and self.on_ground:
            self.vel_y = -self.jump_power

        # apply gravity
        self.vel_y += settings.GRAVITY

        # horizontal movement
        self.rect.x += self.vel_x
        self._collide(self.vel_x, 0, platforms)
        # keep player within map bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.MAP_WIDTH:
            self.rect.right = settings.MAP_WIDTH

        # vertical movement
        self.rect.y += self.vel_y
        self.on_ground = False
        self._collide(0, self.vel_y, platforms)

    def _collide(self, vel_x, vel_y, platforms):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if vel_x > 0:
                    self.rect.right = p.rect.left
                if vel_x < 0:
                    self.rect.left = p.rect.right
                if vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                if vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

    def draw_health(self, surface):
        """Draw a simple health bar in the top-left corner."""
        for i in range(self.max_health):
            color = settings.RED if i < self.health else settings.GRAY
            x = 10 + i * 18
            pygame.draw.rect(surface, color, (x, 10, 16, 16))
