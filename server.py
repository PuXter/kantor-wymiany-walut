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
DISCONNEXT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# def send_currency(curr):
#     message = curr.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     server.send(send_length)
#     server.send(message)


def handle_client(conn, addr):
    print(f"[NEW CONNETION] {addr} connected.")
    cd.getData()
    data = pickle.dumps(cd.getCurrencies())
    conn.send(data)
    # for cur in cd:
    #     # send_currency(str(cur))
    # print
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNEXT_MSG:
                connected = False
            print(f"[{addr}]{msg}")

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
