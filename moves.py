import math
from utility import *
import copy

from enum import Enum

class MOVE(Enum):
    NORMAL = 0
    CASTLE = 1
    EN_PASSANT = 2
    PROMOTION = 3

def check_bounds(r, c):
    return r >= 0 and r < 8 and c >= 0 and c < 8


def valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, king_id, move_type):
    copy_piece_square_board = copy.deepcopy(piece_square_board)
    copy_bitboard = copy.deepcopy(bitboard)

    id_piece = piece_square_board[r1][c1]

    set_new_coord(copy_bitboard, r2, c2, id_piece)

    king_info = copy_bitboard[king_id]

    if move_type == MOVE.CASTLE:
        check1 = valid_after_scan_for_king_checks_after_move(r1, c1, r1, c1, piece_square_board, bitboard, king_id, MOVE.NORMAL)
        if not check1:
            return False
        sign = (c2-c1)//abs(c2-c1)
        check2 = valid_after_scan_for_king_checks_after_move(r1, c1, r1, c1+sign, piece_square_board, bitboard, king_id, MOVE.NORMAL)
        if not check2:
            return False
        #no need to move the rook because it does not give us any additional meaningful check verification. Only need to check that arriving 
        #square is safe
        
    if move_type == MOVE.EN_PASSANT:
        #sign = 1 if get_color(bitboard[king_id]) == Color.WHITE else -1
        copy_piece_square_board[r1][c2] = -1

    copy_piece_square_board[r1][c1] = -1
    copy_piece_square_board[r2][c2] = id_piece

    king_row = get_row(king_info)
    king_col = get_column(king_info)

    #verify if no knight is attacking
    L = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for (x, y) in L:
        row = king_row+x
        col = king_col+y
        if row < 8 and row >= 0 and col >= 0 and col < 8:
            if copy_piece_square_board[row][col] != -1 and get_color(copy_bitboard[copy_piece_square_board[row][col]]) != get_color(king_info) \
                and get_type(copy_bitboard[copy_piece_square_board[row][col]]) == Piece.KNIGHT:
                print("knight attacking")
                return False
        

    #scan if the rows and columns starting frmo the king are safe
    for i in range(king_row+1, 8):
        current_id = copy_piece_square_board[i][king_col]
        if current_id != -1:
            type_piece = get_type(bitboard[current_id])
            color_piece = get_color(bitboard[current_id])
            if color_piece == get_color(king_info) or type_piece == Piece.PAWN or type_piece == Piece.BISHOP or type_piece == Piece.KNIGHT:
                break
            else:
                if type_piece == Piece.QUEEN or type_piece == Piece.ROOK or (i==king_row+1 and type_piece == Piece.KING):
                    print("lines not safe 1")
                    return False
    for i in range(king_row-1, -1, -1):
        current_id = copy_piece_square_board[i][king_col]
        if current_id != -1:
            type_piece = get_type(bitboard[current_id])
            color_piece = get_color(bitboard[current_id])
            if color_piece == get_color(king_info) or type_piece == Piece.PAWN or type_piece == Piece.BISHOP or type_piece == Piece.KNIGHT:
                break
            else:
                if type_piece == Piece.QUEEN or type_piece == Piece.ROOK or (i==king_row-1 and type_piece == Piece.KING):
                    print("lines not safe 2")
                    return False
                     
    for j in range(king_col+1, 8):
        current_id = copy_piece_square_board[king_row][j]
        if current_id != -1:
            type_piece = get_type(bitboard[current_id])
            color_piece = get_color(bitboard[current_id])
            if color_piece == get_color(king_info) or type_piece == Piece.PAWN or type_piece == Piece.BISHOP or type_piece == Piece.KNIGHT:
                break
            else:
                if type_piece == Piece.QUEEN or type_piece == Piece.ROOK or (j==king_col+1 and type_piece == Piece.KING):
                    print("lines not safe 3")
                    return False
                     
    for j in range(king_col-1, -1, -1):
        current_id = copy_piece_square_board[king_row][j]
        if current_id != -1:
            type_piece = get_type(bitboard[current_id])
            color_piece = get_color(bitboard[current_id])
            if color_piece == get_color(king_info) or type_piece == Piece.PAWN or type_piece == Piece.BISHOP or type_piece == Piece.KNIGHT:
                break
            else:
                if type_piece == Piece.QUEEN or type_piece == Piece.ROOK or (j==king_col-1 and type_piece == Piece.KING):
                    print("lines not safe 4")
                    return False
                     
    #scan to see if the diagonals are safe
    L = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for (x, y) in L:
        for i in range(1, 8):
            row = king_row+x*i
            col = king_col+y*i
            if row >= 0 and row < 8 and col >= 0 and col < 8:
                current_id = copy_piece_square_board[row][col]
                if current_id != -1:
                    #check if no bishop or pawn or quenn or king targeting you
                    type_piece = get_type(bitboard[current_id])
                    color_piece = get_color(bitboard[current_id])
                    sign_color = -1 if get_color(king_info) == Color.WHITE else 1
                    if color_piece == get_color(king_info) or type_piece == Piece.ROOK or type_piece == Piece.KNIGHT \
                        or (type_piece == Piece.PAWN and not (row == king_row+sign_color and abs(king_col-col) == 1)):
                            break
                    else:
                        if type_piece == Piece.QUEEN or type_piece == Piece.BISHOP or \
                            (row == king_row+sign_color and abs(king_col-col) == 1 and type_piece == Piece.PAWN) or \
                                (i == 1 and type_piece == Piece.KING):
                                    print(f"diagonal not safe for ({x}, {y})")
                                    return False
    
    return True


def valid_rook_move(r1, c1, r2, c2, piece_square_board, bitboard, kings_id, color_turn):
    
    if not check_bounds(r2, c2):
        return False

    if r1 != r2 and c1 != c2:
        return False
    

    if r1 != r2:
        step = (r2-r1)//abs(r2-r1)
        for i in range(r1+step, r2, step):
            if piece_square_board[i][c1] != -1:
                return False
        color_current = get_color(bitboard[piece_square_board[r1][c1]])
        id_arriving_piece = piece_square_board[r2][c2]
        if id_arriving_piece != -1:
            info_arriving_piece = bitboard[id_arriving_piece]
            if color_current == get_color(info_arriving_piece):
                return False
            
        return valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, \
                                                           bitboard, kings_id[color_turn.value], MOVE.NORMAL)
        
    else:
        step = (c2-c1)//abs(c2-c1)
        for j in range(c1+step, c2, step):
            if piece_square_board[r1][j] != -1:
                return False
        color_current = get_color(bitboard[piece_square_board[r1][c1]])
        id_arriving_piece = piece_square_board[r2][c2]
        if id_arriving_piece != -1:
            info_arriving_piece = bitboard[id_arriving_piece]
            if color_current == get_color(info_arriving_piece):
                return False
            
        return valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.NORMAL)
    


def valid_bishop_move(r1, c1, r2, c2, piece_square_board, bitboard, kings_id, color_turn):
    if not check_bounds(r2, c2):
        return False

    if r1 == r2 or c1 == c2:
        return False
    
    col_diff = c2-c1
    row_diff = r2-r1

    if abs(col_diff) != abs(row_diff):
        return False
    
    row_sign = row_diff//abs(row_diff)
    col_sign = col_diff//abs(col_diff)

    for i in range(1, abs(col_diff)):
        if piece_square_board[r1 + i*row_sign][c1 + i*col_sign] != -1:
            return False
        
    color_current = get_color(bitboard[piece_square_board[r1][c1]])
    id_arriving_piece = piece_square_board[r2][c2]
    if id_arriving_piece != -1:
        info_arriving_piece = bitboard[id_arriving_piece]
        if color_current == get_color(info_arriving_piece):
            return False
            
    return valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.NORMAL)

def valid_knight_move(r1, c1, r2, c2, piece_square_board, bitboard, kings_id, color_turn):

    if not check_bounds(r2, c2):
        return False
    

    row_diff = r2-r1
    col_diff = c2-c1

    x = (row_diff, col_diff)
    L = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    color_current = get_color(bitboard[piece_square_board[r1][c1]])
    id_arriving_piece = piece_square_board[r2][c2]
    if id_arriving_piece != -1:
        info_arriving_piece = bitboard[id_arriving_piece]
        if color_current == get_color(info_arriving_piece):
            return False
        
    return (x in L) and valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.NORMAL)
        
    

def valid_queen_move(r1, c1, r2, c2, piece_square_board, bitboard, kings_id, color_turn):
    if not check_bounds(r2, c2):
        return False
    

    return valid_rook_move(r1, c1, r2, c2, piece_square_board, bitboard, kings_id, color_turn) \
        or valid_bishop_move(r1, c1, r2, c2, piece_square_board, bitboard, kings_id, color_turn)

def valid_pawn_move(r1, c1, r2, c2, piece_square_board, bitboard, last_move, kings_id, color_turn):
    if not check_bounds(r2, c2):
        return False
    
    current_color = get_color(bitboard[piece_square_board[r1][c1]])
    sign_color = 1
    if current_color == Color.WHITE:
        sign_color *= -1
    
    if c1 == c2 and r2-r1 == sign_color:
        if piece_square_board[r2][c2] == -1:
            return valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.NORMAL)
        return False
    elif c1 == c2 and r2-r1 == sign_color*2:
        if piece_square_board[r2][c2] == -1 and piece_square_board[r1+sign_color][c1] == -1 and not has_moved(bitboard[piece_square_board[r1][c1]]):
            return valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.NORMAL)
        return False
    elif abs(c2-c1)==1 and r2-r1==sign_color:
        #usual capture
        if piece_square_board[r2][c2] != -1 and get_color(bitboard[piece_square_board[r2][c2]]) != current_color:
            return valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.NORMAL)
        
        #en passant
        if piece_square_board[r2][c2] == -1:
            if get_type(last_move[0]) != Piece.PAWN:
                return False
            
            last_row = get_row(last_move[0])
            last_column = get_column(last_move[0])
            current_row = get_row(last_move[1])
            current_column = get_column(last_move[1])


            if c2 == current_column and current_row == r2-sign_color and abs(last_row-current_row) == 2 and last_column-current_column == 0 :

                return valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.EN_PASSANT)
        return False
    else:
        return False


def valid_king_move(r1, c1, r2, c2, piece_square_board, bitboard, kings_id, color_turn):
    if not check_bounds(r2, c2):
        return False
    
    L = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)]
    row_diff = r2-r1
    col_diff = c2-c1
    if (row_diff, col_diff) in L:
        return (piece_square_board[r2][c2] == -1 \
                or get_color(bitboard[piece_square_board[r1][c1]]) != get_color(bitboard[piece_square_board[r2][c2]])) \
                    and valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.NORMAL)
        

    kings_color = get_color(bitboard[piece_square_board[r1][c1]])
    if col_diff == 2 and row_diff == 0:
        if kings_color == Color.WHITE:
            if r1 != 7 or c1 != 4 or has_moved(bitboard[piece_square_board[r1][c1]]) or \
                  piece_square_board[7][7] == -1 or get_type(bitboard[piece_square_board[7][7]]) != Piece.ROOK or \
                    has_moved(bitboard[piece_square_board[7][7]]):
                        return False
            
            for i in range(5, 7):
                if piece_square_board[r1][i] != -1:
                    return False

            
        else:
            if r1 != 0 or c1 != 4 or has_moved(bitboard[piece_square_board[r1][c1]]) or \
                  piece_square_board[0][7] == -1 or get_type(bitboard[piece_square_board[0][7]]) != Piece.ROOK or \
                    has_moved(bitboard[piece_square_board[0][7]]):
                        return False
            
            for i in range(5, 7):
                if piece_square_board[r1][i] != -1:
                    return False
                
        return valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.CASTLE)
    
    elif col_diff == -2 and row_diff == 0:
        if kings_color == Color.WHITE:
            if r1 != 7 or c1 != 4 or has_moved(bitboard[piece_square_board[r1][c1]]) or \
                  piece_square_board[7][0] == -1 or get_type(bitboard[piece_square_board[7][0]]) != Piece.ROOK or \
                    has_moved(bitboard[piece_square_board[7][0]]):
                        return False
            
            for i in range(3, 0, -1):
                if piece_square_board[r1][i] != -1:
                    return False
                
            
        else:
            if r1 != 0 or c1 != 4 or has_moved(bitboard[piece_square_board[r1][c1]]) or \
                  piece_square_board[0][0] == -1 or get_type(bitboard[piece_square_board[0][0]]) != Piece.ROOK or \
                    has_moved(bitboard[piece_square_board[0][0]]):
                        return False
            
            for i in range(3, 0, -1):
                if piece_square_board[r1][i] != -1:
                    return False

        return valid_after_scan_for_king_checks_after_move(r1, c1, r2, c2, piece_square_board, bitboard, \
                                                           kings_id[color_turn.value], MOVE.CASTLE)

    else:
        return False
    



def move_generation_rook(id, r, c, piece_square_board, bitboard, kings_id, color_turn):
    possible_rook_moves = []
    for i in range(r+1, 8):
        if valid_rook_move(r, c, i, c, piece_square_board, bitboard, kings_id, color_turn):
            possible_rook_moves.append((id, i, c, MOVE.NORMAL, None))
        else:
            break

    for i in range(r-1, -1, -1):
        if valid_rook_move(r, c, i, c, piece_square_board, bitboard, kings_id, color_turn):
            possible_rook_moves.append((id, i, c, MOVE.NORMAL, None))
        else:
            break
    
    for j in range(c+1, 8):
        if valid_rook_move(r, c, r, j, piece_square_board, bitboard, kings_id, color_turn):
            possible_rook_moves.append((id, r, j, MOVE.NORMAL, None))
        else:
            break
    
    for j in range(c-1, -1, -1):
        if valid_rook_move(r, c, r, j, piece_square_board, bitboard, kings_id, color_turn):
            possible_rook_moves.append((id, r, j, MOVE.NORMAL, None))
        else:
            break

    return possible_rook_moves

def move_generation_bishop(id, r, c, piece_square_board, bitboard, kings_id, color_turn):
    possible_bishop_move = []

    for i in range(1, 8):
        if valid_bishop_move(r, c, r+i, c+i, piece_square_board, bitboard, kings_id, color_turn):
            possible_bishop_move.append((id, r+i, c+i, MOVE.NORMAL, None))
        else:
            break

    for i in range(1, 8):
        if valid_bishop_move(r, c, r+i, c-i, piece_square_board, bitboard, kings_id, color_turn):
            possible_bishop_move.append((id, r+i, c-i, MOVE.NORMAL, None))
        else:
            break

    for i in range(1, 8):
        if valid_bishop_move(r, c, r-i, c+i, piece_square_board, bitboard, kings_id, color_turn):
            possible_bishop_move.append((id, r-i, c+i, MOVE.NORMAL, None))
        else:
            break

    for i in range(1, 8):
        if valid_bishop_move(r, c, r-i, c-i, piece_square_board, bitboard, kings_id, color_turn):
            possible_bishop_move.append((id, r-i, c-i, MOVE.NORMAL, None))
        else:
            break

    return possible_bishop_move

def move_generation_queen(id, r, c, piece_square_board, bitboard, kings_id, color_turn):
    possible_queen_move = []

    return possible_queen_move + move_generation_bishop(id, r, c, piece_square_board, bitboard, kings_id, color_turn) + \
        move_generation_rook(id, r, c, piece_square_board, bitboard, kings_id, color_turn)

def move_generation_knight(id, r, c, piece_square_board, bitboard, kings_id, color_turn):
    possible_knight_move = []

    L = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for (x, y) in L:
        if valid_knight_move(r, c, r+x, c+y, piece_square_board, bitboard, kings_id, color_turn):
            possible_knight_move.append((id, r+x, c+y, MOVE.NORMAL, None))
    
    return possible_knight_move

def move_generation_king(id, r, c, piece_square_board, bitboard, kings_id, color_turn):
    possible_king_move = []

    L = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for (x, y) in L:
        if valid_king_move(r, c, r+x, c+y, piece_square_board, bitboard, kings_id, color_turn):
            possible_king_move.append((id, r+x, c+y, MOVE.NORMAL, None))

    L = [(0, -2), (0, 2)]
    for (x, y) in L:
        if valid_king_move(r, c, r+x, c+y, piece_square_board, bitboard, kings_id, color_turn):
            possible_king_move.append((id, r+x, c+y, MOVE.CASTLE, None))
    
    return possible_king_move

def move_generation_pawn(id, r, c, piece_square_board, bitboard, kings_id, color_turn, last_move):
    possible_pawn_move = []
    #sign_color = -1 if color_turn == Color.WHITE else 1

    if color_turn == Color.WHITE:
        if valid_pawn_move(r, c, r-2, c, piece_square_board, bitboard, last_move, kings_id, color_turn):
            possible_pawn_move.append((id, r-2, c, MOVE.NORMAL, None))
        
        if valid_pawn_move(r, c, r-1, c, piece_square_board, bitboard, last_move, kings_id, color_turn):
            if r-1 != 0:
                possible_pawn_move.append((id, r-1, c, MOVE.NORMAL, None))
            else:
                possible_pawn_move.append((id, r-1, c, MOVE.PROMOTION, Piece.QUEEN))
                possible_pawn_move.append((id, r-1, c, MOVE.PROMOTION, Piece.ROOK))
                possible_pawn_move.append((id, r-1, c, MOVE.PROMOTION, Piece.KNIGHT))
                possible_pawn_move.append((id, r-1, c, MOVE.PROMOTION, Piece.BISHOP))

        if valid_pawn_move(r, c, r-1, c+1, piece_square_board, bitboard, last_move, kings_id, color_turn):
            if piece_square_board[r-1][c+1] != -1:
                if r-1 != 0:
                    possible_pawn_move.append((id, r-1, c+1, MOVE.NORMAL, None))
                else:
                    possible_pawn_move.append((id, r-1, c+1, MOVE.PROMOTION, Piece.QUEEN))
                    possible_pawn_move.append((id, r-1, c+1, MOVE.PROMOTION, Piece.ROOK))
                    possible_pawn_move.append((id, r-1, c+1, MOVE.PROMOTION, Piece.KNIGHT))
                    possible_pawn_move.append((id, r-1, c+1, MOVE.PROMOTION, Piece.BISHOP))
            else:
                possible_pawn_move.append((id, r-1, c+1, MOVE.EN_PASSANT, None))

        if valid_pawn_move(r, c, r-1, c-1, piece_square_board, bitboard, last_move, kings_id, color_turn):
            if piece_square_board[r-1][c-1] != -1:
                if r-1 != 0:
                    possible_pawn_move.append((id, r-1, c-1, MOVE.NORMAL, None))
                else:
                    possible_pawn_move.append((id, r-1, c-1, MOVE.PROMOTION, Piece.QUEEN))
                    possible_pawn_move.append((id, r-1, c-1, MOVE.PROMOTION, Piece.ROOK))
                    possible_pawn_move.append((id, r-1, c-1, MOVE.PROMOTION, Piece.KNIGHT))
                    possible_pawn_move.append((id, r-1, c-1, MOVE.PROMOTION, Piece.BISHOP))
            else:
                possible_pawn_move.append((id, r-1, c-1, MOVE.EN_PASSANT, None))
    
    else:
        if valid_pawn_move(r, c, r+2, c, piece_square_board, bitboard, last_move, kings_id, color_turn):
            possible_pawn_move.append((id, r+2, c, MOVE.NORMAL, None))
        
        if valid_pawn_move(r, c, r+1, c, piece_square_board, bitboard, last_move, kings_id, color_turn):
            if r+1 != 7:
                possible_pawn_move.append((id, r+1, c, MOVE.NORMAL, None))
            else:
                possible_pawn_move.append((id, r+1, c, MOVE.PROMOTION, Piece.QUEEN))
                possible_pawn_move.append((id, r+1, c, MOVE.PROMOTION, Piece.ROOK))
                possible_pawn_move.append((id, r+1, c, MOVE.PROMOTION, Piece.KNIGHT))
                possible_pawn_move.append((id, r+1, c, MOVE.PROMOTION, Piece.BISHOP))

        if valid_pawn_move(r, c, r+1, c+1, piece_square_board, bitboard, last_move, kings_id, color_turn):
            if piece_square_board[r+1][c+1] != -1:
                if r+1 != 7:
                    possible_pawn_move.append((id, r+1, c+1, MOVE.NORMAL, None))
                else:
                    possible_pawn_move.append((id, r+1, c+1, MOVE.PROMOTION, Piece.QUEEN))
                    possible_pawn_move.append((id, r+1, c+1, MOVE.PROMOTION, Piece.ROOK))
                    possible_pawn_move.append((id, r+1, c+1, MOVE.PROMOTION, Piece.KNIGHT))
                    possible_pawn_move.append((id, r+1, c+1, MOVE.PROMOTION, Piece.BISHOP))
            else:
                possible_pawn_move.append((id, r+1, c+1, MOVE.EN_PASSANT, None))

        if valid_pawn_move(r, c, r+1, c-1, piece_square_board, bitboard, last_move, kings_id, color_turn):
            if piece_square_board[r+1][c-1] != -1:
                if r+1 != 7:
                    possible_pawn_move.append((id, r+1, c-1, MOVE.NORMAL, None))
                else:
                    possible_pawn_move.append((id, r+1, c-1, MOVE.PROMOTION, Piece.QUEEN))
                    possible_pawn_move.append((id, r+1, c-1, MOVE.PROMOTION, Piece.ROOK))
                    possible_pawn_move.append((id, r+1, c-1, MOVE.PROMOTION, Piece.KNIGHT))
                    possible_pawn_move.append((id, r+1, c-1, MOVE.PROMOTION, Piece.BISHOP))
            else:
                possible_pawn_move.append((id, r+1, c-1, MOVE.EN_PASSANT, None))

    return possible_pawn_move


def move_generation(pieces_list, piece_square_board, bitboard, last_move, kings_id, color_turn):
    all_possible_moves = []
    for piece in pieces_list:
        piece_type = get_type(bitboard[piece])
        piece_row = get_row(bitboard[piece])
        piece_col = get_column(bitboard[piece])
        match piece_type:
            case Piece.QUEEN: 
                # print(move_generation_queen(piece, piece_row, piece_col, \
                #                                                          piece_square_board, bitboard, kings_id, color_turn))
                all_possible_moves = all_possible_moves + move_generation_queen(piece, piece_row, piece_col, \
                                                                         piece_square_board, bitboard, kings_id, color_turn)
            case Piece.KNIGHT: 
                # print(move_generation_knight(piece, piece_row, piece_col, \
                #                                                          piece_square_board, bitboard, kings_id, color_turn))
                all_possible_moves = all_possible_moves + move_generation_knight(piece, piece_row, piece_col, \
                                                                         piece_square_board, bitboard, kings_id, color_turn)
            case Piece.BISHOP: 
                # print(move_generation_bishop(piece, piece_row, piece_col, \
                #                                                          piece_square_board, bitboard, kings_id, color_turn))
                all_possible_moves = all_possible_moves + move_generation_bishop(piece, piece_row, piece_col, \
                                                                         piece_square_board, bitboard, kings_id, color_turn)
            case Piece.ROOK: 
                # print(move_generation_rook(piece, piece_row, piece_col, \
                #                                                          piece_square_board, bitboard, kings_id, color_turn))
                all_possible_moves = all_possible_moves + move_generation_rook(piece, piece_row, piece_col, \
                                                                         piece_square_board, bitboard, kings_id, color_turn)
            case Piece.PAWN:
                # print(move_generation_pawn(piece, piece_row, piece_col, \
                #                                                          piece_square_board, bitboard, kings_id, color_turn, last_move)) 
                all_possible_moves = all_possible_moves + move_generation_pawn(piece, piece_row, piece_col, \
                                                                         piece_square_board, bitboard, kings_id, color_turn, last_move)
            case Piece.KING: 
                # print(move_generation_king(piece, piece_row, piece_col, \
                #                                                          piece_square_board, bitboard, kings_id, color_turn))
                all_possible_moves = all_possible_moves + move_generation_king(piece, piece_row, piece_col, \
                                                                         piece_square_board, bitboard, kings_id, color_turn)
    
    return all_possible_moves