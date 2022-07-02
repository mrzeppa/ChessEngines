import random
import time

import chess
from chess import engine
from chess import pgn
from Minimax import Minimax
from Utils.openingLibrary import openingLibrary

SF = chess.engine.SimpleEngine.popen_uci(
    "../Utils/stockfish_14.1_win_x64_avx2/stockfish_14.1_win_x64_avx2.exe"
)

for i in range(0, 50):
    f = open("MMvsSF2.txt", "a")
    print(i + 1)
    result = []
    game = chess.Board()
    game.reset_board()

    pgn = chess.pgn.Game()
    pgn.setup(game)
    node = pgn

    opening = random.choice(openingLibrary)
    print(opening)
    for opening_move in opening:
        move = game.parse_san(opening_move)
        game.push(chess.Move.from_uci(str(move)))
        node = node.add_variation(move)

    start_time = time.time()
    while not game.is_game_over():
        if game.turn:
            move = Minimax.getMove(4, game, True, True)
            move = chess.Move.from_uci(str(move))
            game.push(move)
            node = node.add_variation(move)
        else:
            engine_move = SF.play(game, chess.engine.Limit(time=0.005))
            game.push(engine_move.move)
            node = node.add_variation(engine_move.move)

    game_time = time.time() - start_time
    result.append(str(i + 1) + ',')
    if str(game.result()) == '1-0':
        result.append(str(1) + ',')
    else:
        result.append(str(0) + ',')
    # result.append(str(game.result())+',')
    result.append(str(pgn.variations[0]) + ',')
    result.append(str(game_time) + ',')
    result.append("\n")
    f.write(''.join(result))
    f.close()

# Pokazanie przykladowej partii done
# Bezposrednie MMvsSF Biale done
# Bezposrednie MMvsSF Czarne done
# MM sredni czas na ruch w zaleznosci od glebokosci done
# Bezposrednie starcie gdy na ruch dostaniemy srednia/2 czasu
# Czas z obcinaniem galezi vs bez obcinania galezi przy glebokosci 4
#
