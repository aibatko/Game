import socket
import threading
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_f

from game import settings
from game.player import Player
from game.map import create_platforms
from game.weapon import Bullet

HOST = '127.0.0.1'
PORT = 5001


class NetworkClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.player_id = None
        self.color = None
        self.running = True
        self.callbacks = []
        # store messages received when no callbacks are registered yet
        self._pending = []

    def add_callback(self, callback):
        """Register a callback and flush any queued messages."""
        self.callbacks.append(callback)
        if self._pending:
            for msg in list(self._pending):
                callback(msg)
            self._pending.clear()

    def _dispatch(self, message):
        if self.callbacks:
            for cb in self.callbacks:
                cb(message)
        else:
            self._pending.append(message)

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        # receive our id, handling possible interleaved messages
        buffer = ""
        while True:
            chunk = self.socket.recv(1024).decode('utf-8')
            if not chunk:
                raise ConnectionError("Server closed before sending ID")
            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line.startswith("ID:"):
                    _, pid, color = line.split(":", 2)
                    self.player_id = int(pid)
                    self.color = tuple(map(int, color.split(',')))
                    thread = threading.Thread(target=self._listen, daemon=True)
                    thread.start()
                    if buffer:
                        # buffer may contain additional messages
                        for extra in buffer.split('\n'):
                            if extra:
                                self._dispatch(extra)
                    return
                else:
                    self._dispatch(line)

    def _listen(self):
        buffer = ""
        while self.running:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                buffer += data.decode('utf-8')
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self._dispatch(line)
            except Exception:
                break
        self.running = False

    def send_position(self, x, y):
        try:
            self.socket.sendall(f"{x},{y}\n".encode('utf-8'))
        except Exception:
            self.running = False

    def send_bullet(self, x, y, target_x, target_y):
        try:
            self.socket.sendall(f"BULLET:{x},{y},{target_x},{target_y}\n".encode('utf-8'))
        except Exception:
            self.running = False

    def close(self):
        self.running = False
        if self.socket:
            self.socket.close()


class RemotePlayer(Player):
    def __init__(self, color):
        super().__init__(0, 0, color)
        self.speed = 0

    def update(self, *_):
        pass


class MultiplayerScene:
    """Container for multiplayer game objects."""

    def __init__(self, player, platforms):
        self.player = player
        self.remote_players = {}
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(player)
        self.all_sprites.add(platforms)

    def draw(self, surface, camera_x=0):
        """Draw all sprites offset by the camera position."""
        for sprite in self.all_sprites:
            surface.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

    def add_remote_player(self, pid, color):
        rp = RemotePlayer(color)
        self.remote_players[pid] = rp
        self.all_sprites.add(rp)
        return rp

    def remove_remote_player(self, pid):
        rp = self.remote_players.pop(pid, None)
        if rp:
            self.all_sprites.remove(rp)
        return rp

    def spawn_bullet(self, x, y, target_x, target_y):
        bullet = Bullet(x, y, target_x, target_y)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
        return bullet


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    client = NetworkClient(HOST, PORT)
    client.connect()

    player = Player(100, settings.SCREEN_HEIGHT - 100, client.color)
    platforms = create_platforms()
    scene = MultiplayerScene(player, platforms)

    def handle_network(message):
        if message.startswith('JOIN:'):
            _, pid_str, color_str = message.split(':', 2)
            pid = int(pid_str)
            color = tuple(map(int, color_str.split(',')))
            if pid != client.player_id:
                scene.add_remote_player(pid, color)
        elif message.startswith('LEAVE:'):
            pid = int(message.split(':')[1])
            scene.remove_remote_player(pid)
        else:
            try:
                pid, rest = message.split(':', 1)
                pid = int(pid)
                if pid == client.player_id:
                    return
                if rest.startswith('BULLET:'):
                    bullet_data = rest.split('BULLET:', 1)[1]
                    x_str, y_str, tx_str, ty_str = bullet_data.split(',')
                    scene.spawn_bullet(
                        int(x_str),
                        int(float(y_str)),
                        int(tx_str),
                        int(float(ty_str)),
                    )
                else:
                    x_str, y_str = rest.split(',')
                    rp = scene.remote_players.get(pid)
                    if rp:
                        rp.rect.topleft = (int(x_str), int(float(y_str)))
            except ValueError:
                pass

    client.add_callback(handle_network)

    FIRE_DELAY = 300  # milliseconds
    last_shot_time = 0
    shooting = False
    mouse_target = (0, 0)

    running = True
    camera_x = 0
    while running and client.running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                shooting = True
                mouse_target = (event.pos[0] + camera_x, event.pos[1])
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                shooting = False

        if shooting:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time >= FIRE_DELAY:
                scene.spawn_bullet(
                    player.rect.centerx,
                    player.rect.centery,
                    mouse_target[0],
                    mouse_target[1],
                )
                client.send_bullet(
                    player.rect.centerx,
                    player.rect.centery,
                    mouse_target[0],
                    mouse_target[1],
                )
                last_shot_time = current_time

        player.update(platforms)
        scene.bullets.update()

        client.send_position(player.rect.x, player.rect.y)

        # update camera to follow the local player
        camera_x = player.rect.centerx - settings.SCREEN_WIDTH // 2
        camera_x = max(0, min(camera_x, settings.MAP_WIDTH - settings.SCREEN_WIDTH))

        screen.fill(settings.WHITE)
        scene.draw(screen, camera_x)
        pygame.display.flip()
        clock.tick(settings.FPS)

    client.close()
    pygame.quit()


if __name__ == "__main__":
    main()
