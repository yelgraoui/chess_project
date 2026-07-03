from pieces_classes import *

MASK_3BITS = 7

SHIFT_COLOR = 11
SHIFT_ROW = 8
SHIFT_COLUMN = 5
SHIFT_TYPE = 2
SHIFT_MOVED = 1


def convert_coord_squares(x, y):
    row = y//135
    column = x//135
    return row, column

def get_color(x):
    return Color(x >> SHIFT_COLOR)

def get_row(x):
    return MASK_3BITS & (x >> SHIFT_ROW)

def get_column(x):
    return MASK_3BITS & (x >> SHIFT_COLUMN)

def get_type(x):
    return Piece(MASK_3BITS & (x >> SHIFT_TYPE))

def has_moved(x):
    y = 1 & (x >> SHIFT_MOVED)
    if y == 1:
        return True
    else:
        return False
    
def is_checked(x):
    y = 1 & x
    if y == 1:
        return True
    else:
        return False
    

def set_new_coord(bitboard, new_row, new_column, id):
    to_mod = bitboard[id]
    color = get_color(to_mod).value
    type = get_type(to_mod).value
    #has_moved_ = int(has_moved(to_mod))
    is_checked_  = int(is_checked(to_mod))
    bitboard[id] = (color << SHIFT_COLOR) | (new_row << SHIFT_ROW) | (new_column << SHIFT_COLUMN) | (type << SHIFT_TYPE) | (1 << SHIFT_MOVED) | is_checked_


def set_type(bitboard, id, new_type):
    to_mod = bitboard[id]
    color = get_color(to_mod).value
    type = new_type.value
    row = get_row(to_mod)
    column = get_column(to_mod)
    #has_moved_ = int(has_moved(to_mod))
    is_checked_  = int(is_checked(to_mod))
    bitboard[id] = (color << SHIFT_COLOR) | (row << SHIFT_ROW) | (column << SHIFT_COLUMN) | (type << SHIFT_TYPE) | (1 << SHIFT_MOVED) | is_checked_