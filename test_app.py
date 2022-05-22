import unittest
import currency
import client

class TestCurrency(unittest.TestCase):

    def test_get_data(self):
        #Check if there are 34 different currencies
        cd_1 = currency.CurrencyData()
        cd_1.get_data()
        array_1 = cd_1.get_currencies()
        array_length = len(array_1)
        self.assertEqual(array_length, 34)
        #Check if downloaded currency arrays differs
        cd_2 = currency.CurrencyData()
        cd_2.get_data()
        array_2 = cd_2.get_currencies()
        #May return error because of random moments
        #when currencies are modified in a same way
        self.assertNotEqual(array_1[0], array_2[0])

class TestClient(unittest.TestCase):

    def test_currency_converting(self):
        cd = currency.CurrencyData()
        cd.get_data()
        client.update_currencies(cd.get_currencies())
        client.simplify_currencies(client.CURRENCIES)
        #Check if invalid arguments return error
        failed_result_1 = client.count_currencies("das", "usd", "cad")
        self.assertEqual(failed_result_1, -1)
        failed_result_2 = client.count_currencies("20", "0", ";")
        self.assertEqual(failed_result_2, -1)
        #Check if valid arguments don't return error
        result = client.count_currencies("20", "usd", "cad")
        self.assertNotEqual(result, -1)

    def test_balance_update(self):
        #Check if Balance is updated in a correct way
        start_balane = currency.Balance()
        start_balane.code = "PLN"
        start_balane.amount = 10000.0
        client.BALANCE.append(start_balane)
        #Balance should only have 10000 PLN
        self.assertEqual(len(client.BALANCE), 1)
        cd = currency.CurrencyData()
        cd.get_data()
        client.update_currencies(cd.get_currencies())
        client.simplify_currencies(client.CURRENCIES)
        #Simple currencies should have 35 positions
        self.assertEqual(len(client.SIMPLE_CURRENCIES), 35)
        client.update_balance("5000", "pln", "usd")
        #Balance should only have 5000 PLN and some USD
        self.assertEqual(len(client.BALANCE), 2)
        self.assertEqual(client.BALANCE[0].amount, 5000.0)
        client.update_balance("5000", "pln", "cad")
        #Balance should only have some CAD and some USD
        self.assertEqual(len(client.BALANCE), 2)
        self.assertNotEqual(client.BALANCE[0].code, "PLN")
        #Invalid arguments doesn't change balance array
        b_1 = client.BALANCE
        client.update_balance("wef", "pln", "cad")
        client.update_balance("200", "test", "cad")
        b_2 = client.BALANCE
        self.assertEqual(b_1, b_2)

if __name__ == '__main__':
    unittest.main()
