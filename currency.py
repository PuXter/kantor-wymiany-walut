from requests import get
from bs4 import BeautifulSoup
import random

#Page with currency data
URL = 'https://www.nbp.pl/home.aspx?f=/kursy/kursya.html'
#Get response from bank page
PAGE = get(URL)
#Page content
BS = BeautifulSoup(PAGE.content, "html.parser")
#Currency array
CURRENCIES = []

#Currency class defines its atributes
class Currency:

    #Atributes such as name, code and value
    name = " "
    code = " "
    value = 0.0

    #__str__ method overwrite
    def __str__(self):
        return self.name + " " + self.code + " " + str(self.value)

#CurrencyData defines currency data atributes
class CurrencyData:

    #Constructor overwrite, initialize currency array
    def __init__(self):
        self.CURRENCIES = []

    #Method returns current currency array
    def get_currencies(self):
        return self.CURRENCIES

    #Method downloads current currency data
    def get_data(self):

        #Finding correct page components
        table = BS.find("table", class_='nbptable')
        body = table.find("tbody")

        i = 0
        for data in body.find_all("tr"):
            cur = Currency()
            for x in data.find_all("td"):
                if i == 0:
                    cur.name = x.get_text()
                if i == 1:
                    cur.code = x.get_text()
                if i == 2:
                    v = float(x.get_text().replace(',', '.'))
                    r = random.uniform(0.95, 1.05)
                    cur.value = round(v*r, 3)
                i = i + 1
                if i == 3:
                    i = 0
                    self.CURRENCIES.append(cur.__str__())

    #Method prints current currency array
    def show_data():
        for cur in CURRENCIES:
            print(cur)

#SimpleCurrency class defines simpler form of currency
class SimpleCurrency:

    #Atributes such as code and value
    code = ""
    value = 0.0

    #__str__ method overwrite
    def __str__(self):
        return " 1 PLN =  " + str(self.value) + " " + self.code

#Balance class defines amount and code of local currency balance items
class Balance:

    #Atributes such as code and value
    code = ""
    amount = 0.0

    #__str__ method overwrite
    def __str__(self):
        return str(self.amount) + " " + self.code