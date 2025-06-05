import pygame

from . import settings


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(settings.BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
