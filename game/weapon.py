import pygame

from . import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((20, 5))
        self.image.fill(settings.BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10 * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > settings.MAP_WIDTH:
            self.kill()
