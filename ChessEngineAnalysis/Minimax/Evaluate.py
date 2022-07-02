import chess.gaviota
from Utils.MinimaxUtils import *
from Utils.SqUtils import *

material_values = [100, 320, 330, 500, 900, MATE_SCORE]

eg_psqts = {
    "P": white_end_pawn_table,
    "N": white_end_knight_table,
    "B": white_end_bishop_table,
    "R": white_end_rook_table,
    "Q": white_end_queen_table,
    "K": white_end_king_table,
    "p": black_end_pawn_table,
    "n": black_end_knight_table,
    "b": black_end_bishop_table,
    "r": black_end_rook_table,
    "q": black_end_queen_table,
    "k": black_end_king_table,
}
mg_psqts = {
    "P": white_middle_pawn_table,
    "N": white_middle_knight_table,
    "B": white_middle_bishop_table,
    "R": white_middle_rook_table,
    "Q": white_middle_queen_table,
    "K": white_middle_king_table,
    "p": black_middle_pawn_table,
    "n": black_middle_knight_table,
    "b": black_middle_bishop_table,
    "r": black_middle_rook_table,
    "q": black_middle_queen_table,
    "k": black_middle_king_table,
}

phase_scores = [0, 1, 1, 2, 4, 0]
king_threat_table = [0, 0, 1, 2, 3, 5, 7, 9, 12, 15, 18, 22, 26, 30, 35, 39, 44, 50, 56, 62, 68, 75, 82, 85, 89, 97, 105, 113, 122, 131, 140, 150, 169, 180, 191, 202, 213, 225, 237, 248, 260, 272, 283, 295, 307, 319, 330, 342, 354, 366, 377, 389, 401, 412, 424, 436, 448, 459, 471, 483, 494, 500]

material_score = 0
psqt_mg_score = 0
psqt_eg_score = 0
phase = 0
total_phase = 16*phase_scores[chess.PAWN - 1] + 4*phase_scores[chess.KNIGHT - 1] + 4*phase_scores[chess.BISHOP - 1] \
            + 4*phase_scores[chess.ROOK - 1] + 2*phase_scores[chess.QUEEN - 1]
piece_specific_score = 0

b_bitboards = [0, 0, 0, 0, 0, 0, 0]
w_bitboards = [0, 0, 0, 0, 0, 0, 0]
bitboards = [b_bitboards, w_bitboards]

def evaluate(board):
    if board.is_checkmate():
        return -MATE_SCORE

    for color in [chess.WHITE, chess.BLACK]:
        for piece in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            squares = []
            bb = board.pieces(piece, color)
            for i, c in enumerate(bin(bb)[:1:-1], 1):
                if c == "1":
                    squares.append(i - 1)
            bitboards[color][piece] = (squares, bb)

    for color in [chess.WHITE, chess.BLACK]:
        relative_weight = 1 if color == board.turn else -1

        bb_king_zone = get_bb_king_zone(board.king(not color), not color)
        king_attack_units = 0

        for piece in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            piece_symbol = chess.piece_symbol(piece).upper() if color == chess.WHITE else chess.piece_symbol(piece).lower()
            squares, bb = bitboards[color][piece]
            for square in squares:
                material_score += material_values[piece - 1] * relative_weight

                psqt_mg_score += mg_psqts[piece_symbol][square] * relative_weight
                psqt_eg_score += eg_psqts[piece_symbol][square] * relative_weight
                phase += phase_scores[piece - 1]

                if piece == chess.PAWN:
                    passed_pawn_bonus = [0, 5, 10, 20, 40, 80, 160, 0]

                    pawn_file = chess.BB_FILES[chess.square_file(square)]
                    bb_passing_files = chess.SquareSet(pawn_file)
                    if not is_square_a_file(square):
                        pawn_left_file = chess.BB_FILES[chess.square_file(square - 1)]
                        bb_passing_files |= chess.SquareSet(pawn_left_file)
                    if not is_square_h_file(square):
                        pawn_right_file = chess.BB_FILES[chess.square_file(square + 1)]
                        bb_passing_files |= chess.SquareSet(pawn_right_file)
                    if len(bb_passing_files & bitboards[not color][chess.PAWN][1]) == 0:
                        if color == chess.WHITE:
                            piece_specific_score += passed_pawn_bonus[square // 8] * relative_weight
                        else:
                            piece_specific_score += passed_pawn_bonus[8 - ((square // 8) + 1)] * relative_weight

                    pawn_isolated_penalty = -20

                    if len(bb_passing_files & bitboards[color][chess.PAWN][1]) != 3:
                        piece_specific_score += pawn_isolated_penalty * relative_weight

                elif piece == chess.KNIGHT:
                    knight_outpost_bonus = 25
                    knight_squares = bitboards[color][chess.KNIGHT][0]
                    bb_pawns = bitboards[color][chess.PAWN][1]
                    for knight_square in knight_squares:
                        rank = chess.square_rank(square) + 1
                        if (color == chess.WHITE and (rank == 4 or rank == 5 or rank == 6)) or \
                            ((color == chess.BLACK) and (rank == 5 or rank == 4 or rank == 3)):
                                if len(board.attackers(color, knight_square) & bb_pawns) >= 1:
                                    piece_specific_score += knight_outpost_bonus * relative_weight
                                    break

                    king_attack_units += len(board.attacks(square) & bb_king_zone) * 2

                elif piece == chess.BISHOP:
                    king_attack_units += len(board.attacks(square) & bb_king_zone) * 2

                elif piece == chess.ROOK:
                    rook_open_file_bonus = 50
                    rook_file = chess.BB_FILES[chess.square_file(square)]
                    bb_rook_file = chess.SquareSet(rook_file)
                    bb_friend_pawns = bitboards[color][chess.PAWN][1]
                    bb_foe_pawns = bitboards[not color][chess.PAWN][1]
                    if len(bb_rook_file & bb_friend_pawns) == 0:
                        if len(bb_rook_file & bb_foe_pawns) == 0:
                            piece_specific_score += rook_open_file_bonus * relative_weight
                        else:
                            piece_specific_score += rook_open_file_bonus / 2 * relative_weight

                    # Bonus to attacks on the enemy king zone
                    king_attack_units += len(board.attacks(square) & bb_king_zone) * 3

                elif piece == chess.QUEEN:
                    # Penalty to pinned queen
                    queen_pinned_penalty = -50
                    squares_foe_sliders = bitboards[not color][chess.BISHOP][0] + bitboards[not color][chess.ROOK][0] + bitboards[not color][chess.QUEEN][0]
                    bb_foe_sliders = chess.SquareSet(chess.BB_EMPTY)
                    for foe_square in squares_foe_sliders:
                        bb_foe_sliders |= board.attacks(foe_square)
                    if board.attacks(square) & bb_foe_sliders != 0:
                        piece_specific_score += queen_pinned_penalty * relative_weight

                    king_attack_units += len(board.attacks(square) & bb_king_zone) * 5
                    piece_specific_score += king_threat_table[king_attack_units] * relative_weight

    mg_phase = max(phase, total_phase)
    eg_phase = total_phase - mg_phase
    psqt_score = (psqt_mg_score * mg_phase + psqt_eg_score * eg_phase) / total_phase

    mobility_score = 0

    material_weight = 10
    psqt_weight = 1
    mobility_weight = 1
    piece_specific_weight = 1
    score = (material_weight * material_score) + (psqt_weight * psqt_score) + (mobility_weight * mobility_score) + (piece_specific_weight * piece_specific_score)
    return score
        