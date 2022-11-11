import telebot
import requests
import json

from extensions import ConvertException, ValueException, Cryptoconverter
from Config import TOKEN


bot = telebot.TeleBot(TOKEN)

keys_values = {'евро': 'EUR','доллар': 'USD', 'рубль': 'RUR'}

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.chat.first_name}. Я бот для конвертации валют. Чтобы начать работу,'
                                      f'введите параметры через пробел в форме <имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты> \n'
                                      f'Чтобы узнать список доступных валют используйте команду /values')

@bot.message_handler(commands=['values'])
def used_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys_values.keys():
        text ='\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertException
    except ConvertException:
        bot.send_message(message.chat.id,'Неправльное количество слов!!!!ААА!!! Не понимаю!!')
    if len(values) == 3:
        base,quote, amount = values[0], values[1], float(values[2])
        if quote == base:
            try:
                raise ConvertException
            except ConvertException:
                bot.send_message(message.chat.id, f'Нельзя конвертировать валюту {quote} в саму себя... Ну то есть можно, но бессмысленно')

        if quote not in keys_values or base not in keys_values:
            try:
                raise ValueException
            except ValueException:
                bot.send_message(message.chat.id, 'Введены неверные названия валют')
        else:
            result = Cryptoconverter.get_price(base, quote, amount)
            text = f'Цена {amount} {base} в {quote} составит {result}'
            bot.send_message(message.chat.id, text)




@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    bot.send_message(message.chat.id, "Я не понимаю этого")

bot.polling(none_stop=True)
