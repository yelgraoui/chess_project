from tkinter import *
from tkinter import ttk
from PIL import Image
from pieces_classes import *
from utility import *
from moves import *

root = Tk()
root.title("Chess board")
root.minsize(1096, 1096)
root.resizable(False, False)

mainframe = ttk.Frame(root, padding=(8, 8))
canvas = Canvas(mainframe, background='green')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)

mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.grid(column=0, row=0, sticky=(N, W, E, S))


col = 0

board = []
last_move = [0, 0]
turn = Color.WHITE

for j in range(0, 1081-135, 135):
    board.append([])
    for i in range(0, 1081-135, 135):
        #print(j)
        id = 0
        if col == 0:
            id = canvas.create_rectangle(i, j, i+135, j+135, fill="antique white")
            board[j//135].append(id)
        else:
            id = canvas.create_rectangle(i, j, i+135, j+135, fill="saddle brown")
            board[j//135].append(id)
        col ^= 1
        
    col ^= 1


king_b = PhotoImage(file="pieces_images/black_king.svg")
king_b = king_b.zoom(3, 3)
queen_b = PhotoImage(file="pieces_images/black_queen.svg")
queen_b = queen_b.zoom(3, 3)
knight_b = PhotoImage(file="pieces_images/black_knight.svg")
knight_b = knight_b.zoom(3, 3)
pawn_b = PhotoImage(file="pieces_images/black_pawn.svg")
pawn_b = pawn_b.zoom(3, 3)
bishop_b = PhotoImage(file="pieces_images/black_bishop.svg")
bishop_b = bishop_b.zoom(3, 3)
rook_b = PhotoImage(file="pieces_images/black_rook.svg")
rook_b = rook_b.zoom(3, 3)

king_w = PhotoImage(file="pieces_images/white_king.svg")
king_w = king_w.zoom(3, 3)
queen_w = PhotoImage(file="pieces_images/white_queen.svg")
queen_w = queen_w.zoom(3, 3)
knight_w = PhotoImage(file="pieces_images/white_knight.svg")
knight_w = knight_w.zoom(3, 3)
pawn_w = PhotoImage(file="pieces_images/white_pawn.svg")
pawn_w = pawn_w.zoom(3, 3)
bishop_w = PhotoImage(file="pieces_images/white_bishop.svg")
bishop_w = bishop_w.zoom(3, 3)
rook_w = PhotoImage(file="pieces_images/white_rook.svg")
rook_w = rook_w.zoom(3, 3)


square_centric_board = []
for i in range(8):
    square_centric_board.append([])
    for j in range(8):
        square_centric_board[i].append(-1)

bitboard_dict = dict()

white_pieces = []
black_pieces = []

def place_piece(row, column, img, color:Color, type:Piece):
    id = canvas.create_image(135*column, 135*row, image=img, anchor='nw')
    square_centric_board[row][column] = id
    bitboard_dict[id] = (color.value << 11) | (row << 8) | (column << 5) | (type.value << 2)
    if color == Color.WHITE:
        white_pieces.append(id)
    else:
        black_pieces.append(id)

# # #place the pawns
for i in range(8):
    place_piece(1, i, pawn_b, Color.BLACK, Piece.PAWN)
    place_piece(6, i, pawn_w, Color.WHITE, Piece.PAWN)
    

#place the rooks
place_piece(0, 0, rook_b, Color.BLACK, Piece.ROOK)
place_piece(0, 7, rook_b, Color.BLACK, Piece.ROOK)
place_piece(7, 0, rook_w, Color.WHITE, Piece.ROOK)
place_piece(7, 7, rook_w, Color.WHITE, Piece.ROOK)

# #place the knights
place_piece(0, 1, knight_b, Color.BLACK, Piece.KNIGHT)
place_piece(0, 6, knight_b, Color.BLACK, Piece.KNIGHT)
place_piece(7, 1, knight_w, Color.WHITE, Piece.KNIGHT)
place_piece(7, 6, knight_w, Color.WHITE, Piece.KNIGHT)

# #place the bishops
place_piece(0, 2, bishop_b, Color.BLACK, Piece.BISHOP)
place_piece(0, 5, bishop_b, Color.BLACK, Piece.BISHOP)
place_piece(7, 2, bishop_w, Color.WHITE, Piece.BISHOP)
place_piece(7, 5, bishop_w, Color.WHITE, Piece.BISHOP)

# #place king and queen
place_piece(0, 3, queen_b, Color.BLACK, Piece.QUEEN)
place_piece(0, 4, king_b, Color.BLACK, Piece.KING)
place_piece(7, 3, queen_w, Color.WHITE, Piece.QUEEN)
place_piece(7, 4, king_w, Color.WHITE, Piece.KING)

kings_id = [square_centric_board[7][4], square_centric_board[0][4]]

print(white_pieces)
print(black_pieces)

first_press = True
freeze_game = False
r1, c1, r2, c2 = 0, 0, 0, 0

def promotion_mechanism(id_piece, promotion_frame, type, new_img):
    global freeze_game

    set_type(bitboard_dict, id_piece, type)
    canvas.itemconfigure(id, image=new_img)
    promotion_frame.grid_forget()
    freeze_game = False

def castling_mechanism(r1, c1, r2, c2, piece_square_board, bitboard, canvas):
    row_diff = r2-r1
    col_diff = c2-c1

    kings_color = get_color(bitboard[piece_square_board[r1][c1]])
    if col_diff == 2 and row_diff == 0:
        if kings_color == Color.WHITE:
            
            #do castling
            canvas.coords(piece_square_board[7][7], 135*5, 135*7)
            set_new_coord(bitboard, 7, 5, piece_square_board[7][7])
            piece_square_board[7][5] = piece_square_board[7][7]
            piece_square_board[7][7] = -1
            
        else:
            
            #do castling
            canvas.coords(piece_square_board[0][7], 135*5, 135*0)
            set_new_coord(bitboard, 0, 5, piece_square_board[0][7])
            piece_square_board[0][5] = piece_square_board[0][7]
            piece_square_board[0][7] = -1
    
    elif col_diff == -2 and row_diff == 0:
        if kings_color == Color.WHITE:
            
            #do castling
            canvas.coords(piece_square_board[7][0], 135*3, 135*7)
            set_new_coord(bitboard, 7, 3, piece_square_board[7][0])
            piece_square_board[7][3] = piece_square_board[7][0]
            piece_square_board[7][0] = -1
            
        else:
            
            #do castling
            canvas.coords(piece_square_board[0][0], 135*3, 135*0)
            set_new_coord(bitboard, 0, 3, piece_square_board[0][0])
            piece_square_board[0][3] = piece_square_board[0][0]
            piece_square_board[0][0] = -1

    else:
        return
    
def en_passant_mechanism(piece_square_board, last_move, canvas):

    current_row = get_row(last_move[1])
    current_column = get_column(last_move[1])

    id_to_remove = piece_square_board[current_row][current_column]
    color_to_remove = get_color(bitboard_dict[id_to_remove])
    if color_to_remove == Color.BLACK:
        black_pieces.remove(id_to_remove)
    else:
        white_pieces.remove(id_to_remove)
    canvas.itemconfigure(piece_square_board[current_row][current_column], image="")
    piece_square_board[current_row][current_column] = -1
    

def button_pressed(event):
    global first_press
    global freeze_game
    global r1, c1, r2, c2
    global turn

    if freeze_game:
        return

    x, y = event.x, event.y
    r, c = convert_coord_squares(x, y)

    if first_press:
        if square_centric_board[r][c] == -1 or get_color(bitboard_dict[square_centric_board[r][c]]) != turn:
            return 

        r1 = r
        c1 = c
        
        canvas.itemconfigure(board[r][c], fill="tomato2")
        first_press = False

    else:
        r2 = r
        c2 = c
        if r2 == r1 and c1 == c2:
            first_press = True
            if (r1+c1)%2 == 0:
                canvas.itemconfigure(board[r1][c1], fill="antique white")
            else:
                canvas.itemconfigure(board[r1][c1], fill="saddle brown")
        else:
            id_piece = square_centric_board[r1][c1]
            piece_type = get_type(bitboard_dict[id_piece])
            is_valid = False
            match piece_type:
                case Piece.ROOK:
                    is_valid = valid_rook_move(r1, c1, r2, c2, square_centric_board, bitboard_dict, kings_id, turn)
                case Piece.BISHOP:
                    is_valid = valid_bishop_move(r1, c1, r2, c2, square_centric_board, bitboard_dict, kings_id, turn)
                case Piece.KNIGHT:
                    is_valid = valid_knight_move(r1, c1, r2, c2, square_centric_board, bitboard_dict, kings_id, turn)
                case Piece.QUEEN:
                    is_valid = valid_queen_move(r1, c1, r2, c2, square_centric_board, bitboard_dict, kings_id, turn)
                case Piece.PAWN:
                    is_valid = valid_pawn_move(r1, c1, r2, c2, square_centric_board, bitboard_dict, last_move, kings_id, turn)
                case Piece.KING:
                    is_valid = valid_king_move(r1, c1, r2, c2, square_centric_board, bitboard_dict, kings_id, turn)
            
            if is_valid:
                id_arriving_square = square_centric_board[r2][c2]
                if id_arriving_square != -1:
                    color_to_remove = get_color(bitboard_dict[id_arriving_square])
                    if color_to_remove == Color.WHITE:
                        white_pieces.remove(id_arriving_square)
                    else:
                        black_pieces.remove(id_arriving_square)
                    canvas.itemconfigure(id_arriving_square, image="")

                if (r1+c1)%2 == 0:
                    canvas.itemconfigure(board[r1][c1], fill="antique white")
                else:
                    canvas.itemconfigure(board[r1][c1], fill="saddle brown")

                
                #managing promotion
                if piece_type == Piece.PAWN and ((get_color(bitboard_dict[id_piece]) == Color.WHITE and r2 == 0) \
                                                 or (get_color(bitboard_dict[id_piece]) == Color.BLACK and r2 == 7)):
                    freeze_game = True
                    promotion_frame = ttk.Frame(canvas)
                    promotion_frame.grid(column=0, row=0)
                    if get_color(bitboard_dict[id_piece]) == Color.WHITE:
                        button_knight = ttk.Button(promotion_frame, image=knight_w, \
                                                   command=(lambda : promotion_mechanism(id_piece, promotion_frame, Piece.KNIGHT, knight_w)))
                        button_bishop = ttk.Button(promotion_frame, image=bishop_w, \
                                                   command=(lambda : promotion_mechanism(id_piece, promotion_frame, Piece.BISHOP, bishop_w)))
                        button_rook = ttk.Button(promotion_frame, image=rook_w, \
                                                 command=(lambda : promotion_mechanism(id_piece, promotion_frame, Piece.ROOK, rook_w)))
                        button_queen = ttk.Button(promotion_frame, image=queen_w, \
                                                  command=(lambda : promotion_mechanism(id_piece, promotion_frame, Piece.QUEEN, queen_w)))
                        button_knight.grid(column=0, row=0)
                        button_bishop.grid(column=1, row=0)
                        button_rook.grid(column=2, row=0)
                        button_queen.grid(column=3, row=0)
                    else:
                        button_knight = ttk.Button(promotion_frame, image=knight_b, \
                                                   command=(lambda : promotion_mechanism(id_piece, promotion_frame, Piece.KNIGHT, knight_b)))
                        button_bishop = ttk.Button(promotion_frame, image=bishop_b, \
                                                   command=(lambda : promotion_mechanism(id_piece, promotion_frame, Piece.BISHOP, bishop_b)))
                        button_rook = ttk.Button(promotion_frame, image=rook_b, \
                                                 command=(lambda : promotion_mechanism(id_piece, promotion_frame, Piece.ROOK, rook_b)))
                        button_queen = ttk.Button(promotion_frame, image=queen_b, \
                                                  command=(lambda : promotion_mechanism(id_piece, promotion_frame, Piece.QUEEN, queen_b)))
                        button_knight.grid(column=0, row=0)
                        button_bishop.grid(column=1, row=0)
                        button_rook.grid(column=2, row=0)
                        button_queen.grid(column=3, row=0)

                #managing en passant
                if piece_type == Piece.PAWN and abs(r2-r1) == 1 and abs(c1-c2) == 1 and square_centric_board[r2][c2] == -1:
                    en_passant_mechanism(square_centric_board, last_move, canvas)

                #managing castling
                if piece_type == Piece.KING and abs(c2-c1) == 2:
                    castling_mechanism(r1, c1, r2, c2, square_centric_board, bitboard_dict, canvas)
                
                canvas.coords(id_piece, 135*c2, 135*r2)
                square_centric_board[r1][c1] = -1
                square_centric_board[r2][c2] = id_piece
                last_move[0] = bitboard_dict[id_piece]
                set_new_coord(bitboard_dict, r2, c2, id_piece)
                last_move[1] = bitboard_dict[id_piece]

                if turn == Color.WHITE:
                    black_king_id = kings_id[1]
                    black_king_row = get_row(bitboard_dict[black_king_id])
                    black_king_col = get_column(bitboard_dict[black_king_id])
                    if len(move_generation(black_pieces, square_centric_board, bitboard_dict, last_move, kings_id, Color.BLACK)) == 0:
                        freeze_game = True
                        end_frame = ttk.Frame(canvas)
                        end_frame.grid(column=0, row=0)
                        if valid_after_scan_for_king_checks_after_move(black_king_row, black_king_col, black_king_row, black_king_col, \
                                                                    square_centric_board, bitboard_dict, black_king_id, MOVE.NORMAL):
                            label = ttk.Label(end_frame, text="Draw")
                            label.grid(column=0, row=0)
                        else:
                            label = ttk.Label(end_frame, text="White wins")
                            label.grid(column=0, row=0)
                    print(move_generation(black_pieces, square_centric_board, bitboard_dict, last_move, kings_id, Color.BLACK))
                    turn = Color.BLACK
                else:
                    white_king_id = kings_id[0]
                    white_king_row = get_row(bitboard_dict[white_king_id])
                    white_king_col = get_column(bitboard_dict[white_king_id])
                    print(move_generation(white_pieces, square_centric_board, bitboard_dict, last_move, kings_id, Color.WHITE))
                    if len(move_generation(white_pieces, square_centric_board, bitboard_dict, last_move, kings_id, Color.WHITE)) == 0:
                        freeze_game = True
                        end_frame = ttk.Frame(canvas)
                        end_frame.grid(column=0, row=0)
                        if valid_after_scan_for_king_checks_after_move(white_king_row, white_king_col, white_king_row, white_king_col, \
                                                                    square_centric_board, bitboard_dict, white_king_id, MOVE.NORMAL):
                            label = ttk.Label(end_frame, text="Draw")
                            label.grid(column=0, row=0)
                        else:
                            label = ttk.Label(end_frame, text="Black wins")
                            label.grid(column=0, row=0)
                    turn = Color.WHITE
            else:
                if (r1+c1)%2 == 0:
                    canvas.itemconfigure(board[r1][c1], fill="antique white")
                else:
                    canvas.itemconfigure(board[r1][c1], fill="saddle brown")
            
            first_press = True
            

canvas.bind("<Button-1>", button_pressed)

root.mainloop()