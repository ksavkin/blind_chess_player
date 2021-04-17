import telebot
import chess
import chess.engine

bot = telebot.TeleBot('1728273090:AAHfWDqNNQjXs2UffWj_ool8ySD6vyTMKbg')
engine = chess.engine.SimpleEngine.popen_uci(
    "/Users/konstantinsavkin/chess_engines/stockfish/13/bin/stockfish")
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Показать доску', 'Показать список ходов',
             'Обозначение фигур', 'Начать новую игру')
counts_user = {}
counts = {}
chess_moves = []

users = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    global users
    counts[message.chat.id] = 0
    counts_user[message.chat.id] = 0
    if message.chat.id not in users:
        users[message.chat.id] = chess.Board()
    else:
        users[message.chat.id] = chess.Board()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(
    text='Новая игра', callback_data='/newgame'))
    

    bot.send_message(
        message.chat.id, 'Привет я - бот для слепой игры в шахматы, давай сыграем ! ', reply_markup=markup)
    
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
    global counts
    global counts_user
    if human_move.html_text == "Показать доску":
        counts[message.chat.id] += 1
        if counts[message.chat.id] > counts_user[message.chat.id]:
            bot.send_message(
                message.chat.id, "Твое количество подсказок закончилось")
            return 1
        board = str(users[message.chat.id]).replace("P", "♙").replace(
            "p", "♟").replace("R", "♖").replace("N", "♘")
        board = board.replace("B", "♗").replace("K", "♔").replace("Q", "♕")
        board = board.replace("r", "♜").replace("n", "♞").replace(
            "b", "♝").replace("k", "♚").replace("q", "♛")
        board = board.replace(".", "- ")

        bot.send_message(human_move.chat.id, board)
        return 1
    elif human_move.html_text == "Показать список ходов":
        counts[message.chat.id] += 1
        if counts[message.chat.id] > counts_user[message.chat.id]:
            bot.send_message(
                message.chat.id, "Твое количество подсказок закончилось")
            return 1
        bot.send_message(human_move.chat.id, str(chess_moves[0:]))
        return 1
    elif human_move.html_text == "Обозначение фигур":
        bot.send_message(human_move.chat.id, "Обозначения фигур: K(♔) - король белых \n Q(♕) - ферзь белых \n B(♗) - слон белых \n N(♘) - конь белых \n R (♖)- ладья белых \n P(♙) - пешка черных. k(♚) - король черных \n q(♛) - ферзь ) - b (♝) слон черных \n n(♞) - конь черных \n r(♜)- ладья черных \n p(♟) - пешка черных.")
        return 1

    elif human_move.html_text == "Начать новую игру":
        start_message(message)
    return get_move(human_move.html_text, message)
def choose_color(call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(
            text='Я хочу играть белыми', callback_data='white'))
    markup.add(telebot.types.InlineKeyboardButton(
            text='Я хочу играть черными', callback_data='black'))
    bot.send_message(
            call.message.chat.id, 'Выбери каким цветом ты хочешь играть', reply_markup=markup)
    bot.callback_query_handler(func=lambda call: True)
    bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
    bot.callback_query_handler(func=lambda call: True)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global counts
    global counts_user
    if call.data == '/newgame':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            text='0', callback_data='count_user0'))
        markup.add(telebot.types.InlineKeyboardButton(
            text='1', callback_data='count_user1'))
        markup.add(telebot.types.InlineKeyboardButton(
            text='3', callback_data='count_user3'))
        markup.add(telebot.types.InlineKeyboardButton(
            text='5', callback_data='count_user5'))
        markup.add(telebot.types.InlineKeyboardButton(
            text="7", callback_data='count_user7'))
        markup.add(telebot.types.InlineKeyboardButton(
            text='9', callback_data='count_user9'))
        markup.add(telebot.types.InlineKeyboardButton(
            text='11', callback_data='count_user11'))
        markup.add(telebot.types.InlineKeyboardButton(
            text='13', callback_data='count_user13'))
        bot.send_message(
            call.message.chat.id, "Выбери сколько уровень сложности ( сколько раз ты можешь пользоваться подсказками)", reply_markup=markup)
        
    elif call.data == "white":
        bot.send_message(
            call.message.chat.id, 'У тебя будут кнопки-подсказки, удачи!', reply_markup=keyboard)
        create_game(call.message, iswhite=True)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
    elif call.data == "black":
        bot.send_message(
            call.message.chat.id, 'У тебя будут кнопки-подсказки, удачи!', reply_markup=keyboard)
        create_game(call.message, iswhite=False)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
    elif call.data == "count_user0":
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        counts_user[call.message.chat.id] = 0
        choose_color(call)
    elif call.data == "count_user1":
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        counts_user[call.message.chat.id] = 1
        choose_color(call)
    elif call.data == "count_user3":
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        counts_user[call.message.chat.id] = 3
        choose_color(call)
    elif call.data == "count_user5":
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        counts_user[call.message.chat.id] = 5
        choose_color(call)
    elif call.data == "count_user7":
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        counts_user[call.message.chat.id] = 7
        choose_color(call)
    elif call.data == "count_user9":
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        counts_user[call.message.chat.id] = 9
        choose_color(call)
    elif call.data == "count_user11":
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        counts_user[call.message.chat.id] = 11
        choose_color(call)
    elif call.data == "count_user13":
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        counts_user[call.message.chat.id] = 13
        choose_color(call)


def create_game(message, iswhite):
    if not iswhite:

        result = engine.play(users[message.chat.id],
                             chess.engine.Limit(time=0.1))
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
        bot.send_message(
            message.chat.id, "Игра закончена, ты победил. Если хочешь начать слачала напиши команду '/start' ")
        return

    result = engine.play(users[message.chat.id], chess.engine.Limit(time=0.1))
    chess_moves.append(str(result.move))
    users[message.chat.id].push(result.move)
    bot.send_message(message.chat.id, result.move)

    if users[message.chat.id].is_checkmate():
        users[message.chat.id] = chess.Board()
        bot.send_message(
            message.chat.id, "Игра закончена, я победил. Если хочешь начать слачала напиши команду '/start' ")
        return
    else:
        bot.send_message(message.chat.id, "Твой ход")


bot.polling()
