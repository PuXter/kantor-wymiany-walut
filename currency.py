from requests import get
from bs4 import BeautifulSoup
import random

#Strona z danymi o kursach walutowych 
URL = 'https://www.nbp.pl/home.aspx?f=/kursy/kursya.html'
#Odpowiedz na zadanie GET ze strony
page = get(URL)
#Zawartosc strony
bs = BeautifulSoup(page.content, "html.parser")
#Tablica walut
currencies = [] 

#Klasa Currency definuje obiekt waluty
class Currency:

    #Atrybuty waluty takie jak nazwa, kod i wartosc
    name = " "
    code = " "
    value = 0.0

    #Nadpisanie metody __str__
    def __str__(self):
        return self.name + " " + self.code + " " + str(self.value)

#Klasa CurrencyData definuje obiekty danych walut
class CurrencyData:

    #Nadpianie konstruktora, tworzacego tablice walut
    def __init__(self):
        self.currencies = []

    #Metoda zwracajca aktualna tablice walut
    def getCurrencies(self):
        return self.currencies

    #Metoda sciagajaca aktualne dane walut
    def getData(self, currencies=None):
        #Znalezienie odpowiednich elementow strony
        table = bs.find("table", class_='nbptable')
        body = table.find("tbody")

        i = 0

        for data in body.find_all("tr"):
            cur = Currency()
            for x in data.find_all("td"):
                if(i==0):
                    #Nazwa waluty
                    cur.name = x.get_text()
                if(i==1):
                    #Kod waluty
                    cur.code = x.get_text()
                if(i==2):
                    #Wartosc waluty
                    v = float(x.get_text().replace(',','.'))
                    r = random.uniform(0.95, 1.05)
                    cur.value = round(v*r,3)
                i = i + 1
                if(i==3):
                    i = 0
                    #Dodanie waluty do tablicy
                    self.currencies.append(cur.__str__())

    #Metoda odpowiedzialna za wyswietlenie danych o walutach
    def showData(self):
        for cur in currencies:
            print(cur)
            
class SimpleCurrency:
    
    #Atrybuty waluty takie jak kod i wartosc
    code = ""
    value = 0.0

    #Nadpisanie metody __str__
    def __str__(self):
        return " 1 PLN =  " + str(self.value) + " " + self.code 
