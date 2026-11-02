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
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  ", end="")
    for c in range(COLS):
        print(letters[c], end="   ")
    print()
    for r in range(ROWS):
        print("+" + "---+"*COLS)
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print("+" + "---+"*COLS)

def is_valid_column(col_letter):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(col_letter) != 1:
        return False
    if col_letter not in letters[:COLS]:
        return False
    return True

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1

def winning_move(board, checker):
    # check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # check positively sloped diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    # check negatively sloped diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

board = create_board()
players = CHECKERS[:PLAYERS]
current_player = random.randint(0, PLAYERS-1)

while True:
    clear_screen()
    print_board(board)
    print("Player " + players[current_player] + ", please enter a column:")
    col_input = input().upper()
    if not is_valid_column(col_input):
        continue
    col = ord(col_input) - ord('A')
    row = get_next_open_row(board, col)
    if row == -1:
        # column full, lose turn
        current_player = (current_player + 1) % PLAYERS
        continue
    board[row][col] = players[current_player]
    if winning_move(board, players[current_player]):
        clear_screen()
        print_board(board)
        print("Player", players[current_player], "won!")
        break
    if is_draw(board):
        clear_screen()
        print_board(board)
        print("The game is a draw.")
        break
    current_player = (current_player + 1) % PLAYERS
