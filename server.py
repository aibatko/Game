import random
import socket
import threading

HOST = '0.0.0.0'
PORT = 5001

clients = {}
player_colors = {}
next_id = 1
lock = threading.Lock()


def broadcast(message, sender=None):
    for cid, conn in list(clients.items()):
        if conn is sender:
            continue
        try:
            conn.sendall(message.encode('utf-8'))
        except Exception:
            with lock:
                del clients[cid]


def handle_client(conn, addr, player_id):
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # broadcast position to others with player id
                broadcast(f"{player_id}:{data.decode('utf-8')}", sender=conn)
    finally:
        with lock:
            if player_id in clients:
                del clients[player_id]
            if player_id in player_colors:
                del player_colors[player_id]
        broadcast(f"LEAVE:{player_id}\n")


def main():
    global next_id
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with lock:
                player_id = next_id
                next_id += 1
                # capture ids of players that were already connected
                existing_ids = list(clients.keys())
                clients[player_id] = conn
                color = random.choice([
                    "0,0,255",    # blue
                    "255,0,0",    # red
                    "0,255,0",    # green
                    "255,255,0",  # yellow
                    "255,165,0",  # orange
                    "128,0,128",  # purple
                ])
                player_colors[player_id] = color

            # send the assigned id before any other messages
            try:
                conn.sendall(f"ID:{player_id}:{color}\n".encode('utf-8'))
            except Exception:
                conn.close()
                continue

            # inform the new client about players already in the game
            for pid in existing_ids:
                try:
                    conn.sendall(
                        f"JOIN:{pid}:{player_colors[pid]}\n".encode('utf-8')
                    )
                except Exception:
                    pass

            thread = threading.Thread(target=handle_client, args=(conn, addr, player_id), daemon=True)
            thread.start()
            broadcast(f"JOIN:{player_id}:{color}\n", sender=conn)


if __name__ == '__main__':
    main()
