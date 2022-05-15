import socket
import pickle
from currency import CurrencyData
from datetime import datetime
from currency import Currency 

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

#Stworzenie socketu klienta
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Flaga oczekiwania na wiadomosc
rec_msg = False

#Wiadomosc o ostatniej aktualizacji danych walut
timestamp = ""

#Tablica z danymi o walutach
currencies = []

#Funkcja sluzy do przeliczania zlotowek na podana ilosc podanej waluty
def count_currencies(c_amount, c_to):
    ct = Currency()
    #Wyszukanie waluty w tablicy walut
    for data in currencies:
        if(data.code==c_to):
            ct = data
            print(f"Currency: {data}")
    if(ct.code==""): 
        print("Error: Given currency code is invalid")
        return
    #Przeliczenie i wyswietlenie wyniku
    result = round(float(c_amount) / float(ct.value), 3)
    print(f"{c_amount} PLN = {result} {c_to}")
    

#Funkcja do aktualizacji danych o walutach
def update_currencies(data):
    currencies.clear()
    i = 0
    #Czytanie ostatnich danych
    for line in reversed(data):
        if(i < 34):
            #Wyluskanie odpowidnich informacji z tekstu
            res = " ".join(reversed(line.split(" ")))
            res = res.split()
            #Stworzenie obiektu waluty
            c = Currency()
            c.name = line.rsplit(' 1',2)[0]  
            c.code = str(res[1])
            c.value = float(res[0])
            #Dodanie waluty do tablicy
            currencies.append(c)
            i = i + 1

#Funkjca wyswietlajaca menu dla klienta
def menu():
    print()
    if(timestamp!=""):
        print(f"Last currency update {timestamp}")
    print()
    print("0 - Exit client")
    print("1 - Download currency data")
    print("2 - Show currency data")
    print("3 - Count currencies")
    print()

#Funkcja wysylajaca wiadomosc do serwera
def send(msg):
    try:
        #Kodowanie wiadomosci
        message = msg.encode(FORMAT)
        #Dlugosc wiadomosci
        msg_length = len(message)
        #Wyslanie dlugosci tekstu
        send_length = str(msg_length).encode(FORMAT)
        #Dodanie ew brakujących bitów do wiadomosci dlugosci tekstu
        send_length += b' ' * (HEADER - len(send_length))
        #Wyslanie informacji o dlugosci wiadomosci
        client.send(send_length)
        #Wyslanie wiadmosci
        client.send(message)
        #Jesli flaga rec_msg ustawiona na true (przygotowanie do odebrania wiadomosci od serwera)
        if (rec_msg):
            #Dlugosc pobranej wiadomosci
            msg_length = client.recv(102400)
            if msg_length is not None:
                #Zaladowanie danych o walutach
                data = pickle.loads(msg_length)
                #Zaktualizowanie danych klienta o walutach
                update_currencies(data)
    except BrokenPipeError:
        print("Error: Connection with server has been broken")
        exit()

#Polaczenie z serwerem
try:
    client.connect(ADDR)
except ConnectionRefusedError:
    print("Error: Unable to contact server")
    exit()

#Proste menu klienta
menu()
inp = input("GIVE COMMAND ")
while(inp != "0"):
    #1 - aktualizacja danych o walutach
    if(inp=="1"):
        rec_msg = True
        send(REQUEST_DATA_MSG)
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
    #2 - wyswietlenie danych o walutach
    if(inp=="2"):
        if(len(currencies) > 0):
            for cur in currencies:
                print(cur)  
    #3 - przeliczanie zlotowek na podana walute
    if(inp=="3"):
        amount = input("How many? ")
        curr = input("To which currency? ")
        count_currencies(amount,curr)
    #reszta - echo do testow
    else:
        rec_msg = False
        print("Error: Invalid command")
    menu()
    inp = input("GIVE COMMAND ")

#Rozlaczenie po komendzie "0"
rec_msg = False
send(DISCONNECT_MSG)
