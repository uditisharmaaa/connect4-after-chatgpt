import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = "  "
    for i in range(COLS):
        header += " " + letters[i] + "  "
    print(header)
    print("+" + "---+" * COLS)
    for row in board:
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
        print("+" + "---+" * COLS)

def get_player_move(player):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        move = input("Player {}, please enter a column: ".format(player))
        if len(move) != 1:
            continue
        move = move.upper()
        if move not in letters[:COLS]:
            continue
        col = letters.index(move)
        return col

def place_checker(board, col, checker):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1  # column full

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical check
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal down-left check
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if board[r][c] == checker and board[r+1][c-1] == checker and board[r+2][c-2] == checker and board[r+3][c-3] == checker:
                return True
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

board = create_board()
players = CHECKERS[:PLAYERS]
current = random.randint(0, PLAYERS -1)

print_board(board)

while True:
    player_checker = players[current]
    col = get_player_move(player_checker)
    row, col = place_checker(board, col, player_checker)
    if row == -1:
        # full column, lose turn
        current = (current + 1) % PLAYERS
        continue
    print_board(board)
    if check_win(board, player_checker):
        print("Player {} won!".format(player_checker))
        break
    if is_draw(board):
        print("Draw!")
        break
    current = (current + 1) % PLAYERS
