from pycbrf.toolbox import ExchangeRates


def converter_1(currency=0, date='2020-11-27'):
    # USD - доллар EUR - евро XDR - резервная валюта мира
    # GBP - английский фунт   CHF - швейцарский франк

    arr = ['USD', 'EUR', 'XDR', 'GBP', 'CHF']
    rates = ExchangeRates(date)
    return rates[arr[currency]].value


def return_server():
    return 'https://www.banki.ru/products/currency/cash/moskva/#bank-rates'
    # корректные курсы в вашем городе
