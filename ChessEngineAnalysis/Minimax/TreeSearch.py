import chess.polyglot
from Evaluate import *

def qsearch(board, alpha, beta, movetime=INF, stop=lambda: False):

    global nodes

    if can_exit_search(movetime, stop, start_time):
        return 0

    stand_pat = evaluate(board)
    nodes += 1

    if stand_pat >= beta:
        return beta
    alpha = max(alpha, stand_pat)

    captures = list(board.generate_legal_captures())
    captures.sort(key=lambda move: rate(board, move, None), reverse=True)
    for capture in captures:
        board.push(capture)
        score = -qsearch(board, -beta, -alpha, movetime, stop)
        board.pop()

        if score >= beta:
            return beta
        alpha = max(alpha, score)
    return alpha


def negamax(board, depth, alpha, beta, movetime=INF, stop=lambda: False):
    global nodes

    if can_exit_search(movetime, stop, start_time):
        return (None, 0)

    key = chess.polyglot.zobrist_hash(board)
    tt_move = None

    if key in ttable:
        tt_depth, tt_move, tt_score, flag = ttable[key]
        if tt_depth >= depth:
            nodes += 1
            if flag == "EXACT":
                return (tt_move, tt_score)
            elif flag == "LOWERBOUND":
                alpha = max(alpha, tt_score)
            elif flag == "UPPERBOUND":
                beta = min(beta, tt_score)
            if alpha >= beta:
                return (tt_move, tt_score)

    old_alpha = alpha
    if depth <= 0 or board.is_game_over():
        score = qsearch(board, alpha, beta, movetime, stop)
        return (None, score)
    else:
        if null_move_ok(board):
            null_move_depth_reduction = 2
            board.push(chess.Move.null())
            score = -negamax(board, depth - 1 - null_move_depth_reduction, -beta, -beta + 1, movetime, stop)[1]
            board.pop()
            if score >= beta:
                return (None, score)

        best_move = None
        best_score = -INF
        moves = list(board.legal_moves)
        moves.sort(key=lambda move: rate(board, move, tt_move), reverse=True)

        moves_searched = 0
        failed_high = False

        for move in moves:
            board.push(move)

            late_move_depth_reduction = 0
            full_depth_moves_threshold = 4
            reduction_threshold = 3
            if moves_searched >= full_depth_moves_threshold and failed_high == False and depth >= reduction_threshold and reduction_ok(
                    board, move):
                late_move_depth_reduction = 1

            score = -negamax(board, depth - 1 - late_move_depth_reduction, -beta, -alpha, movetime, stop)[1]
            board.pop()
            moves_searched += 1

            if score > best_score:
                best_move = move
                best_score = score

            alpha = max(alpha, best_score)

            if alpha >= beta:
                if not board.is_capture(move):
                    htable[board.piece_at(move.from_square).color][move.from_square][
                        move.to_square] += depth ** 2
                break

        tt_flag = "EXACT"
        if best_score <= old_alpha:
            tt_flag = "UPPERBOUND"
        elif best_score >= beta:
            tt_flag = "LOWERBOUND"
        ttable[key] = (depth, best_move, best_score, tt_flag)

        return (best_move, best_score)


def generate_move(board, depth, movetime=INF, stop=lambda: False):
    global nodes
    global start_time

    move = None
    score = 0
    results = []
    d = 0
    for d in range(1, depth + 1):
        if can_exit_search(movetime, stop, start_time):
            break
        move, score = negamax(board, d, -MATE_SCORE, MATE_SCORE, movetime, stop)

    if results:
        move, score, d, nodes, start_time = results[-1]

    return (move, score)


def cpu_move(board, depth, movetime=INF, stop=lambda: False):
    global OPENING_BOOK
    global ttable
    global htable

    global nodes
    global start_time

    nodes = 0
    move = generate_move(board, depth, movetime, stop)[0]
    return move
