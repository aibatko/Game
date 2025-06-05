import pygame

from . import settings


class Enemy(pygame.sprite.Sprite):
    """Simple enemy that can be shot by bullets."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(settings.RED)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

    def update(self):
        """Placeholder for future movement."""
        pass
