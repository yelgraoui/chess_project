#method taken from https://www.chessprogramming.org/Simplified_Evaluation_Function

from utility import *
from pieces_classes import *
from moves import *

from enum import Enum

class Game_Status(Enum):
    WHITE_WINS = 0
    BLACK_WINS = 1
    DRAW = 2
    STILL_GOING = 3


w_pawn = [
 [0,  0,  0,  0,  0,  0,  0,  0],
 [50, 50, 50, 50, 50, 50, 50, 50],
 [10, 10, 20, 30, 30, 20, 10, 10],
 [5,  5, 10, 25, 25, 10,  5,  5],
 [0,  0,  0, 20, 20,  0,  0,  0],
 [5, -5,-10,  0,  0,-10, -5,  5],
 [5, 10, 10,-20,-20, 10, 10,  5],
 [0,  0,  0,  0,  0,  0,  0,  0]
]

w_knight = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
[-40,-20,  0,  0,  0,  0,-20,-40],
[-30,  0, 10, 15, 15, 10,  0,-30],
[-30,  5, 15, 20, 20, 15,  5,-30],
[-30,  0, 15, 20, 20, 15,  0,-30],
[-30,  5, 10, 15, 15, 10,  5,-30],
[-40,-20,  0,  5,  5,  0,-20,-40],
[-50,-40,-30,-30,-30,-30,-40,-50]
]

w_bishop = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
[-10,  0,  0,  0,  0,  0,  0,-10],
[-10,  0,  5, 10, 10,  5,  0,-10],
[-10,  5,  5, 10, 10,  5,  5,-10],
[-10,  0, 10, 10, 10, 10,  0,-10],
[-10, 10, 10, 10, 10, 10, 10,-10],
[-10,  5,  0,  0,  0,  0,  5,-10],
[-20,-10,-10,-10,-10,-10,-10,-20]
]

w_rook = [
  [0,  0,  0,  0,  0,  0,  0,  0],
  [5, 10, 10, 10, 10, 10, 10,  5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
  [0,  0,  0,  5,  5,  0,  0,  0]
]

w_queen = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
[-10,  0,  0,  0,  0,  0,  0,-10],
[-10,  0,  5,  5,  5,  5,  0,-10],
 [-5,  0,  5,  5,  5,  5,  0, -5],
  [0,  0,  5,  5,  5,  5,  0, -5],
[-10,  5,  5,  5,  5,  5,  0,-10],
[-10,  0,  5,  0,  0,  0,  0,-10],
[-20,-10,-10, -5, -5,-10,-10,-20]
]

w_king_middlegame = [
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-20,-30,-30,-40,-40,-30,-30,-20],
[-10,-20,-20,-20,-20,-20,-20,-10],
 [20, 20,  0,  0,  0,  0, 20, 20],
 [20, 30, 10,  0,  0, 10, 30, 20]
]

w_king_endgame = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
[-30,-20,-10,  0,  0,-10,-20,-30],
[-30,-10, 20, 30, 30, 20,-10,-30],
[-30,-10, 30, 40, 40, 30,-10,-30],
[-30,-10, 30, 40, 40, 30,-10,-30],
[-30,-10, 20, 30, 30, 20,-10,-30],
[-30,-30,  0,  0,  0,  0,-30,-30],
[-50,-30,-30,-30,-30,-30,-30,-50]
]

P = 100
N = 320
B = 330
R = 500
Q = 900
K = 20000

def evaluate_board(square_piece_board, bitboard):

    two_queens_onboard = False
    w_king = []

    for i in range(8):
        for j in range(8):
            if square_piece_board[i][j] != -1 and get_type(bitboard[square_piece_board[i][j]]) == Piece.QUEEN:
                two_queens_onboard = True
                break

    if two_queens_onboard:
        w_king = w_king_middlegame
    else:
        w_king = w_king_endgame

    score = 0

    for i in range(8):
        for j in range(8):
            if square_piece_board[i][j] != -1:
                piece_info = bitboard[square_piece_board[i][j]]
                piece_type = get_type(piece_info)
                piece_color = get_color(piece_info)
                correct_row_to_look = i
                if piece_color == Color.BLACK:
                    correct_row_to_look = 7-i
                
                sign_color = 1 if piece_color == Color.WHITE else -1

                match piece_type:
                    case Piece.PAWN:
                        score += (w_pawn[correct_row_to_look][j] + P)*sign_color
                    case Piece.KNIGHT:
                        score += (w_knight[correct_row_to_look][j] + N)*sign_color
                    case Piece.BISHOP:
                        score += (w_bishop[correct_row_to_look][j] + B)*sign_color
                    case Piece.ROOK:
                        score += (w_rook[correct_row_to_look][j] + R)*sign_color
                    case Piece.QUEEN:
                        score += (w_queen[correct_row_to_look][j] + Q)*sign_color
                    case Piece.KING:
                        score += (w_king[correct_row_to_look][j] + K)*sign_color

    return score




def evaluate(square_piece_board, bitboard, dict_positions, rule_50_moves, turn, last_move, kings_id, pieces_list):

    if rule_50_moves == 100:
        return (0, Game_Status.DRAW)
    
    board_rep = representation_of_board(square_piece_board, bitboard)
    if board_rep in dict_positions and dict_positions[board_rep] == 3:
        return (0, Game_Status.DRAW)

    
    #get the color turn
    king_row = get_row(bitboard[kings_id[turn.value]])
    king_col = get_column(bitboard[kings_id[turn.value]])

    #check if there are attacks of the king
    if valid_after_scan_for_king_checks_after_move(king_row, king_col, king_row, \
                                                    king_col, square_piece_board, bitboard, kings_id[turn.value], MOVE.NORMAL):
        
        #if none, verify that the color turn can generate moves
        if len(move_generation(pieces_list, square_piece_board, bitboard, last_move, kings_id, turn)) == 0:
            return (0, Game_Status.DRAW)
        return (evaluate_board(square_piece_board, bitboard), Game_Status.STILL_GOING)

    #we are under check
    else:
        #no moves possible
        if len(move_generation(pieces_list, square_piece_board, bitboard, last_move, kings_id, turn)) == 0:
            if turn == Color.WHITE:
                return (-1000000000000000000000000000000, Game_Status.BLACK_WINS)
            else:
                return (1000000000000000000000000000000, Game_Status.WHITE_WINS)
        #can still move
        else:
            return (evaluate_board(square_piece_board, bitboard), Game_Status.STILL_GOING)



import copy

def alpha_beta(depth, alpha, beta, maximising_player, \
               square_piece_board, bitboard, is_en_passant_possible_for_next_player, dict_positions, \
             rule_50_moves, turn, last_move, kings_id, white_piece, black_piece):

    node_evaluation = evaluate(square_piece_board, bitboard, dict_positions, \
                     rule_50_moves, turn, last_move, kings_id, white_piece if turn == Color.WHITE else black_piece)

    if depth == 0 or node_evaluation[1] != Game_Status.STILL_GOING:
        return (node_evaluation, None)


    game_status_ = Game_Status.STILL_GOING
    if turn == Color.WHITE:
        value = -1000000000000000000000000000000
        move_to_make = None
        possible_moves = move_generation(white_piece, square_piece_board, bitboard, last_move, kings_id, turn)
        # print("WHITE : ", possible_moves)
        for move in possible_moves:
            old_row = get_row(bitboard[move[0]])
            old_col = get_column(bitboard[move[0]])

            id_piece = move[0]
            new_row = move[1]
            new_col = move[2]
            type_of_move = move[3]
            type_promotion = move[4]

            piece_captured = -1
            info_on_piece = None

            old_en_passant = is_en_passant_possible_for_next_player
            old_last_moves = copy.deepcopy(last_move)
            old_rule_50 = rule_50_moves

            last_move[0] = bitboard[move[0]]

            if get_type(bitboard[move[0]]) == Piece.PAWN and abs(old_row - new_row) == 2:
                if new_col - 1 >= 0 and square_piece_board[new_row][new_col-1] != -1 \
                    and get_type(bitboard[square_piece_board[new_row][new_col-1]]) == Piece.PAWN:
                        is_en_passant_possible_for_next_player = True
                if new_col + 1 <= 7 and square_piece_board[new_row][new_col+1] != -1 \
                    and get_type(bitboard[square_piece_board[new_row][new_col+1]]) == Piece.PAWN:
                        is_en_passant_possible_for_next_player = True

            old_type, piece_captured, old_has_moved = make_move(id_piece, old_row, old_col, new_row, new_col, \
                      square_piece_board, bitboard, kings_id[Color.WHITE.value], type_of_move, type_promotion)

            if old_type == Piece.PAWN:
                rule_50_moves = 0

            if piece_captured != -1:
                black_piece.remove(piece_captured)
                rule_50_moves = 0

            board_rep = representation_of_board(square_piece_board, bitboard)
            if board_rep in dict_positions:
                dict_positions[board_rep] += 1
            else:
                if not old_en_passant:
                    dict_positions[board_rep] = 1


            last_move[1] = bitboard[move[0]]
            #call recursion
            evaluation_child = alpha_beta(depth-1, alpha, beta, maximising_player ^ True, \
               square_piece_board, bitboard, is_en_passant_possible_for_next_player, dict_positions, \
             rule_50_moves, Color.BLACK, last_move, kings_id, white_piece, black_piece)



            #unmake move
            unmake_move(id_piece, old_row, old_col, new_row, new_col, square_piece_board, bitboard, \
                        kings_id[Color.WHITE.value], type_of_move, old_type, piece_captured, old_has_moved)

            if piece_captured != -1:
                black_piece.append(piece_captured)

            if board_rep in dict_positions:
                dict_positions[board_rep] = max(0, dict_positions[board_rep] - 1)

            last_move = copy.deepcopy(old_last_moves)
            rule_50_moves = old_rule_50
            is_en_passant_possible_for_next_player = old_en_passant

            # print(move, evaluation_child)
            if evaluation_child[0][0] > value:
                # print("hello there")
                move_to_make = move    
            value = max(value, evaluation_child[0][0])
            if value >= beta:
                # print("hello there bis")
                #move_to_make = move
                game_status_ = evaluation_child[0][1]
                break
            alpha = max(alpha, value)

        return ((value, game_status_), move_to_make)
    else:
        #same but for blacks
        value = 1000000000000000000000000000000
        move_to_make = None
        possible_moves = move_generation(black_piece, square_piece_board, bitboard, last_move, kings_id, turn)
        for move in possible_moves:
            old_row = get_row(bitboard[move[0]])
            old_col = get_column(bitboard[move[0]])
            old_type = get_type(bitboard[move[0]])

            id_piece = move[0]
            new_row = move[1]
            new_col = move[2]
            type_of_move = move[3]
            type_promotion = move[4]

            piece_captured = -1
            info_on_piece = None

            old_en_passant = is_en_passant_possible_for_next_player
            old_last_moves = copy.deepcopy(last_move)
            old_rule_50 = rule_50_moves

            last_move[0] = bitboard[move[0]]
            #make move
            

            if get_type(bitboard[move[0]]) == Piece.PAWN and abs(old_row - new_row) == 2:
                if new_col - 1 >= 0 and square_piece_board[new_row][new_col-1] != -1 \
                    and get_type(bitboard[square_piece_board[new_row][new_col-1]]) == Piece.PAWN:
                        is_en_passant_possible_for_next_player = True
                if new_col + 1 <= 7 and square_piece_board[new_row][new_col+1] != -1 \
                    and get_type(bitboard[square_piece_board[new_row][new_col+1]]) == Piece.PAWN:
                        is_en_passant_possible_for_next_player = True

            old_type, piece_captured, old_has_moved = make_move(id_piece, old_row, old_col, new_row, new_col, \
                      square_piece_board, bitboard, kings_id[Color.BLACK.value], type_of_move, type_promotion)      

            if old_type == Piece.PAWN:
                rule_50_moves = 0
            if piece_captured != -1:
                white_piece.remove(piece_captured)
                rule_50_moves = 0      

            board_rep = representation_of_board(square_piece_board, bitboard)
            if board_rep in dict_positions:
                dict_positions[board_rep] += 1
            else:
                if not old_en_passant:
                    dict_positions[board_rep] = 1


            last_move[1] = bitboard[move[0]]
            #call recursion
            evaluation_child = alpha_beta(depth-1, alpha, beta, maximising_player ^ True, \
               square_piece_board, bitboard, is_en_passant_possible_for_next_player, dict_positions, \
             rule_50_moves, Color.WHITE, last_move, kings_id, white_piece, black_piece)



            #unmake move
            unmake_move(id_piece, old_row, old_col, new_row, new_col, square_piece_board, bitboard, \
                        kings_id[Color.BLACK.value], type_of_move, old_type, piece_captured, old_has_moved)

            if piece_captured != -1:
                white_piece.append(piece_captured)

            if board_rep in dict_positions:
                dict_positions[board_rep] = max(0, dict_positions[board_rep] - 1)

            last_move = copy.deepcopy(old_last_moves)
            rule_50_moves = old_rule_50
            is_en_passant_possible_for_next_player = old_en_passant

            if evaluation_child[0][0] < value:
                # print("modify me :(")
                move_to_make = move
            value = min(value, evaluation_child[0][0])
            if value <= alpha:
                # print("sad")
                #move_to_make = move
                game_status_ = evaluation_child[0][1]
                break
            beta = min(beta, value)
        #print(move_to_make)
        return ((value, game_status_), move_to_make)