import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(" ", end=" ")
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

def valid_column(col, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(col) != 1:
        return False
    if col not in letters[:COLS]:
        return False
    col_index = letters.index(col)
    if board[0][col_index] != " ":
        return False
    return True

def place_checker(board, col_index, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return -1, -1

def check_win(board, r, c, checker):
    # horizontal
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # diagonal /
    count = 0
    start_row = r
    start_col = c
    while start_row > 0 and start_col < COLS-1:
        start_row -= 1
        start_col += 1
    row = start_row
    col = start_col
    while row < ROWS and col >= 0:
        if board[row][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        row += 1
        col -= 1
    # diagonal \
    count = 0
    start_row = r
    start_col = c
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    row = start_row
    col = start_col
    while row < ROWS and col < COLS:
        if board[row][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        row += 1
        col += 1
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS -1)
    print_board(board)
    while True:
        checker = players[current]
        print("Player " + checker + ", please enter a column:")
        col = input().upper()
        if not valid_column(col, board):
            print("Invalid input or column full, enter again.")
            continue
        col_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(col)
        r, c = place_checker(board, col_index, checker)
        if r == -1:
            # full column - lose turn
            current = (current +1) % NUM_PLAYERS
            continue
        print_board(board)
        if check_win(board, r, c, checker):
            print("Player " + checker + " won!")
            break
        if check_draw(board):
            print("The game is a draw.")
            break
        current = (current +1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
