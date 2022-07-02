import chess
import Utils
import time
from Utils.OpeningLibrary import openingLibrary

board = chess.Board()

pgn = chess.pgn.Game()
pgn.setup(board)
node = pgn

for i in range(0, 50):
    f = open("NNvsSFD4modelv3 .csv", "a")
    print(i+1)
    result = []
    board = chess.Board()
    board.reset_board()
    move_time = 0
    move_counter = 0

    pgn = chess.pgn.Game()
    pgn.setup(board)
    node = pgn

    for opening_move in openingLibrary[i]:
        move = board.parse_san(opening_move)
        board.push(chess.Move.from_uci(str(move)))
        node = node.add_variation(move)


    start_time = time.time()
    while not board.is_game_over():
        if board.turn:
            move_time_start = time.time()
            move = Utils.get_ai_move(board, 3)
            move = chess.Move.from_uci(str(move))
            print(move)
            board.push(move)
            move_counter += 1
            move_time += time.time() - move_time_start
            node = node.add_variation(move)

        else:
            engine_move = Utils.SF.play(board, chess.engine.Limit(time=0.1))
            board.push(engine_move.move)
            node = node.add_variation(engine_move.move)
            print(engine_move.move)

    game_time = time.time() - start_time
    result.append(str(i + 1) + ';')
    if str(board.result()) == '1-0':
        result.append(str(1) + ';')
    elif str(board.result()) == '1/2-1/2':
        result.append(str(0.5)+';')
    else:
        result.append(str(0) + ';')

    result.append(str(openingLibrary[i])+';')
    result.append(str(pgn.variations[0]) + ';')
    result.append(str(game_time) + ';')
    result.append(str(move_time/move_counter)+';')
    result.append("\n")
    f.write(''.join(result))
    f.close()