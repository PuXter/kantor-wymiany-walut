import socket
import pickle
from currency import CurrencyData
from datetime import datetime
from currency import Currency 
from currency import SimpleCurrency 
from currency import Balance

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

#Tablica z uproszczonymi danymi do przeliczania
simple_currencies = []

#Tablica z przeliczonymi walutami
balance = []

#Funkcja sluzy do przeliczania walut
def count_currencies(c_amount, c_from,c_to):
    
    if not c_amount.isdigit():
        print("Error: Invalid given data")
        return -1

    if float(c_amount) <= 0 or c_from == c_to:
        print("Error: Invalid given data")
        return -1

    c_from=c_from.upper()
    c_to=c_to.upper()


    cf = SimpleCurrency()
    ct = SimpleCurrency()

    #Wyszukanie waluty w tablicy walut
    for data in simple_currencies:
        if(data.code==c_from):
            cf = data
        if(data.code==c_to):
            ct = data

    if(ct.code=="" or cf.code=="" or float(ct.value)==0.0 or float(cf.value)==0.0): 
        print("Error: Given currency code is invalid")
        return -1

    #Przeliczenie i wyswietlenie wyniku
    result = round( (float(c_amount) / float(cf.value)) * float(ct.value)  , 3)
    return result

def update_balance(c_amount, c_from,c_to):

    #Blad przy przeliczeniu walut jest bledem przy aktualizacji salda
    if count_currencies == -1:
        return -1
    
    if not c_amount.isdigit():
        print("Error: Invalid given data")
        return -1
    
    c_from=c_from.upper()
    c_to=c_to.upper()

    #Odnalezienie waluty w dostepnym saldzie do przewalutowania
    fb = Balance()
    for b in balance:
        if(c_from==b.code):
            fb.code=b.code
            fb.amount=b.amount
    
    #Brak odnalezienia waluty jest bledem
    if fb.code=="":
        print("There is no given currency in your balance")
        return -1
    
    #Aktualizacja waluty z ktorej pobieramy pieniadze do przewalutowania
    for b in balance:
        if(c_from==b.code):
            if b.amount == 0 or float(c_amount) > b.amount:
                print("Unable to perform changes in balance")
                return -1
            else:
                b.amount = b.amount - float(c_amount)
            
    result = count_currencies(c_amount, c_from,c_to)
    
    #Aktualizacja waluty do ktorej przewalutowujemy jesli widnieje w saldzie  
    for b in balance:
        if(c_to==b.code):
            b.amount = b.amount + result
            return
        
    #Aktualizacja waluty do ktorej przewalutowujemy jesli nie widnieje w saldzie  
    b = Balance()
    b.amount = result
    b.code = c_to.upper()
    balance.append(b)    

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
            c.code = str(res[2]) + " " + str(res[1])
            c.value = float(res[0])
            #Dodanie waluty do tablicy
            currencies.append(c)
            i = i + 1

#Funkcja upraszczajaca waluty do przeliczania
def simplify_currencies(curr):
    simple_currencies.clear()
    for data in curr:
        sc = SimpleCurrency()
        v = float(data.code.rsplit()[0])
        sc.value = round(v/data.value, 3)
        sc.code = data.code.rsplit()[1]
        simple_currencies.append(sc)
    pln = SimpleCurrency()
    pln.value = 1.0
    pln.code = "PLN"
    simple_currencies.append(pln)


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

#Funkcja wyswietlajaca stan salda
def show_balance():
    print("Current balance avaliable:")
    for b in balance:
        print(b)
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

msg_length = client.recv(102400)
if msg_length is not None:
    data = pickle.loads(msg_length)

if not data:
    send(DISCONNECT_MSG)
    print("Error: Unable to connect to server")
    print("Reason: Reached maximum numbers of clients")
    exit()

#Definicja i dodanie poczatkowego salda
start_balance = Balance()
start_balance.code = "PLN"
start_balance.amount = 10000.0
balance.append(start_balance)
#Proste menu klienta
menu()
show_balance()
inp = input("> ")
while(inp != "0"):
    #1 - aktualizacja danych o walutach
    if(inp=="1"):
        rec_msg = True
        send(REQUEST_DATA_MSG)
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        simplify_currencies(currencies)
    #2 - wyswietlenie danych o walutach
    elif(inp=="2"):
        if(len(simple_currencies) > 0):
            for cur in simple_currencies:
                print(cur)  
    #3 - przeliczanie podanych walut
    elif(inp=="3"):
        amount = input("How many? ")
        curr_from = input("From which currency? ")
        curr_to = input("To which currency? ")
        if count_currencies(amount,curr_from,curr_to) != -1: 
            update_balance(amount,curr_from,curr_to)
    else:
        rec_msg = False
        print("Error: Invalid command")
    menu()
    show_balance()
    inp = input("> ")

#Rozlaczenie po komendzie "0"
rec_msg = False
send(DISCONNECT_MSG)
