import pygame
from . import settings


def show_death_screen(screen):
    """Display a simple death screen and wait for the user to quit."""
    font = pygame.font.SysFont(None, 72)
    text = font.render("You Died", True, settings.RED)
    screen_rect = screen.get_rect()
    text_rect = text.get_rect(center=screen_rect.center)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
        screen.fill(settings.BLACK)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(100)

