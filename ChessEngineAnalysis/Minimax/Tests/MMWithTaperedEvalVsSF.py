import time

import chess
from chess import engine
from chess import pgn

from MCST.search import cpu_move
from Utils.openingLibrary import openingLibrary

SF = chess.engine.SimpleEngine.popen_uci(
    "../../Utils/stockfish_14.1_win_x64_avx2/stockfish_14.1_win_x64_avx2.exe"
)
game = chess.Board()

pgn = chess.pgn.Game()
pgn.setup(game)
node = pgn



for depth in range(4, 5):

    for i in range(0, 50):
        f = open("MMWithTaperedEvalvsSF.csv", "a")
        print(i + 1)
        result = []
        game = chess.Board()
        game.reset_board()
        move_time = 0
        move_counter = 0

        pgn = chess.pgn.Game()
        pgn.setup(game)
        node = pgn

        # opening = random.choice(openingLibrary)
        opening = openingLibrary[i]
        # opening = ['d4', 'g6']
        for opening_move in opening:
            move = game.parse_san(opening_move)
            game.push(chess.Move.from_uci(str(move)))
            node = node.add_variation(move)
        print(opening)

        start_time = time.time()
        while not game.is_game_over():
            if game.turn:
                move_time_start = time.time()
                move = cpu_move(game, depth)
                move = chess.Move.from_uci(str(move))
                game.push(move)
                move_counter += 1
                move_time += time.time() - move_time_start
                node = node.add_variation(move)

            else:
                engine_move = SF.play(game, chess.engine.Limit(depth=0))
                game.push(engine_move.move)
                node = node.add_variation(engine_move.move)
                print(engine_move.move)

        game_time = time.time() - start_time

        result.append(str(i + 1) + ',')
        if str(game.result()) == '1-0':
            result.append(str(1) + ',')
        elif str(game.result()) == '1/2-1/2':
            result.append(str(0.5) + ',')
        else:
            result.append(str(0) + ',')

        print(pgn)
        result.append(str(opening) + ',')
        result.append(str(pgn.variations[0]) + ',')
        result.append(str(game_time) + ',')
        result.append(str(move_time / move_counter) + ',')
        result.append("\n")
        f.write(''.join(result))
        f.close()
