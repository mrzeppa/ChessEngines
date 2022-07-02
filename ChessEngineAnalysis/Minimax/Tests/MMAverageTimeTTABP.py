import random

from MCST.search import *
import chess

from Utils.openingLibrary import openingLibrary

game = chess.Board()

for depth in range(1, 5):

    for i in range(0, 26):
        f = open("MMAverageTimeTTABP.csv", "a")
        print(i + 1)
        result = []
        game = chess.Board()
        game.reset_board()
        move_time = 0
        move_counter = 0

        start_time = time.time()
        while not game.is_game_over():
            if game.turn:
                move_time_start = time.time()
                move = cpu_move(game, depth)
                move = chess.Move.from_uci(str(move))
                game.push(move)
                move_time += time.time() - move_time_start
                move_counter += 1
            else:
                move_time_start = time.time()
                move = cpu_move(game, depth)
                move = chess.Move.from_uci(str(move))
                game.push(move)
                move_time += time.time() - move_time_start
                move_counter += 1
        ttable.clear()

        game_time = time.time() - start_time
        result.append(str(i + 1)+';')
        result.append(str(depth)+';')
        result.append(str(game_time) + ';')
        result.append(str(move_time/move_counter)+';')
        result.append("\n")
        f.write(''.join(result))
        f.close()
