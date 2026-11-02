import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+---" * COLS + "+")
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print("+---" * COLS + "+")

def input_column(player):
    while True:
        col = input(f"Player {player}, please enter a column: ")
        if len(col) != 1:
            continue
        col = col.upper()
        if col < 'A' or col >= chr(ord('A') + COLS):
            continue
        return ord(col) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1  # Column full

def check_win(board, row, col, checker):
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # Check diagonal /
    count = 0
    start_row = row
    start_col = col
    while start_row > 0 and start_col < COLS - 1:
        start_row -= 1
        start_col += 1
    r = start_row
    c = start_col
    count = 0
    while r < ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    # Check diagonal \
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -=1
        start_col -=1
    r = start_row
    c = start_col
    count = 0
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count = 0
        r +=1
        c +=1
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
        col = input_column(checker)
        r = place_checker(board, col, checker)
        if r == -1:
            # Column full, lose turn
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, r, col, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

main()
