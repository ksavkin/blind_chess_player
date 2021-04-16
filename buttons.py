import telebot
import chess
import chess.engine
bot = telebot.TeleBot('1728273090:AAHfWDqNNQjXs2UffWj_ool8ySD6vyTMKbg')
engine = chess.engine.SimpleEngine.popen_uci("/Users/konstantinsavkin/chess_engines/stockfish/13/bin/stockfish")
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Показать доску', 'Показать список ходов', 'Обозначение фигур', 'Как ходить?')
chess_moves = []
count = 0
count_user = 0

users = {}
@bot.message_handler(commands=['start'])
def start_message(message):
    global users
    global count
    global count_user
    count = 0
    count_user = 0
    if message.chat.id not in users:
        users[message.chat.id] = chess.Board()
    else:
        users[message.chat.id] = chess.Board()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Новая игра', callback_data='/newgame'))
    
    bot.send_message(message.chat.id, 'Привет я - бот для слепой игры в шахматы, давай сыграем ! ', reply_markup=markup)




# возвращает ход если он корректный, иначе None
def get_move(human_move, message):
    try:
        condition_P = "♙" in message.text
        condition_p = "♟" in message.text
        if condition_P or condition_p:
            human_move = message.text[1:]

        condition_R = "♖" in message.text
        condition_r = "♜" in message.text
        if condition_P or condition_r:
            human_move = "R" + message.text[1:]

        condition_N = "♘" in message.text
        condition_n = "♞" in message.text
        if condition_N or condition_n:
            human_move = "N" + message.text[1:]

        condition_B = "♗" in message.text
        condition_b = "♝" in message.text
        if condition_B or condition_b:
            human_move = "B" + message.text[1:]

        condition_Q = "♕" in message.text
        condition_q = "♛" in message.text
        if condition_Q or condition_q:
            human_move = "Q" + message.text[1:]

        condition_K = "♔" in message.text
        condition_k = "♚" in message.text
        if condition_Q or condition_q:
            human_move = "K" + message.text[1:]

        move = users[message.chat.id].parse_san(human_move)
        if move in users[message.chat.id].legal_moves:
            return move
    except:
        return None

def command_processing(human_move):
    message = human_move
    global count
    if human_move.html_text == "Показать доску":
        count += 1
        if count > count_user:
            bot.send_message(message.chat.id, "Твое количество подсказок закончилось")
            return 1
        board = str(users[message.chat.id]).replace("P", "♙").replace("p", "♟").replace("R", "♖").replace("N", "♘")
        board = board.replace("B", "♗").replace("K", "♔").replace("Q", "♕")
        board = board.replace("r", "♜").replace("n", "♞").replace("b", "♝").replace("k", "♚").replace("q", "♛")
        board = board.replace(".", "- ")
        
        bot.send_message(human_move.chat.id, board)
        return 1
    elif human_move.html_text == "Показать список ходов":
        count += 1
        if count_user > count:
            bot.send_message(message.chat.id, "Твое количество подсказок закончилось")
            return 1
        bot.send_message(human_move.chat.id, str(chess_moves[0:]))
        return 1
    elif human_move.html_text == "Обозначение фигур":
        bot.send_message(human_move.chat.id, "Обозначения фигур: K(♔) - король белых ; Q(♕) - ферзь белых; B(♗) - слон белых; N(♘) - конь белых; R (♖)- ладья белых;  P(♙) - пешка черных. k(♚) - король черных ; q(♛) - ферзь ) - b (♝) слон черных; n(♞) - конь черных; r(♜)- ладья черных;  p(♟) - пешка черных.")
        return 1
    elif human_move.html_text == "Как ходить?":
        rules = "Если вы хотите походить пешкой, например с поля e2 на поле e4, то вы можете записать этот ход, следующем способом: e2-e4  или e4 или  ♙e4. Если вы хотите походить, например конем с поля b1 на поле c3 , то вы можете записать этот ход, следующем способом: b1-c3  или Nс3 или  ♘с3.Короткая рокировка обозначается(0-0), а длинная (0-0-0)"

        bot.send_message(human_move.chat.id, rules)
        return 1
    return get_move(human_move.html_text, message)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global count_user
    if call.data == '/newgame':
        markup = telebot.types.InlineKeyboardMarkup()
        
        markup.add(telebot.types.InlineKeyboardButton(text='5', callback_data='count_user5'))
        markup.add(telebot.types.InlineKeyboardButton(text='10', callback_data='count_user10'))
        markup.add(telebot.types.InlineKeyboardButton(text='15', callback_data='count_user15'))
        markup.add(telebot.types.InlineKeyboardButton(text='20', callback_data='count_user20'))
        markup.add(telebot.types.InlineKeyboardButton(text='25', callback_data='count_user25'))
        markup.add(telebot.types.InlineKeyboardButton(text='30', callback_data='count_user30'))
        bot.send_message(call.message.chat.id, "Выбери сколько уровень сложности ( сколько раз ты можешь пользоваться подсказками)", reply_markup=markup)
        bot.callback_query_handler(func=lambda call: True)
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Я хочу играть белыми', callback_data='white'))
        markup.add(telebot.types.InlineKeyboardButton(text='Я хочу играть черными', callback_data='black'))
        bot.send_message(call.message.chat.id, 'Выбери каким цветом ты хочешь играть', reply_markup=markup)
        bot.callback_query_handler(func=lambda call: True)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == "white":
        bot.send_message(call.message.chat.id, 'У тебя будут кнопки-подсказки, удачи!', reply_markup=keyboard)
        create_game(call.message, iswhite=True)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == "black":
        bot.send_message(call.message.chat.id, 'У тебя будут кнопки-подсказки, удачи!', reply_markup=keyboard)
        create_game(call.message, iswhite=False)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == "count_user5":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        count_user = 5
    elif call.data == "count_user10":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        count_user = 10
    elif call.data == "count_user15":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        count_user = 15
    elif call.data == "count_user20":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        count_user = 20
    elif call.data == "count_user25":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        count_user = 25
    elif call.data == "count_user30":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        count_user = 30
    
    
    


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
        bot.send_message(message.chat.id, "Игра закончена, ты победил. Если хочешь начать слачала напиши команду '/start' ")
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
