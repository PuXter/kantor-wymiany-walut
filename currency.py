from requests import get
from bs4 import BeautifulSoup
import random

URL = 'https://www.nbp.pl/home.aspx?f=/kursy/kursya.html'
page = get(URL)
bs = BeautifulSoup(page.content, "html.parser")
currencies = [] 

class Currency:

    name = " "
    code = " "
    value = 0.0

    def __str__(self):
        return self.name + " " + self.code + " " + str(self.value)


class CurrencyData:

    def __init__(self):
        self.currencies = []

    def getCurrencies(self):
        return self.currencies

    def getData(self, currencies=None):
        table = bs.find("table", class_='nbptable')
        body = table.find("tbody")

        i = 0

        for data in body.find_all("tr"):
            cur = Currency()
            for x in data.find_all("td"):
                if(i==0):
                    cur.name = x.get_text()
                if(i==1):
                    cur.code = x.get_text()
                if(i==2):
                    v = float(x.get_text().replace(',','.'))
                    r = random.uniform(0.95, 1.05)
                    cur.value = round(v*r,3)
                i = i + 1
                if(i==3):
                    i = 0
                    self.currencies.append(cur.__str__())
                    # del cur

    def saveData(self):
        print(self.currencies[0])
        for cur in self.currencies:
            pass

    def showData(self):
        for cur in currencies:
            print(cur)
            
