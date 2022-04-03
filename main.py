import currency
from currency import CurrencyData

def main():
    cd = CurrencyData()
    cd.getData()
    # print(cd.saveData())
    print(cd.showData())

main()