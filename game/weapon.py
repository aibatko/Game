import pygame

from . import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
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
        self.speed = 10 * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > settings.MAP_WIDTH:
            self.kill()
