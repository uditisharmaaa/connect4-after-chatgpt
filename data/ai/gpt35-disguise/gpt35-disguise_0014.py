import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"] 

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" " for _ in range(COLS)]
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = "  "
    for i in range(COLS):
        header += " " + letters[i] + "  "
    print(header)
    sep = "+" + "---+"*COLS
    for r in range(ROWS):
        print(sep)
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print(sep)

def get_player_input(player, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        col = input(f"Player {player}, please enter a column: ")
        if len(col) != 1 or not col.isalpha() or not col.isupper():
            continue
        idx = letters.find(col)
        if idx == -1 or idx >= COLS:
            continue
        # check if column full
        if board[0][idx] != " ":
            # column full - player loses turn
            return -1
        return idx

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1  # should not get here if checked before

def check_win(board, r, c, checker):
    # horizontal
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    # diagonal (\)
    count = 0
    start_row = r
    start_col = c
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    row = start_row
    col = start_col
    count = 0
    while row < ROWS and col < COLS:
        if board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        row += 1
        col += 1
    # diagonal (/)
    start_row = r
    start_col = c
    while start_row < ROWS-1 and start_col > 0:
        start_row += 1
        start_col -= 1
    row = start_row
    col = start_col
    count = 0
    while row >= 0 and col < COLS:
        if board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        row -= 1
        col += 1
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[current]
        col = get_player_input(checker, board)
        if col == -1:
            # lost turn because column is full
            current = (current + 1) % PLAYERS
            continue
        r, c = place_checker(board, col, checker)
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current = (current + 1) % PLAYERS

main()
