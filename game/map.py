import pygame

from .platform import Platform
from . import settings


def create_platforms():
    platforms = pygame.sprite.Group()
    # simple ground
    ground = Platform(0, settings.SCREEN_HEIGHT - 40, settings.SCREEN_WIDTH, 40)
    platforms.add(ground)

    # additional platforms
    platforms.add(Platform(200, settings.SCREEN_HEIGHT - 150, 120, 20))
    platforms.add(Platform(400, settings.SCREEN_HEIGHT - 250, 120, 20))
    return platforms
