import telebot
import chess
import chess.engine

bot = telebot.TeleBot('1728273090:AAHfWDqNNQjXs2UffWj_ool8ySD6vyTMKbg')
engine = chess.engine.SimpleEngine.popen_uci("/Users/konstantinsavkin/chess_engines/stockfish/13/bin/stockfish")
board = chess.Board()
class Game():
    def __init__(self, board):
        self.board = board
@bot.message_handler(commands=['start'])
def recive_start(message):
    create_game(message)

def create_game(message):
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    bot.send_message(message.chat.id, result.move)
    bot.send_message(message.chat.id, board)

@bot.message_handler(content_types=['text'])
def recive(message):
    human_move = message
    uci = chess.Move.from_uci(human_move.html_text)
    board.push(uci)

    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    bot.send_message(message.chat.id, result.move)
    bot.send_message(message.chat.id, board)


bot.polling()

