import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

clients = {}
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
    conn.sendall(f"ID:{player_id}\n".encode('utf-8'))
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

            # inform the new client about players already in the game
            for pid in existing_ids:
                try:
                    conn.sendall(f"JOIN:{pid}\n".encode('utf-8'))
                except Exception:
                    pass

            thread = threading.Thread(target=handle_client, args=(conn, addr, player_id), daemon=True)
            thread.start()
            broadcast(f"JOIN:{player_id}\n", sender=conn)


if __name__ == '__main__':
    main()
