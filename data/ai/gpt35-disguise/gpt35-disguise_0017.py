import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN = 4

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    clear()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(col):
    if len(col) != 1:
        return False
    col = col.upper()
    if col < 'A' or col >= chr(ord('A') + COLS):
        return False
    return True

def column_index(col):
    return ord(col.upper()) - ord('A')

def place_checker(board, col_index, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN +1):
            if all(board[r][c+i] == checker for i in range(WIN)):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - WIN +1):
            if all(board[r+i][c] == checker for i in range(WIN)):
                return True
    # diagonal /
    for r in range(WIN-1, ROWS):
        for c in range(COLS - WIN +1):
            if all(board[r-i][c+i] == checker for i in range(WIN)):
                return True
    # diagonal \
    for r in range(ROWS - WIN +1):
        for c in range(COLS - WIN +1):
            if all(board[r+i][c+i] == checker for i in range(WIN)):
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players_checkers[current_player]
        print(f"Player {checker}, please enter a column:")
        move = input().strip()
        if not is_valid_column(move):
            continue
        col = column_index(move)
        placed = place_checker(board, col, checker)
        if not placed:
            # column full, lose turn
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
