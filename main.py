import pygame
from pygame.locals import *

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
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
        self.vel_y += GRAVITY

        # horizontal movement
        self.rect.x += self.vel_x
        self.collide(self.vel_x, 0, platforms)

        # vertical movement
        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide(0, self.vel_y, platforms)

    def collide(self, vel_x, vel_y, platforms):
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

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((20, 5))
        self.image.fill((150, 75, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10 * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, SCREEN_HEIGHT - 100)
    arrows = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # simple ground platform
    ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
    platforms.add(ground)

    # additional platforms
    platforms.add(Platform(200, SCREEN_HEIGHT - 150, 120, 20))
    platforms.add(Platform(400, SCREEN_HEIGHT - 250, 120, 20))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_f:
                arrow = Arrow(player.rect.centerx, player.rect.centery, player.direction)
                arrows.add(arrow)
                all_sprites.add(arrow)

        player.update(platforms)
        arrows.update()

        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
