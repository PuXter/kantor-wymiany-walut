import currency
from currency import CurrencyData

def main():
    cd = CurrencyData()
    cd.getData()
    print(cd.showData())

main()