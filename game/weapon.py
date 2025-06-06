import math
import pygame

from . import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, owner=None):
        super().__init__()
        # create a small pixel art bullet
        self.image = pygame.Surface((12, 4), pygame.SRCALPHA)
        # body of the bullet
        pygame.draw.rect(self.image, settings.BROWN, (0, 0, 9, 4))
        # highlight lines
        pygame.draw.line(self.image, settings.YELLOW, (2, 1), (7, 1))
        pygame.draw.line(self.image, settings.YELLOW, (2, 2), (7, 2))
        # tip of the bullet
        pygame.draw.polygon(self.image, settings.RED, [(9, 0), (12, 2), (9, 4)])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.owner = owner

        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy) or 1
        # slow down bullet travel speed a bit so projectiles are easier to follow
        speed = 5
        self.vel_x = speed * dx / dist
        self.vel_y = speed * dy / dist

    def update(self, platforms=None):
        """Move the bullet and destroy it on collisions or when off-screen."""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # remove bullet if it collides with any platform
        if platforms:
            for p in platforms:
                if self.rect.colliderect(p.rect):
                    self.kill()
                    return

        # remove bullet if it flies outside the visible area
        if (
            self.rect.right < 0
            or self.rect.left > settings.MAP_WIDTH
            or self.rect.bottom < 0
            or self.rect.top > settings.SCREEN_HEIGHT
        ):
            self.kill()
