import telebot
from telebot import types

import chess
import chess.engine

from user import User
from game import Game


class GameEngine:

    ENGINE_PATH = "/Users/konstantinsavkin/chess_engines/stockfish/13/bin/stockfish"

    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

    # массив игр
    games = {}

    def __init__(self, bot):
        self.bot = bot

    def game_add(self, chat_id):
        user = User(chat_id)

        game = Game(self.bot)
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
            self.bot.send_message(user.chat_id, 'некорректный ход')
            return False
        game.board_add_move(move)
        return True

    # ход компьютера
    def bot_move(self, user):
        self.bot.send_chat_action(user.chat_id, 'typing')
        game = self.get_game_by_user(user)

        move = self.engine.play(
            game.board, chess.engine.Limit(time=game.level)).move
        game.board_add_move(move)
        self.bot.send_message(user.chat_id, move)

    def check_game_over(self, user):
        current_game = self.get_game_by_user(user)

        status = current_game.check_gamme_over(user)

        if status != None:
            winner = status.winner
            if winner == chess.WHITE:
                self.bot.send_message(
                    user.chat_id, "Игра окончена. Белые подбедили!")
            else:
                self.bot.send_message(
                    user.chat_id, "Игра окончена. Черные подбедили!")

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(
                telebot.types.InlineKeyboardButton(
                    text='Новая игра',
                    callback_data='newgame'))

            self.bot.send_message(
                user.chat_id,
                'Давай начнем заново',
                reply_markup=markup)

            return True

        return False
