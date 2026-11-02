import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def valid_column(col):
    return col.isalpha() and col.upper() >= 'A' and col.upper() < chr(ord('A') + COLS)

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_line(line, checker):
    count = 0
    for c in line:
        count = count + 1 if c == checker else 0
        if count >= 4:
            return True
    return False

def check_win(board, r, c, checker):
    # Horizontal
    if check_line(board[r], checker): 
        return True
    # Vertical
    if check_line([board[i][c] for i in range(ROWS)], checker): 
        return True
    # Diagonal /
    diag1 = []
    row, col = r, c
    while row > 0 and col < COLS - 1:
        row -= 1
        col += 1
    while row < ROWS and col >= 0:
        diag1.append(board[row][col])
        row += 1
        col -= 1
    if check_line(diag1, checker): 
        return True
    # Diagonal \
    diag2 = []
    row, col = r, c
    while row > 0 and col > 0:
        row -= 1
        col -= 1
    while row < ROWS and col < COLS:
        diag2.append(board[row][col])
        row += 1
        col += 1
    if check_line(diag2, checker): 
        return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[current]
        while True:
            col_input = input(f"Player {checker}, please enter a column: ").upper()
            if not valid_column(col_input):
                continue
            col = ord(col_input) - ord('A')
            if is_column_full(board, col):
                break  # lose turn
            row = place_checker(board, col, checker)
            break
        print_board(board)
        if not is_column_full(board, col):
            if check_win(board, row, col, checker):
                print(f"Player {checker} won!")
                return
        if board_full(board):
            print("The game is a draw!")
            return
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
