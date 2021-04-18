import telebot
from telebot import types

import chess
import chess.svg
import chess.engine

import cairosvg
import uuid
import os

TOKEN = '1728273090:AAHfWDqNNQjXs2UffWj_ool8ySD6vyTMKbg'

# логи входящих сообщений в конслоль


def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)


hideKeyboard = types.ReplyKeyboardRemove()

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)


class Game:
    # количество подсказок
    help_count_init = 0

    # Уровень сложности
    level = 1  # 1,2,3

    # доска игры
    board = chess.Board()

    # игрок
    # user = None

    # def __init__(self, user):
    #     self.user = user

    # получим класс хода из текста сообщения
    def get_move_from_text(self, text):
        human_move = text \
            .replace("♙", "") \
            .replace("♟", "") \
            .replace("♖", "R") \
            .replace("♜", "R") \
            .replace("♘", "N") \
            .replace("♞", "N") \
            .replace("♗", "B") \
            .replace("♝", "B") \
            .replace("♕", "Q") \
            .replace("♛", "Q") \
            .replace("♔", "K") \
            .replace("♚", "K")

        try:
            move = self.board.parse_san(human_move)
            if move in self.board.legal_moves:
                return move
            return None
        except:
            return None

    # добавить ход на доску
    def board_add_move(self, move):
        self.board.push(move)

    # показвыаем доску, если число подсказкок > 0
    def can_help_take(self, user):
        if self.help_count_init > 0:
            self.help_count_init -= 1
            return True

        bot.send_message(user.chat_id, "Твое количество подсказок закончилось")
        return False

    def movies_show(self, user):
        text = [str(i) for i in self.board.move_stack]
        if len(self.board.move_stack) < 1:
            text = "В игре не было сделано ни одного хода"
        bot.send_message(user.chat_id, str(text))

    def board_show(self, user):
        if not self.can_help_take(user):
            return
        svg_code = chess.svg.board(self.board, size=350)
        file_name = str(uuid.uuid4()) + '.png'

        cairosvg.svg2png(bytestring=svg_code, write_to=file_name)
        photo = open(file_name, 'rb')
        bot.send_photo(user.chat_id, photo)
        os.remove(file_name)

    def set_help_count(self, count):
        self.help_count_init = count

    def set_level(self, level):
        sec = 1.0
        if level == 1:
            sec = 0.0000000001
        elif level == 2:
            sec = 0.000000001
        elif level == 3:
            sec = 0.00000001
        elif level == 4:
            sec = 0.0000001
        elif level == 5:
            sec = 0.000001
        elif level == 6:
            sec = 0.00001
        elif level == 7:
            sec = 0.0001
        elif level == 8:
            sec = 0.001
        elif level == 9:
            sec = 0.01
        elif level == 10:
            sec = 0.1

        self.level = sec

    # проверка, что игра окончена
    def check_gamme_over(self, user):
        return self.board.outcome()


class GameEngine:

    ENGINE_PATH = "/Users/konstantinsavkin/chess_engines/stockfish/13/bin/stockfish"

    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

    # массив игр
    games = {}

    def game_add(self, chat_id):
        user = User(chat_id)

        game = Game()
        game.board = chess.Board()
        self.games[user] = game

    # получить текущую игру у пользователя
    def get_game_by_user(self, user):
        if not user in self.games:
            self.game_add(user.chat_id)

        return self.games[user]

    # обработчик хода человека

    def human_move_processing(self, user, text):
        game = self.get_game_by_user(user)
        move = game.get_move_from_text(text)
        if move == None:
            bot.send_message(user.chat_id, 'некорректный ход')
            return False
        game.board_add_move(move)
        return True

    # ход компьютера
    def bot_move(self, user):
        bot.send_chat_action(user.chat_id, 'typing')
        game = self.get_game_by_user(user)

        move = self.engine.play(
            game.board, chess.engine.Limit(time=game.level)).move
        game.board_add_move(move)
        bot.send_message(user.chat_id, move)

    def check_game_over(self, user):
        current_game = self.get_game_by_user(user)

        status = current_game.check_gamme_over(user)

        if status != None:
            winner = status.winner
            if winner == chess.WHITE:
                bot.send_message(
                    user.chat_id, "Игра окончена. Белые подбедили!")
            else:
                bot.send_message(
                    user.chat_id, "Игра окончена. Черные подбедили!")

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(
                telebot.types.InlineKeyboardButton(
                    text='Новая игра',
                    callback_data='newgame'))

            bot.send_message(
                user.chat_id,
                'Давай начнем заново',
                reply_markup=markup)

            return True

        return False


class User:
    chat_id = ""

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def __hash__(self):
        return hash(self.chat_id)

    def __eq__(self, user):
        return self.chat_id == user.chat_id


game_engine = GameEngine()


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id

    bot.send_message(
        chat_id,
        'Привет я - бот для слепой игры в шахматы')

    command_help(message)

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            text='Новая игра',
            callback_data='newgame'))
    bot.send_message(
        chat_id,
        'Давайте сыграем в слепые шахматы',
        reply_markup=keyboard)


def send_figure_help(chat_id):
    user = User(chat_id)
    text = "Используйте латинские символы для обзначения фигур: \
        \n К - король белых \
        \n k - король черных \
        \n Q - ферзь белых \
        \n q - ферзь черных \
        \n B - слон белых \
        \n K - конь белых \
        \n R - ладья белых \
        \n r - ладья черных \
        \n P - пешка белых \
        \n p - пешка черных"

    text += "Графическое бозначения фигур: \nK(♔) - король белых \n Q(♕) - ферзь белых \n B(♗) - слон белых \n N(♘) - конь белых \n R (♖)- ладья белых \n P(♙) - пешка черных.\n k(♚) - король черных \n q(♛) - ферзь ) - b (♝) слон черных \n n(♞) - конь черных \n r(♜)- ладья черных \n p(♟) - пешка черных."
    bot.send_message(chat_id, text)


@bot.message_handler(commands=['help'])
def command_help(message):
    help_text = "Вы можете использовать команды: \n"
    help_text += "/start : для старта новой игры. \n"
    help_text += "/help : для получения этой справки. \n"
    help_text += "Для ходов Вы можете использовать одну из нотаций на Ваш вкус: \n"
    help_text += "Полную нотацию: e2e4 \n"
    help_text += "Короткую нотацию: e4 \n"
    help_text += "Графическиб нотацию: ♟e4 \n"
    bot.send_message(message.chat.id, help_text)
    send_figure_help(message.chat.id)


def setup_new_game(chat_id):

    game_engine.game_add(chat_id)

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='0', callback_data='help_count0'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='1', callback_data='help_count1'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='2', callback_data='help_count2'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='3', callback_data='help_count3'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text="5", callback_data='help_count5'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='8', callback_data='help_count8'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='13', callback_data='help_count13'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='21', callback_data='help_count21'))

    bot.send_message(
        chat_id,
        "Выбери сколько раз ты можешь пользоваться подсказками)",
        reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'newgame')
def command_newgame(call):
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id)
    setup_new_game(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("help_count"))
def command_helpcount(call):
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id)
    count = int(call.data.replace("help_count", ""))

    user = User(call.message.chat.id)
    current_game = game_engine.get_game_by_user(user)
    current_game.set_help_count(count)

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 1', callback_data='level1'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 2', callback_data='level2'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 3', callback_data='level3'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 4', callback_data='level4'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 5', callback_data='level5'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 6', callback_data='level6'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 7', callback_data='level7'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 8', callback_data='level8'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 9', callback_data='level9'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Уровень 10', callback_data='level10'))

    bot.send_message(
        call.message.chat.id,
        "Выберите уровень сложности (чем уровень выше, тем бот сильнее играет)",
        reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("level"))
def command_level(call):
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id)
    level = int(call.data.replace("level", ""))

    user = User(call.message.chat.id)
    current_game = game_engine.get_game_by_user(user)
    current_game.set_level(level)

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Я хочу играть белыми', callback_data='color_white'))
    keyboard.add(telebot.types.InlineKeyboardButton(
        text='Я хочу играть черными', callback_data='color_black'))

    bot.send_message(
        call.message.chat.id, 'Выбери каким цветом ты хочешь играть', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'color_white')
def command_color_white(call):
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id)
    do_play(call.message.chat.id, True)


@bot.callback_query_handler(func=lambda call: call.data == 'color_black')
def command_color_black(call):
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id)
    do_play(call.message.chat.id, False)


@bot.message_handler(content_types=['text'], func=lambda message: message.text.lower() == 'показать доску')
def command_board_show(message):
    user = User(message.chat.id)
    current_game = game_engine.get_game_by_user(user)
    current_game.board_show(user)


@bot.message_handler(content_types=['text'], func=lambda message: message.text.lower() == 'показать список ходов')
def command_moves_show(message):
    user = User(message.chat.id)
    current_game = game_engine.get_game_by_user(user)
    current_game.movies_show(user)


@bot.message_handler(content_types=['text'], func=lambda message: message.text.lower() == 'начать новую игру')
def command_figure_help(message):
    setup_new_game(message.chat.id)


@bot.message_handler(content_types=['text'], func=lambda message: message.text.lower() == 'помощь')
def command_figure_help(message):
    send_figure_help(message.chat.id)


@bot.message_handler(content_types=['text'])
def message_receive(message):

    text = message.text
    user = User(message.chat.id)
    current_game = game_engine.get_game_by_user(user)

    if current_game == None:
        bot.send_message(user.chat_id, "Игра не найдена. Начинаем новую игру")
        setup_new_game(message.chat.id)
        return

    if game_engine.human_move_processing(user, text):
        if game_engine.check_game_over(user):
            return

        game_engine.bot_move(user)
        if not game_engine.check_game_over(user):
            bot.send_message(message.chat.id, "Твой ход")


def do_play(chat_id, is_human_white):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    bot.send_message(
        chat_id,
        'Новая партия начинается. У тебя будут кнопки-подсказки, удачи!',
        reply_markup=keyboard)

    keyboard.row('Показать доску', 'Показать список ходов',
                 'Помощь', 'Начать новую игру')
    if is_human_white:
        bot.send_message(
            chat_id,
            'Вы выбрали играть за белых, сделайте ход',
            reply_markup=keyboard)
    else:
        user = User(chat_id)
        bot.send_message(
            chat_id,
            'Вы выбрали играть за черных. Ход бота',
            reply_markup=keyboard)
        game_engine.bot_move(user)


bot.polling()
