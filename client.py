import socket
import pickle
from datetime import datetime
from currency import Currency
from currency import SimpleCurrency
from currency import Balance

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

#Message after which client will be disconnected from server
DISCONNECT_MSG = "!DISCONNECT"
#Message after which client will recieve currency update
REQUEST_DATA_MSG = "!REQ_DATA"

#Define client socket
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Flag which indicates waiting for message from server
REC_MSG = False

#Message that shows last currency update time
TIMESTAMP = ""

#Currency array
CURRENCIES = []

#Simplified currencies array
SIMPLE_CURRENCIES = []

#Balance array
BALANCE = []

#Function converts currencies
#c_amount - amount of currency that's going to be calculated
#c_from - currency code from which result's going to be calculated
#c_to - currency code to which result's going to be calculated
def count_currencies(c_amount, c_from, c_to):

    #If currency amount isn't a digit, function returns error
    if not c_amount.isdigit():
        print("Error: Invalid given data")
        return -1

    #If given amount is less than 0 or given currencies are the same, functions return error
    if float(c_amount) <= 0 or c_from == c_to:
        print("Error: Invalid given data")
        return -1

    #Ensuring that currencies are upper cased
    c_from = c_from.upper()
    c_to = c_to.upper()

    cf = SimpleCurrency()
    ct = SimpleCurrency()

    #Searching for given currencies in currency array
    for data in SIMPLE_CURRENCIES:
        if data.code == c_from:
            cf = data
        if data.code == c_to:
            ct = data

    #If currencies haven't been found, function returns error
    if ct.code == "" or cf.code == "" or float(ct.value) == 0.0 or float(cf.value) == 0.0:
        print("Error: Given currency code is invalid")
        return -1

    #Converting currencies
    result = round((float(c_amount) / float(cf.value)) * float(ct.value), 3)
    return result

#Functions updates balance
#c_amount - amount of currency that's going to be calculated
#c_from - currency code from which result's going to be calculated
#c_to - currency code to which result's going to be calculated
def update_balance(c_amount, c_from, c_to):

    #If currency arguments are invalid, count_currencies returns error, than function returns error
    if count_currencies(c_amount, c_from, c_to) == -1:
        return -1

    #If currency amount isn't a digit, function returns error
    if not c_amount.isdigit():
        print("Error: Invalid given data")
        return -1

    #Ensuring that currencies are upper cased
    c_from = c_from.upper()
    c_to = c_to.upper()

    #Finding given currencies, from which result's going to be calculated, in current balance array
    fb = Balance()
    for b in BALANCE:
        if c_from == b.code:
            fb.code = b.code
            fb.amount = b.amount

    #If currencies haven't been found, function returns error
    if fb.code == "":
        print("There is no given currency in your balance")
        return -1

    #Currency update from which we collect money for currency conversion
    for b in BALANCE:
        if c_from == b.code:
            if b.amount == 0 or float(c_amount) > b.amount:
                print("Unable to perform changes in balance")
                return -1
            b.amount = b.amount - float(c_amount)
            if b.amount == 0:
                BALANCE.remove(b)

    #Converting currencies
    result = count_currencies(c_amount, c_from, c_to)

    #Updating the currency to which we will convert money to currency conversion,
    # if it's already in balance array
    for b in BALANCE:
        if c_to == b.code:
            b.amount = b.amount + result
            return

    #Updating the currency to which we will convert money to currency conversion,
    # if it's not in balance array
    b = Balance()
    b.amount = result
    b.code = c_to.upper()
    BALANCE.append(b)

#Function updates currency array
#data - downloaded currency data
def update_currencies(data):
    CURRENCIES.clear()
    i = 0
    #Reading last data updates
    for line in reversed(data):
        if i < 34:
            #Getting correct informations from downloaded text
            res = " ".join(reversed(line.split(" ")))
            res = res.split()
            #Currency object instance
            c = Currency()
            c.name = line.rsplit(' 1', 2)[0]
            c.code = str(res[2]) + " " + str(res[1])
            c.value = float(res[0])
            #Adding currency to currency array
            CURRENCIES.append(c)
            i = i + 1

#Function simplifies downloaded currencies for converting
def simplify_currencies(curr):
    SIMPLE_CURRENCIES.clear()
    for data in curr:
        #SimpleCurrency object instance
        sc = SimpleCurrency()
        v = float(data.code.rsplit()[0])
        sc.value = round(v/data.value, 3)
        sc.code = data.code.rsplit()[1]
        SIMPLE_CURRENCIES.append(sc)
    #Adding information about the zloty exchange rate for possible conversions
    pln = SimpleCurrency()
    pln.value = 1.0
    pln.code = "PLN"
    SIMPLE_CURRENCIES.append(pln)

#Function prints basic menu
def menu():
    print()
    if TIMESTAMP != "":
        print(f"Last currency update {TIMESTAMP}")
    print()
    print("0 - Exit client")
    print("1 - Download currency data")
    print("2 - Show currency data")
    print("3 - Count currencies")
    print()

#Functions prints avaliable balance
def show_balance():
    print("Current balance avaliable:")
    for b in BALANCE:
        print(b)
    print()

#Function sends message to server
#msg - message that will be send to server
def send(msg):
    try:
        #Encoding message
        message = msg.encode(FORMAT)
        #Message length
        MSG_LENGTH = len(message)
        #Sending message length
        send_length = str(MSG_LENGTH).encode(FORMAT)
        #Adding any missing bits to the text length message
        send_length += b' ' * (HEADER - len(send_length))
        #Sending information about the length of the message
        CLIENT.send(send_length)
        #Sending message
        CLIENT.send(message)
        #If REC_MSG set on true (ready to recieve message from server)
        if REC_MSG:
            #Recieved message length
            MSG_LENGTH = CLIENT.recv(102400)
            if MSG_LENGTH is not None:
                #Loading currency data
                data = pickle.loads(MSG_LENGTH)
                #Updating client currency data
                update_currencies(data)
    except BrokenPipeError:
        print("Error: Connection with server has been broken")
        exit()

if __name__ == '__main__':
    #Connecting to server
    try:
        CLIENT.connect(ADDR)
    except ConnectionRefusedError:
        print("Error: Unable to contact server")
        exit()

    #Downloading clients acceptance messages
    MSG_LENGTH = CLIENT.recv(102400)
    if MSG_LENGTH is not None:
        DATA = pickle.loads(MSG_LENGTH)

    #If the customer is not accepted, error will be displayed
    if not DATA:
        send(DISCONNECT_MSG)
        print("Error: Unable to connect to server")
        print("Reason: Reached maximum numbers of clients")
        exit()

    #Adding an initial balance
    START_BALANCE = Balance()
    START_BALANCE.code = "PLN"
    START_BALANCE.amount = 10000.0
    BALANCE.append(START_BALANCE)
    #Display of basic client menu
    menu()
    #Display of the current balance
    show_balance()
    INP = input("> ")
    while INP != "0":
        #1 - currency data update
        if INP == "1":
            REC_MSG = True
            send(REQUEST_DATA_MSG)
            NOW = datetime.now()
            TIMESTAMP = NOW.strftime("%H:%M:%S")
            simplify_currencies(CURRENCIES)
        #2 - display currency data
        elif INP == "2":
            if len(SIMPLE_CURRENCIES) > 0:
                for cur in SIMPLE_CURRENCIES:
                    print(cur)
        #3 - conversion of given currencies
        elif INP == "3":
            AMOUNT = input("How many? ")
            CURR_FROM = input("From which currency? ")
            CURR_TO = input("To which currency? ")
            if count_currencies(AMOUNT, CURR_FROM, CURR_TO) != -1:
                update_balance(AMOUNT, CURR_FROM, CURR_TO)
        else:
            REC_MSG = False
            print("Error: Invalid command")
        menu()
        show_balance()
        try:
            INP = input("> ")
        except (KeyboardInterrupt):
            INP = "0"

    #Disconnect after command "0"
    REC_MSG = False
    send(DISCONNECT_MSG)
