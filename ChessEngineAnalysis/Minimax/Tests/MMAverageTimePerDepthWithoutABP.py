import random

from MCST.search import *
import chess

from Minimax.Minimax import getMove
from Utils.openingLibrary import openingLibrary

game = chess.Board()

for depth in range(1, 6):

    for i in range(0, 10):
        f = open("MMAverageTimePerDepthNoABP.csv", "a")
        print(i + 1)
        result = []
        game = chess.Board()
        game.reset_board()
        move_time = 0
        move_counter = 0

        opening = openingLibrary[i]
        for opening_move in opening:
            move = game.parse_san(opening_move)
            game.push(chess.Move.from_uci(str(move)))

        ttable.clear()
        start_time = time.time()
        while not game.is_game_over():
            if game.turn:
                move_time_start = time.time()
                move = cpu_move(game, depth)
                move = chess.Move.from_uci(str(move))
                print(move)
                game.push(move)
                move_time += time.time() - move_time_start
                move_counter += 1
            else:
                move_time_start = time.time()
                move = cpu_move(game, depth)
                move = chess.Move.from_uci(str(move))
                print(move)

                game.push(move)
                move_time += time.time() - move_time_start
                move_counter += 1

        game_time = time.time() - start_time
        result.append(str(i + 1)+';')
        result.append(str(depth)+';')
        result.append(str(game_time) + ';')
        result.append(str(move_time/move_counter)+';')
        result.append("\n")
        f.write(''.join(result))
        f.close()
