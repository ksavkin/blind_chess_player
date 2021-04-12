import telebot
import chess
import chess.engine

class Game():
    bot = telebot.TeleBot('1728273090:AAHfWDqNNQjXs2UffWj_ool8ySD6vyTMKbg')
    
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci("/Users/konstantinsavkin/chess_engines/stockfish/13/bin/stockfish")
       
    
        @self.bot.message_handler(commands=['start'])
        def recive_start(message):
            create_game(message)

    def create_game(self, message):    
        board = chess.Board()
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        bot.send_message(message.chat.id, result.move)
        bot.send_message(message.chat.id, board)

game = Game()
