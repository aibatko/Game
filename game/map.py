import pygame

from .platform import Platform
from . import settings


def create_platforms():
    platforms = pygame.sprite.Group()

    # ground spanning the entire map width
    ground = Platform(0, settings.SCREEN_HEIGHT - 40, settings.MAP_WIDTH, 40)
    platforms.add(ground)

    # scatter some additional platforms across the map
    step = 300
    for i in range(1, settings.MAP_WIDTH // step):
        x = i * step
        platforms.add(Platform(x, settings.SCREEN_HEIGHT - 150, 120, 20))
        if i % 2 == 0:
            platforms.add(Platform(x + 150, settings.SCREEN_HEIGHT - 250, 120, 20))

    return platforms
