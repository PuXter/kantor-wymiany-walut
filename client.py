import socket
import pickle
from currency import CurrencyData

# cd = CurrencyData()
HEADER = 64
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNEXT_MSG = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


# cd.getData()
# cd.showData()

while True:
    msg_length = client.recv(102400)
    if msg_length is not None:
        data = pickle.loads(msg_length)
        for x in data:
            print(x)
        break


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


send("MESS1")
input()
send("MESS2")
input()
send("MESS3")
input()
send("!DISCONNECT")
