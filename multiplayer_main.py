import socket
import threading
import pygame
from pygame.locals import QUIT, KEYDOWN, K_f

from game import settings
from game.player import Player
from game.map import create_platforms
from game.weapon import Bullet

HOST = '127.0.0.1'
PORT = 5000


class NetworkClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.player_id = None
        self.running = True
        self.callbacks = []

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        # receive our id
        data = self.socket.recv(1024).decode('utf-8').strip()
        if data.startswith('ID:'):
            self.player_id = int(data.split(':')[1])
        thread = threading.Thread(target=self._listen, daemon=True)
        thread.start()

    def _listen(self):
        while self.running:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                for line in data.decode('utf-8').splitlines():
                    for cb in self.callbacks:
                        cb(line)
            except Exception:
                break
        self.running = False

    def send_position(self, x, y):
        try:
            self.socket.sendall(f"{x},{y}\n".encode('utf-8'))
        except Exception:
            self.running = False

    def close(self):
        self.running = False
        if self.socket:
            self.socket.close()


class RemotePlayer(Player):
    def __init__(self):
        super().__init__(0, 0)
        self.image.fill((255, 0, 0))
        self.speed = 0

    def update(self, *_):
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    client = NetworkClient(HOST, PORT)
    client.connect()

    player = Player(100, settings.SCREEN_HEIGHT - 100)
    bullets = pygame.sprite.Group()
    platforms = create_platforms()

    remote_players = {}

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    def handle_network(message):
        if message.startswith('JOIN:'):
            pid = int(message.split(':')[1])
            if pid != client.player_id:
                rp = RemotePlayer()
                remote_players[pid] = rp
                all_sprites.add(rp)
        elif message.startswith('LEAVE:'):
            pid = int(message.split(':')[1])
            rp = remote_players.pop(pid, None)
            if rp:
                all_sprites.remove(rp)
        else:
            try:
                pid, rest = message.split(':')
                pid = int(pid)
                if pid == client.player_id:
                    return
                x_str, y_str = rest.split(',')
                rp = remote_players.get(pid)
                if rp:
                    rp.rect.topleft = (int(x_str), int(float(y_str)))
            except ValueError:
                pass

    client.callbacks.append(handle_network)

    running = True
    while running and client.running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_f:
                bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
                bullets.add(bullet)
                all_sprites.add(bullet)

        player.update(platforms)
        bullets.update()

        client.send_position(player.rect.x, player.rect.y)

        screen.fill(settings.WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(settings.FPS)

    client.close()
    pygame.quit()


if __name__ == "__main__":
    main()
