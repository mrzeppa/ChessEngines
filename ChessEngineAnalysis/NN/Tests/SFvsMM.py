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
    f = open("SFvsMM.txt", "a")
    print(i + 1)
    result = []
    game = chess.Board()
    game.reset_board()

    pgn = chess.pgn.Game()
    pgn.setup(game)
    node = pgn

    is_minimax_as_white = random.choice([True, True])

    opening = random.choice(openingLibrary)
    print(opening)
    for opening_move in opening:
        move = game.parse_san(opening_move)
        game.push(chess.Move.from_uci(str(move)))
        node = node.add_variation(move)

    start_time = time.time()
    while not game.is_game_over() and not game.is_checkmate():
        engine_move = SF.play(game, chess.engine.Limit(time=0.1))
        print(engine_move.move)
        game.push(engine_move.move)
        node = node.add_variation(engine_move.move)

        move = Minimax.getMove(1, game, True, False)
        print("-" + str(move))
        move = chess.Move.from_uci(str(move))
        game.push(move)
        node = node.add_variation(move)

    game_time = time.time() - start_time
    result.append(str(i + 1)+',')
    if str(game.result()) == '1-0':
        result.append(str(0)+',')
    else:
        result.append(str(1)+',')
    # result.append(str(game.result())+',')
    result.append(str(pgn.variations[0])+',')
    result.append(str(game_time)+',')
    result.append("\n")
    f.write(''.join(result))
    f.close()

# Pokazanie przykladowej partii
# Bezposrednie MMvsSF Biale
# Bezposrednie MMvsSF Czarne
# MM sredni czas na ruch w zaleznosci od glebokosci
# Bezposrednie starcie gdy na ruch dostaniemy srednia/2 czasu
# Czas z obcinaniem galezi vs bez obcinania galezi przy glebokosci 4
#
