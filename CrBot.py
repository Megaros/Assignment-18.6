import telebot
from telebot import types
from config import TOKEN, keys
from extensions import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_htlp(message: telebot.types.Message):
    text = '\n________________________________________________________\n' \
           ' Данный бот конвертирует любое количество валюты в другую валюту, выбранную ' \
           'пользвателем и доступную боту.\n' \
           ' Чтобы начать  работу отправьте сообщение боту' \
           ' в следующем формате:\n <имя валюты>   <в какую валюту перевести>  <количество переводимой валюты>\n' \
           ' Увидеть список всех доступных валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join([text, key])
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Слишком много или не все параметры 🤨')
        quote, base, amount = values
        total_base = CriptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя🤷‍♂️\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}🤷‍♂️')
    else:
        text = f'Цена {amount} {quote} в {base}ах ➡️ {total_base}'
        bot.reply_to(message, text)


bot.polling()
