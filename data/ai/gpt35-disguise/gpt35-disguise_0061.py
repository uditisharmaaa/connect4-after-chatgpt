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
    clear_screen()
    print(" ", end=" ")
    for c in range(COLS):
        print(letters[c], end="   ")
    print()
    for r in range(ROWS):
        print("+---"*COLS + "+")
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print("+---"*COLS + "+")

def valid_input(s):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(s) != 1:
        return False
    if s not in letters[:COLS]:
        return False
    return True

def get_column_from_letter(letter):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters.index(letter)

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_horizontal(board, checker):
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

def check_vertical(board, checker):
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

def check_diagonal(board, checker):
    # check /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    # check \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    return False

def check_win(board, checker):
    if check_horizontal(board, checker):
        return True
    if check_vertical(board, checker):
        return True
    if check_diagonal(board, checker):
        return True
    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[current]
        print(f"Player {checker}, please enter a column:")
        valid_move = False
        while not valid_move:
            move = input().upper()
            if not valid_input(move):
                print("Invalid input, please enter a valid column letter:")
                continue
            col = get_column_from_letter(move)
            if not place_checker(board, col, checker):
                # column full - lose turn
                valid_move = True
                # print_board(board)
                # no spot available, lose turn, just break input loop
            else:
                valid_move = True
                print_board(board)
                if check_win(board, checker):
                    print(f"Player {checker} won!")
                    return
                if check_draw(board):
                    print("Draw! The board is full.")
                    return
        current = (current + 1) % PLAYERS

main()
