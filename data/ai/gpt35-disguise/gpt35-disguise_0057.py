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
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  ", end="")
    for c in range(COLS):
        print(" " + letters[c] + "  ", end="")
    print()
    for r in range(ROWS):
        print("+---"*COLS + "+")
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print("+---"*COLS + "+")

def valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

def make_move(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1  # Should not happen if move is valid

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS -3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical check
    for c in range(COLS):
        for r in range(ROWS -3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS -3):
        for c in range(COLS -3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS -3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def get_player_input(checker):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        col_input = input("Player " + checker + ", please enter a column: ")
        if len(col_input) != 1:
            continue
        if not col_input.isalpha():
            continue
        col_input = col_input.upper()
        if col_input not in letters[:COLS]:
            continue
        col = letters.index(col_input)
        return col

def main():
    board = create_board()
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = CHECKERS[current]
        col = get_player_input(checker)
        if not valid_move(board, col):
            # If column full, player loses turn
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        make_move(board, col, checker)
        print_board(board)
        if check_win(board, checker):
            print("Player " + checker + " won!")
            break
        if check_draw(board):
            print("Draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
