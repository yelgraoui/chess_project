wp1 = (1 << 14)
wp2 = (1 << 15) | (1 << 13)
wp3 = (1 << 14) | (1 << 12)
wp4 = (1 << 13) | (1 << 11)
wp5 = (1 << 12) | (1 << 10)
wp6 = (1 << 11) | (1 << 9)
wp7 = (1 << 10) | (1 << 8)
wp8 = (1 << 9) 

white_pawn_attack = [
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [wp1 << 48, wp2 << 48, wp3 << 48, wp4 << 48, wp5 << 48, wp6 << 48, wp7 << 48, wp8 << 48],
    [wp1 << 40, wp2 << 40, wp3 << 40, wp4 << 40, wp5 << 40, wp6 << 40, wp7 << 40, wp8 << 40], 
    [wp1 << 32, wp2 << 32, wp3 << 32, wp4 << 32, wp5 << 32, wp6 << 32, wp7 << 32, wp8 << 32],
    [wp1 << 24, wp2 << 24, wp3 << 24, wp4 << 24, wp5 << 24, wp6 << 24, wp7 << 24, wp8 << 24],
    [wp1 << 16, wp2 << 16, wp3 << 16, wp4 << 16, wp5 << 16, wp6 << 16, wp7 << 16, wp8 << 16],
    [wp1 << 8, wp2 << 8, wp3 << 8, wp4 << 8, wp5 << 8, wp6 << 8, wp7 << 8, wp8 << 8],
    [wp1, wp2, wp3, wp4, wp5, wp6, wp7, wp8]
]

bp1 = (1 << (6 + 8*6))
bp2 = (1 << (7 + 8*6)) | (1 << (5 + 8*6))
bp3 = (1 << (6 + 8*6)) | (1 << (4 + 8*6))
bp4 = (1 << (5 + 8*6)) | (1 << (3 + 8*6))
bp5 = (1 << (4 + 8*6)) | (1 << (2 + 8*6))
bp6 = (1 << (3 + 8*6)) | (1 << (1 + 8*6))
bp7 = (1 << (2 + 8*6)) | (1 << (0 + 8*6))
bp8 = (1 << (1 + 8*6))

black_pawn_attack = [
    [bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8],
    [bp1 >> 8, bp2 >> 8, bp3 >> 8, bp4 >> 8, bp5 >> 8, bp6 >> 8, bp7 >> 8, bp8 >> 8],
    [bp1 >> 16, bp2 >> 16, bp3 >> 16, bp4 >> 16, bp5 >> 16, bp6 >> 16, bp7 >> 16, bp8 >> 16],
    [bp1 >> 24, bp2 >> 24, bp3 >> 24, bp4 >> 24, bp5 >> 24, bp6 >> 24, bp7 >> 24, bp8 >> 24],
    [bp1 >> 32, bp2 >> 32, bp3 >> 32, bp4 >> 32, bp5 >> 32, bp6 >> 32, bp7 >> 32, bp8 >> 32],
    [bp1 >> 40, bp2 >> 40, bp3 >> 40, bp4 >> 40, bp5 >> 40, bp6 >> 40, bp7 >> 40, bp8 >> 40],
    [bp1 >> 48, bp2 >> 48, bp3 >> 48, bp4 >> 48, bp5 >> 48, bp6 >> 48, bp7 >> 48, bp8 >> 48],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

N_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
ROW_MASK = 0b11111111
def attack_of_knight(i, j):
    b = [0, 0, 0, 0, 0, 0, 0, 0]
    for r in range(8):
        for c in range(8):
            if ((r-i), (c-j)) in N_moves:
                b[r] |= (1 << (7-c))

    res = 0
    for k in range(8):
        res <<= 8
        res |= b[k]

    return res

def attack_of_rook(i, j):
    b = [0, 0, 0, 0, 0, 0, 0, 0]
    for r in range(8):
        for c in range(8):
            if (r != i or c != j) and (r == i or c == j):
                b[r] |= (1 << (7-c))

    res = 0
    for k in range(8):
        res <<= 8
        res |= b[k]

    return res

def attack_of_bishop(i, j):
    b = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for r in range(8):
        for c in range(8):
            if (r != i and c != j) and (abs(r-i) == abs(c-j)):
                b[r] |= (1 << (7-c))

    res = 0
    for k in range(8):
        res <<= 8
        res |= b[k]

    return res

def attack_of_queen(i, j):
    return attack_of_bishop(i, j) | attack_of_rook(i, j)  


def check_bounds(r, c):
    return r >= 0 and r < 8 and c >= 0 and c < 8


def attack_of_king(i, j):
    L = [(1, 1), (1, -1), (-1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
    b = [0, 0, 0, 0, 0, 0, 0, 0]
    for (r, c) in L:
        if check_bounds(i+r, j+c):
            b[i+r] |= (1 << (7-(c+j)))

    res = 0
    for k in range(8):
        res <<= 8
        res |= b[k]

    return res
    

knight_attack = [[attack_of_knight(i, j) for j in range(8)] for i in range(8)]
rook_attack = [[attack_of_rook(i, j) for j in range(8)] for i in range(8)]
bishop_attack = [[attack_of_bishop(i, j) for j in range(8)] for i in range(8)]
queen_attack = [[attack_of_queen(i, j) for j in range(8)] for i in range(8)]
king_attack = [[attack_of_king(i, j) for j in range(8)] for i in range(8)]




def print_bb(bb):
    for i in range(7, -1, -1):
        tmp = (bb >> (i*8)) & ROW_MASK
        L = []
        for j in range(7, -1, -1):
            L.append((tmp >> j) & 0b1)
        print(L)

# print_bb(attack_of_knight(0, 0))
# print()
# print_bb(attack_of_knight(0, 5))
# print()
# print_bb(attack_of_knight(4, 5))
# print()
# print_bb(attack_of_knight(7, 7))
# print()
# print_bb(attack_of_knight(0, 1))
# print()
# print_bb(attack_of_knight(0, 6))


# print_bb(knight_attack[0][6])
# print()
# print_bb(knight_attack[0][1])
# print()
# print_bb(knight_attack[4][4])
# print()
# print_bb(knight_attack[7][1])
# print()

# print_bb(attack_of_queen(4, 4))
# print()
# print_bb(attack_of_queen(0, 3))
# print()
# print_bb(attack_of_queen(7, 4))
# print()


# print_bb(attack_of_king(4, 4))
# print()
# print_bb(attack_of_king(0, 3))
# print()
# print_bb(attack_of_king(7, 4))
# print()
# print_bb(attack_of_king(7, 7))
# print()

# print_bb(black_pawn_attack[0][6])
# print()
# print_bb(black_pawn_attack[0][0])
# print()
# print_bb(black_pawn_attack[4][4])
# print()
# print_bb(black_pawn_attack[7][1])
# print()
