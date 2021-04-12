import chess
import chess.engine
import sys 

engine = chess.engine.SimpleEngine.popen_uci("/Users/konstantinsavkin/chess_engines/stockfish/13/bin/stockfish")
board = chess.Board()

def get_move(possible_move):
    try:
        move = board.parse_san(possible_move)
        if move in board.legal_moves:
            return move
    except:
        return None



while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)

    print(result.move)
    print(board)

    human_move = input()

    move = get_move(human_move)
    if move == None:
        print ("invalid movie")
        continue

    board.push(move)
 
 


engine.quit()


