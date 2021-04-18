import telebot
from telebot import types

import chess
import chess.svg
import chess.engine

import cairosvg
import uuid
import os

class Game:
    # количество подсказок
    help_count_init = 0

    # Уровень сложности
    level = 1  # 1,2,3

    # доска игры
    board = chess.Board()

    def __init__(self, bot):
        self.bot = bot

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

        self.bot.send_message(user.chat_id, "Твое количество подсказок закончилось")
        return False

    def movies_show(self, user):
        text = [str(i) for i in self.board.move_stack]
        if len(self.board.move_stack) < 1:
            text = "В игре не было сделано ни одного хода"
        self.bot.send_message(user.chat_id, str(text))

    def board_show(self, user):
        if not self.can_help_take(user):
            return
        svg_code = chess.svg.board(self.board, size=350)
        file_name = str(uuid.uuid4()) + '.png'

        cairosvg.svg2png(bytestring=svg_code, write_to=file_name)
        photo = open(file_name, 'rb')
        self.bot.send_photo(user.chat_id, photo)
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

