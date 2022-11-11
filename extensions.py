import telebot
import requests
import json


class ConvertException(Exception):
    pass


class ValueException(Exception):
    pass

class Cryptoconverter:
    @staticmethod
    def get_price(base, quote, amount):
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        EUR_ = float(data['Valute']['EUR']['Value'])
        USD_ = float(data['Valute']['USD']['Value'])
        if base == 'евро' and quote == 'рубль':
            total_price = EUR_ * amount
        elif base == 'доллар' and quote == 'рубль':
            total_price = USD_ * amount
        elif base == 'рубль' and quote == 'евро':
            total_price = amount / EUR_
        elif base == 'рубль' and quote == 'доллар':
            total_price = amount / USD_
        elif base == 'доллар' and quote == 'евро':
            total_price = (USD_ / EUR_ * amount)
        elif base == 'евро' and quote == 'доллар':
            total_price = (EUR_ / USD_ * amount)

        return total_price