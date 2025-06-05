import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE

from . import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(settings.BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 10
        self.on_ground = False
        self.direction = 1  # 1=right, -1=left

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[K_LEFT]:
            self.vel_x = -self.speed
            self.direction = -1
        if keys[K_RIGHT]:
            self.vel_x = self.speed
            self.direction = 1
        if keys[K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power

        # apply gravity
        self.vel_y += settings.GRAVITY

        # horizontal movement
        self.rect.x += self.vel_x
        self._collide(self.vel_x, 0, platforms)

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
