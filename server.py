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

#Wiadomosc po ktorej klient zostaje rozlaczony
DISCONNECT_MSG = "!DISCONNECT"
#Wiadomosc po ktorej wysylana zostaje aktualizacja o danych walut
REQUEST_DATA_MSG = "!REQ_DATA"

#Stworzenie socketu serwera
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Przyedzielenie adresu do serwera
server.bind(ADDR)

#Funkcja obslugujaca laczacych sie klientow
def handle_client(conn, addr):
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
                cd.getData()
                data = pickle.dumps(cd.getCurrencies())
                conn.send(data)
        #Wypisanie logow
        print(f"[{addr}] - - {msg}")
    #Zakonczenie polaczenia
    conn.close()

#Funkcja rozpoczynajca dzialanie serwera
def start():
    server.listen()
    print(f"[LISTENING] Server is listening in {SERVER}")
    while True:
        #Akceptowanie nadchodzacego polaczenia klienta
        con, addr = server.accept()
        #Kazdy klient jest oddzielnym watkiem
        thread = threading.Thread(target=handle_client, args=(con, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

#Info o dzialaniu serwera
print("[STARTING] server is starting...")
start()
