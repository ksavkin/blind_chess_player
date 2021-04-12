import chess
import chess.engine


def valid_chess_moves(human_move):
    if chess.Move.from_uci(human_move.html_text) in board.legal_moves:
        return True
    return False

def get_move(human_move):
    try:
        move = board.push_san(human_move)
        if valid_chess_moves(human_move):
            return move
    except:
        return None



engine = chess.engine.SimpleEngine.popen_uci("/Users/konstantinsavkin/chess_engines/stockfish/13/bin/stockfish")

board = chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)

    print(result.move)
    print(board)

    human_move = input()

    uci = get_move(human_move)
    if uci == None:
        print ("invalid movie")
        continue

    board.push(uci)
 
 


engine.quit()


