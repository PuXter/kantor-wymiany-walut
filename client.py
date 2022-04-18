import socket
import pickle
from currency import CurrencyData
from datetime import datetime
from currency import Currency 

HEADER = 64
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

DISCONNECT_MSG = "!DISCONNECT"
REQUEST_DATA_MSG = "!REQ_DATA"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

REC_MSG = False

timestamp = ""

currencies = []

def update_currencies(data):
    currencies.clear()
    i = 0
    for line in reversed(data):
        if(i < 34):
            res = " ".join(reversed(line.split(" ")))
            res = res.split()
            c = Currency()
            c.name = line.rsplit(' 1',2)[0]  
            c.code = str(res[2]) + " " + str(res[1])
            c.value = float(res[0])
            currencies.append(c)
            i = i + 1

def menu():
    print()
    if(timestamp!=""):
        print(f"Last currency update {timestamp}")
    print()
    print("0 - Exit client")
    print("1 - Download currency data")
    print("2 - Show currency data")
    print()

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    if (REC_MSG):
        msg_length = client.recv(102400)
        if msg_length is not None:
            data = pickle.loads(msg_length)
            update_currencies(data)

menu()
inp = input("GIVE COMMAND ")
while(inp != "0"):
    if(inp=="1"):
        REC_MSG = True
        send(REQUEST_DATA_MSG)
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
    if(inp=="2"):
        if(len(currencies) > 0):
            for cur in currencies:
                print(cur)  
    else:
        REC_MSG = False
        send(inp)
    menu()
    inp = input("GIVE COMMAND ")

REC_MSG = False
send(DISCONNECT_MSG)
