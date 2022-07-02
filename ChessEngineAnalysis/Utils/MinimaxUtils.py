import chess
import chess.svg
import time

INF = float("inf")
MATE_SCORE = 99999
ttable = {}
htable = [[[0 for x in range(64)] for y in range(64)] for z in
          range(2)]

squares_index = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}


def rate(board, move, tt_move):
    if tt_move:
        return 600

    if htable[board.piece_at(move.from_square).color][move.from_square][move.to_square] != 0:
        return htable[board.piece_at(move.from_square).color][move.from_square][move.to_square] / -100

    if board.is_capture(move):
        if board.is_en_passant(move):
            return 0
        else:
            return (board.piece_at(move.to_square).piece_type - board.piece_at(move.from_square).piece_type) * 100

    if move.promotion:
        return 0

    return -1000


def get_num_pieces(board):
    return len(board.piece_map())


def null_move_ok(board):
    endgame_threshold = 14
    if (board.move_stack and board.peek() != chess.Move.null()) or board.is_check() or get_num_pieces(
            board) <= endgame_threshold:
        return False
    return True


def reduction_ok(board, move):
    result = True
    board.pop()
    if board.is_capture(move) or move.promotion or board.gives_check(move) or board.is_check():
        result = False
    board.push(move)
    return result


def is_square_a_file(square):
    return square % 8 == 0


def is_square_h_file(square):
    return (square + 1) % 8 == 0


def can_exit_search(movetime, stop, start_time):
    return stop() or (movetime - (time.time_ns() - start_time) * 10 ** -6) <= 0


def get_bb_king_zone(square, color):
    king_rank = chess.BB_RANKS[chess.square_rank(square)]
    bb_king_ranks = chess.SquareSet(king_rank)
    if color == chess.WHITE:
        if square + 8 <= 63:
            king_forward_rank = chess.BB_RANKS[chess.square_rank(square) + 1]
            bb_king_ranks |= chess.SquareSet(king_forward_rank)
            if square + 16 <= 63:
                king_forward_rank = chess.BB_RANKS[chess.square_rank(square) + 2]
                bb_king_ranks |= chess.SquareSet(king_forward_rank)
        if square - 8 >= 0:
            king_back_rank = chess.BB_RANKS[chess.square_rank(square) - 1]
            bb_king_ranks |= chess.SquareSet(king_back_rank)
    elif color == chess.BLACK:
        if square - 8 >= 0:
            king_forward_rank = chess.BB_RANKS[chess.square_rank(square) - 1]
            bb_king_ranks |= chess.SquareSet(king_forward_rank)
            if square - 16 >= 0:
                king_forward_rank = chess.BB_RANKS[chess.square_rank(square) - 2]
                bb_king_ranks |= chess.SquareSet(king_forward_rank)
        if square + 8 <= 63:
            king_back_rank = chess.BB_RANKS[chess.square_rank(square) + 1]
            bb_king_ranks |= chess.SquareSet(king_back_rank)

    king_file = chess.BB_FILES[chess.square_file(square)]
    bb_king_files = chess.SquareSet(king_file)
    if not is_square_a_file(square):
        king_left_file = chess.BB_FILES[chess.square_file(square - 1)]
        bb_king_files |= chess.SquareSet(king_left_file)
    if not is_square_h_file(square):
        king_right_file = chess.BB_FILES[chess.square_file(square + 1)]
        bb_king_files |= chess.SquareSet(king_right_file)

    bb_king_zone = bb_king_ranks & bb_king_files
    return bb_king_zone