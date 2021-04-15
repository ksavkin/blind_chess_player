import telebot
import chess
import chess.engine
# bot = telebot.TeleBot('token')
engine = chess.engine.SimpleEngine.popen_uci("/Users/konstantinsavkin/chess_engines/stockfish/13/bin/stockfish")
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Показать доску', 'Показать список ходов')
chess_moves = []
users = {}
@bot.message_handler(commands=['start'])
def start_message(message):
    global users
    # global board
    if message.chat.id not in users:
        users[message.chat.id] = chess.Board()
        # board = users[message.chat.id]
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Новая игра', callback_data='/newgame'))
    bot.send_message(message.chat.id, 'Привет давай сыграем в шахматы!', reply_markup=markup)



# возвращает ход если он корректный, иначе None
def get_move(human_move, message):
    try:
        move = users[message.chat.id].parse_san(human_move)
        if move in users[message.chat.id].legal_moves:
            return move
    except:
        return None

def command_processing(human_move):
    message = human_move
    if human_move.html_text == "Показать доску":
        bot.send_message(human_move.chat.id, users[message.chat.id])
        return 1
    if human_move.html_text == "Показать список ходов":
        bot.send_message(human_move.chat.id, str(chess_moves[0:]))
        return 1

    return get_move(human_move.html_text, message)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == '/newgame':

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Я хочу играть белыми', callback_data='white'))
        markup.add(telebot.types.InlineKeyboardButton(text='Я хочу играть черными', callback_data='black'))
        bot.send_message(call.message.chat.id, 'Выбери каким цветом ты хочешь играть', reply_markup=markup)
        bot.callback_query_handler(func=lambda call: True)
    elif call.data == "white":
        bot.send_message(call.message.chat.id, 'У тебя будут кнопки-подсказки, удачи!', reply_markup=keyboard)
        create_game(call.message, iswhite=True)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == "black":
        bot.send_message(call.message.chat.id, 'У тебя будут кнопки-подсказки, удачи!', reply_markup=keyboard)
        create_game(call.message, iswhite=False)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    


def create_game(message, iswhite):
    if not iswhite:
        
    
        result = engine.play(users[message.chat.id], chess.engine.Limit(time=0.1))
        bot.send_message(message.chat.id, result.move)

        users[message.chat.id].push(result.move)
    else:
        bot.send_message(message.chat.id, "Начинай")
@bot.message_handler(content_types=['text'])
def recive(message):

    human_move = message
    if command_processing(human_move) == 1:
        return
    elif command_processing(human_move) == None:
        bot.send_message(message.chat.id, 'некорректный ход')
        return
    new_move = command_processing(human_move)
    chess_moves.append(human_move.html_text)
    users[message.chat.id].push(new_move)
    if users[message.chat.id].is_stalemate():
        users[message.chat.id] = chess.Board()
        bot.send_message(message.chat.id, "Игра закончена, я победил. Если хочешь начать слачала напиши команду '/start' ")
        return

    result = engine.play(users[message.chat.id], chess.engine.Limit(time=0.1))
    chess_moves.append(str(result.move))
    users[message.chat.id].push(result.move)
    bot.send_message(message.chat.id, result.move)
    
    if users[message.chat.id].is_checkmate():
        users[message.chat.id] = chess.Board()
        bot.send_message(message.chat.id, "Игра закончена, я победил. Если хочешь начать слачала напиши команду '/start' ")
        return
    else:
        bot.send_message(message.chat.id, "Твой ход")
bot.polling()
