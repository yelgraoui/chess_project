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
            if square_piece_board[i][j] != -1 and get_type(bitboard(square_piece_board[i][j])) == Piece.QUEEN:
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
                        score += w_pawn[correct_row_to_look][j] + P
                    case Piece.KNIGHT:
                        score += w_knight[correct_row_to_look][j] + N
                    case Piece.BISHOP:
                        score += w_bishop[correct_row_to_look][j] + B
                    case Piece.ROOK:
                        score += w_rook[correct_row_to_look][j] + R
                    case Piece.QUEEN:
                        score += w_queen[correct_row_to_look][j] + Q
                    case Piece.KING:
                        score += w_king[correct_row_to_look][j] + K

    return score

