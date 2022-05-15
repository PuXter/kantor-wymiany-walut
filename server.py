import socket
import threading
from currency import CurrencyData
import pickle

cd = CurrencyData()

#Dlugosc wiadomosci
HEADER = 64
#Port do wysylania wiadomosci
PORT = 8000
#IP serwera
SERVER = socket.gethostbyname(socket.gethostname())
#Struktura adresu
ADDR = (SERVER, PORT)
#Format kodowania
FORMAT = 'utf-8'

#Ograniczona liczba klienow 
MAX_CLIENTS = 3
#Wiadomosc po ktorej klient zostaje rozlaczony
DISCONNECT_MSG = "!DISCONNECT"
#Wiadomosc po ktorej wysylana zostaje aktualizacja o danych walut
REQUEST_DATA_MSG = "!REQ_DATA"

#Stworzenie socketu serwera
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Przyedzielenie adresu do serwera
server.bind(ADDR)

def allow_new_client(num):
    if(num < MAX_CLIENTS): return True
    else: return False

#Funkcja obslugujaca laczacych sie klientow
def handle_client(conn, addr, is_ok):

    if(is_ok == False):
        #conn.send("CONN_REFUSED")
        print(f"[CONNETION] {addr} refused.")
        conn.close()
        return

    print(f"[NEW CONNETION] {addr} connected.")
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
    #Zakonczenie polaczenia
    conn.close()

#Funkcja rozpoczynajca dzialanie serwera
def start():
    try:
        server.listen()
        print(f"[LISTENING] Server is listening in {SERVER}")
        while True:
            if(allow_new_client(threading.active_count() - 1) == True):
                #Akceptowanie nadchodzacego polaczenia klienta
                con, addr = server.accept()
                #Kazdy klient jest oddzielnym watkiem
                thread = threading.Thread(target=handle_client, args=(con, addr,True))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            else:
                con, addr = server.accept()
                thread = threading.Thread(target=handle_client, args=(con, addr,False))
                thread.start()
    except KeyboardInterrupt:
        server.close()
        print()
        print("Server has been closed")
        return


#Info o dzialaniu serwera
print("[STARTING] server is starting...")
start()
