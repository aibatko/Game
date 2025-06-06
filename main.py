import random
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_f

from game import settings
from game.player import Player
from game.map import create_platforms
from game.weapon import Bullet
from game.enemy import Enemy


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    is_fullscreen = False

    player = Player(100, settings.SCREEN_HEIGHT - 100)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    platforms = create_platforms()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    enemy_spawn_time = 0
    SPAWN_DELAY = 2000  # milliseconds
    FIRE_DELAY = 300  # milliseconds between bullets
    last_shot_time = 0
    shooting = False
    mouse_target = (0, 0)

    running = True
    camera_x = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_f:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(
                        (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
                    )
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                shooting = True
                mouse_target = (event.pos[0] + camera_x, event.pos[1])
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                shooting = False

        if shooting:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time >= FIRE_DELAY:
                bullet = Bullet(
                    player.rect.centerx,
                    player.rect.centery,
                    mouse_target[0],
                    mouse_target[1],
                    owner=player,
                )
                bullets.add(bullet)
                all_sprites.add(bullet)
                last_shot_time = current_time

        player.update(platforms)
        bullets.update(platforms)
        enemies.update()

        # spawn enemies periodically
        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_time > SPAWN_DELAY:
            x = random.randint(50, settings.MAP_WIDTH - 50)
            enemy = Enemy(x, settings.SCREEN_HEIGHT - 40)
            enemies.add(enemy)
            all_sprites.add(enemy)
            enemy_spawn_time = current_time

        # check bullet collisions with enemies
        pygame.sprite.groupcollide(enemies, bullets, True, True)

        # update camera to follow the player
        camera_x = player.rect.centerx - settings.SCREEN_WIDTH // 2
        camera_x = max(0, min(camera_x, settings.MAP_WIDTH - settings.SCREEN_WIDTH))

        screen.fill(settings.WHITE)
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
        player.draw_health(screen)
        pygame.display.flip()
        clock.tick(settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
