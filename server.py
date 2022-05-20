import socket
import threading
from currency import CurrencyData
import pickle

cd = CurrencyData()

#Message length 
HEADER = 16
#Port which will be used to transport messages
PORT = 8000
#Sever IP
SERVER = socket.gethostbyname(socket.gethostname())
#Address structure
ADDR = (SERVER, PORT)
#Coding format
FORMAT = 'utf-8'
#Current amount of clients
amount_of_clients = 0
#Limited number of clients
MAX_CLIENTS = 3
#Message after which client is disconnected
DISCONNECT_MSG = "!DISCONNECT"
#The message after which the update of the given currencies is sent
REQUEST_DATA_MSG = "!REQ_DATA"

#Define server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Function checks if more clients can be allowed
def allow_new_client(num):
    if(num < MAX_CLIENTS): return True
    else: return False

#Function handles connecting clients
def handle_client(conn, addr, is_ok):
    global amount_of_clients
    #Disconnecting the customer if the maximum number of customers is reached
    if(is_ok == False):
        print(f"[CONNETION] {addr} refused.")
        #Sending the customer information about the rejection of connection
        data = pickle.dumps(False)
        conn.send(data)
        conn.close()
        return

    print(f"[NEW CONNETION] {addr} connected.")
    #Sending the customer information about accepting connection
    data = pickle.dumps(True)
    conn.send(data)
    connected = True
    while connected:
        #Receiving message length
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            #Message decoding
            msg = conn.recv(msg_length).decode(FORMAT)
            #Disconnecting the customer after receiving disconnect message
            if msg == DISCONNECT_MSG:
                connected = False
            #Sending currency messages after receiving request message
            if msg == REQUEST_DATA_MSG:
                thread = threading.Thread(target=cd.getData())
                thread.start()
                data = pickle.dumps(cd.getCurrencies())
                conn.send(data)
        #Print logs
        print(f"[{addr}] - - {msg}")
    #Decrease anmount of clients
    amount_of_clients = amount_of_clients - 1
    #Close connection
    conn.close()

#Function starts server
def start():
    global amount_of_clients
    try:
        #Binding server address
        server.bind(ADDR)
        server.listen()
        print(f"[LISTENING] Server is listening in {SERVER}")
        while True:
            print(f"[ACTIVE CONNECTIONS] {amount_of_clients}")
            #Accepting the upcoming client connection
            con, addr = server.accept()
            if allow_new_client(amount_of_clients):
                #Every client is a thread
                thread = threading.Thread(target=handle_client, args=(con, addr,True))
                thread.start()
                #Increasing amount of clients
                amount_of_clients = amount_of_clients + 1
            else:
                thread = threading.Thread(target=handle_client, args=(con, addr,False))
                thread.start()
    except KeyboardInterrupt:
        server.close()
        print()
        print("Server has been closed")
        exit()
    except OSError:
        print("Error: Unable to start server on given address")
        print("Note: If you're trying to restart server, wait few minutes and try to run it again")
        return

#Starting a server
print("[STARTING] server is starting...")
start()
