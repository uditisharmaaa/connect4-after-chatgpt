import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---"*COLS + "+")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+---"*COLS + "+")

def get_column_index(col):
    if len(col) != 1:
        return -1
    c = col[0]
    if c < "A" or c >= chr(ord("A") + COLS):
        return -1
    return ord(c) - ord("A")

def place_checker(board, col, checker):
    # place at lowest empty row of that column
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal down-left
    for r in range(ROWS-3):
        for c in range(3, COLS):
            if board[r][c] == checker and board[r+1][c-1] == checker and board[r+2][c-2] == checker and board[r+3][c-3] == checker:
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
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        print("Player {}, please enter a column:".format(checker))
        col_input = input().strip()
        col_idx = get_column_index(col_input)
        if col_idx == -1:
            # invalid input
            continue

        placed = place_checker(board, col_idx, checker)
        if not placed:
            # column full, turn lost
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, checker):
            print("Player {} won!".format(checker))
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
