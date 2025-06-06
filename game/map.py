import pygame

from .platform import Platform
from . import settings


def create_platforms():
    platforms = pygame.sprite.Group()

    ground_y = settings.SCREEN_HEIGHT - 40

    # ----- ground with gaps -----
    segment_width = 400
    gap_width = 120
    x = 0
    count = 0
    while x < settings.MAP_WIDTH:
        width = min(segment_width, settings.MAP_WIDTH - x)
        platforms.add(Platform(x, ground_y, width, 40))
        x += width
        count += 1
        if count % 2 == 0 and x + gap_width < settings.MAP_WIDTH:
            # leave a hole in the ground
            x += gap_width

    # ----- floating platforms and pillars -----
    for i in range(200, settings.MAP_WIDTH, 600):
        platforms.add(Platform(i, ground_y - 60, 80, 20))
        platforms.add(Platform(i + 100, ground_y - 140, 100, 20))
        platforms.add(Platform(i + 220, ground_y - 220, 120, 20))

    for i in range(500, settings.MAP_WIDTH, 800):
        platforms.add(Platform(i, ground_y - 100, 40, 100))

    return platforms
