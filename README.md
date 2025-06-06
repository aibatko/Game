# Simple Platformer Game

This repository contains a small platformer game built with Python and Pygame. It has been refactored into several modules for easier development:

- `game/player.py` – the player sprite and movement logic
- `game/map.py` – creation of the level platforms
- `game/weapon.py` – simple projectile weapon
- `game/settings.py` – configuration constants
- `game/enemy.py` – enemy sprites that can be shot

The game currently supports:

- Basic player movement (left, right, and jumping)
- Simple gravity and collision with platforms
- Shooting bullets with the left mouse button
- A few example platforms for parkour
- Enemies that spawn periodically and can be destroyed with bullets
- A scrolling camera that follows the player
- A much larger map with additional platforms
- Randomly colored player shirts in multiplayer mode
- Bullets deal damage to other players in multiplayer and a simple death screen
  appears when your health reaches zero

## Running the game

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the game:
   ```bash
   python main.py
   ```

Use `A` and `D` to move left and right, `W` to jump, and click with the left mouse button to shoot toward the cursor.

Further improvements, including multiplayer features, may be added later.

## Multiplayer Server

A simple TCP server is included for experimental multiplayer support.

1. Start the server:
   ```bash
   python server.py
   ```
2. Run the multiplayer client on any machine in the same network. Specify the
   server's IP address if it is running on a different machine:
   ```bash
   python multiplayer_main.py --host <SERVER_IP>
   ```

Each running client connects to the server and shares player positions with
others.
