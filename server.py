import socket
import threading
import pickle
from currency import CurrencyData

CD = CurrencyData()

#Port which will be used to transport messages
PORT = 8000
#Sever IP
SERVER_IP = socket.gethostbyname(socket.gethostname())
#Address structure
ADDR = (SERVER_IP, PORT)
#Current amount of clients
AMOUNT_OF_CLIENTS = 0
#Limited number of clients
MAX_CLIENTS = 3
#Message after which client is disconnected
DISCONNECT_MSG = "!DISCONNECT"
#The message after which the update of the given currencies is sent
REQUEST_DATA_MSG = "!REQ_DATA"
#Message which defines a broken connection
BROKEN_CONNECTION = "!BROKEN_CONNECTION"

#Define server socket
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Function checks if more clients can be allowed
def allow_new_client(num):
    if num < MAX_CLIENTS: 
        return True
    return False

#Function handles connecting clients
def handle_client(conn, addr, is_ok):
    global AMOUNT_OF_CLIENTS
    global msg
    #Disconnecting the customer if the maximum number of customers is reached
    if not is_ok:
        print(f"[CONNETION] {addr} refused.")
        #Sending the customer information about the rejection of connection
        data = pickle.dumps(False)
        conn.send(data)
        conn.close()
        return

    print(f"[NEW CONNETION] {addr} connected.")
    #Sending client information about accepting connection
    data = pickle.dumps(True)
    conn.send(data)
    
    connected = True
    while connected:
        try:
            #Receiving message length
            msg_length = conn.recv(102400)  
            if msg_length:
                msg = pickle.loads(msg_length)
                #Disconnecting the customer after receiving disconnect message
                if msg == DISCONNECT_MSG:
                    connected = False
                #Sending currency messages after receiving request message
                if msg == REQUEST_DATA_MSG:
                    thread = threading.Thread(target=CD.get_data())
                    thread.start()
                    data = pickle.dumps(CD.get_currencies())
                    conn.send(data)
            #Print logs
            print(f"[{addr}] - - {msg}")
            #Handles broken connection
            if msg == BROKEN_CONNECTION:
                AMOUNT_OF_CLIENTS = AMOUNT_OF_CLIENTS - 1
                conn.close()
                return
            msg = BROKEN_CONNECTION
        except (UnboundLocalError):
            AMOUNT_OF_CLIENTS = AMOUNT_OF_CLIENTS - 1
            conn.close()
            return
    #Decrease anmount of clients
    AMOUNT_OF_CLIENTS = AMOUNT_OF_CLIENTS - 1
    #Close connection
    conn.close()

#Function starts server
def start():
    global AMOUNT_OF_CLIENTS
    try:
        #Binding server address
        SERVER.bind(ADDR)
        SERVER.listen()
        print(f"[LISTENING] Server is listening in {SERVER_IP}")
        while True:
            print(f"[ACTIVE CONNECTIONS] {AMOUNT_OF_CLIENTS}")
            #Accepting the upcoming client connection
            con, addr = SERVER.accept()
            if allow_new_client(AMOUNT_OF_CLIENTS):
                #Every client is a thread
                thread = threading.Thread(target=handle_client, args=(con, addr, True))
                thread.start()
                #Increasing amount of clients
                AMOUNT_OF_CLIENTS = AMOUNT_OF_CLIENTS + 1
            else:
                thread = threading.Thread(target=handle_client, args=(con, addr, False))
                thread.start()
    except KeyboardInterrupt:
        SERVER.close()
        print()
        print("Server has been closed")
        exit()
    except OSError:
        print("Error: Unable to start server on given address")
        print("Note: If you're trying to restart server, wait few minutes and try to run it again")
        return

if __name__ == '__main__':
    #Starting a server
    print("[STARTING] server is starting...")
    start()
