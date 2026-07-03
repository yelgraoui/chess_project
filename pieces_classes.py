from enum import Enum

class Color(Enum):
    WHITE = 0
    BLACK = 1

class Piece(Enum):
    PAWN = 0
    ROOK = 1
    BISHOP = 2
    KNIGHT = 3
    KING = 4
    QUEEN = 5

#print(Color(0), Color(1), Piece(4))
# print(int(True), int(False))
