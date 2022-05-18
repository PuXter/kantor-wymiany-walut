import socket
import threading
from currency import CurrencyData
import pickle

cd = CurrencyData()

#Dlugosc wiadomosci
HEADER = 16
#Port do wysylania wiadomosci
PORT = 8000
#IP serwera
SERVER = socket.gethostbyname(socket.gethostname())
#Struktura adresu
ADDR = (SERVER, PORT)
#Format kodowania
FORMAT = 'utf-8'
#Obecna liczba klientow
amount_of_clients = 0
#Ograniczona liczba klientow 
MAX_CLIENTS = 3
#Wiadomosc po ktorej klient zostaje rozlaczony
DISCONNECT_MSG = "!DISCONNECT"
#Wiadomosc po ktorej wysylana zostaje aktualizacja o danych walut
REQUEST_DATA_MSG = "!REQ_DATA"

#Stworzenie socketu serwera
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def allow_new_client(num):
    if(num < MAX_CLIENTS): return True
    else: return False

#Funkcja obslugujaca laczacych sie klientow
def handle_client(conn, addr, is_ok):
    global amount_of_clients
    #Odlaczenie klienta w przypadku osiagniecia maksymalnej ilosci klientow
    if(is_ok == False):
        print(f"[CONNETION] {addr} refused.")
        #Wyslanie klientowi informacji o odrzuceniu polaczenia
        data = pickle.dumps(False)
        conn.send(data)
        conn.close()
        return

    print(f"[NEW CONNETION] {addr} connected.")
    #Wyslanie klientowi informacji o przyjeciu polaczenia
    data = pickle.dumps(True)
    conn.send(data)
    connected = True
    while connected:
        #Odebranie dlugosci wiadomosci
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            #Dekodowanie wiadomosci
            msg = conn.recv(msg_length).decode(FORMAT)
            #Odlaczenie klienta po otrzymaniu wlasciwej wiadomosci
            if msg == DISCONNECT_MSG:
                connected = False
            #Przeslanie wiadomosci o walutach po otrzymaniu wlasciwej wiadomosci
            if msg == REQUEST_DATA_MSG:
                thread = threading.Thread(target=cd.getData())
                thread.start()
                data = pickle.dumps(cd.getCurrencies())
                conn.send(data)
        #Wypisanie logow
        print(f"[{addr}] - - {msg}")
    #Zmniejszenie liczby klientow
    amount_of_clients = amount_of_clients - 1
    #Zakonczenie polaczenia
    conn.close()

#Funkcja rozpoczynajca dzialanie serwera
def start():
    global amount_of_clients
    try:
        #Przyedzielenie adresu do serwera
        server.bind(ADDR)
        server.listen()
        print(f"[LISTENING] Server is listening in {SERVER}")
        while True:
            print(f"[ACTIVE CONNECTIONS] {amount_of_clients}")
            #Akceptowanie nadchodzacego polaczenia klienta
            con, addr = server.accept()
            if allow_new_client(amount_of_clients):
                #Kazdy klient jest oddzielnym watkiem
                thread = threading.Thread(target=handle_client, args=(con, addr,True))
                thread.start()
                #Zwiekszenie liczby klientow
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

#Info o dzialaniu serwera
print("[STARTING] server is starting...")
start()
