import socket
import threading
from currency import CurrencyData
import pickle

cd = CurrencyData()

HEADER = 64
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

DISCONNECT_MSG = "!DISCONNECT"
REQUEST_DATA_MSG = "!REQ_DATA"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNETION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            if msg == REQUEST_DATA_MSG:
                cd.getData()
                data = pickle.dumps(cd.getCurrencies())
                conn.send(data)
        print(f"[{addr}] - - {msg}")

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening in {SERVER}")
    while True:
        con, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(con, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
