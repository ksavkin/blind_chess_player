import telebot

bot = telebot.TeleBot('1749325046:AAFOLhDLVE-XywHDjofLmpDvb0GlVJGv4EA')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'Понедельник':
        bot.send_message(message.chat.id, '''Русский язык
        Физика
        Геометрия
        Чимия
        История
        Литература''')

bot.polling()