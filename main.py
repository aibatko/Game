import pygame
from pygame.locals import QUIT, KEYDOWN, K_f

from game import settings
from game.player import Player
from game.map import create_platforms
from game.weapon import Bullet


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, settings.SCREEN_HEIGHT - 100)
    bullets = pygame.sprite.Group()
    platforms = create_platforms()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_f:
                # spawn bullet at the front of the player depending on the direction
                if player.direction > 0:
                    bullet_x = player.rect.right
                else:
                    bullet_x = player.rect.left
                bullet = Bullet(bullet_x, player.rect.centery, player.direction)
                bullets.add(bullet)
                all_sprites.add(bullet)

        player.update(platforms)
        bullets.update()

        screen.fill(settings.WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
