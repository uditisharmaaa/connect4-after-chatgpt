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
    print(" ", end=" ")
    for c in range(COLS):
        print(letters[c], end="   ")
    print()
    for r in range(ROWS):
        print("+" + "---+"*COLS)
        print("|", end="")
        for c in range(COLS):
            print(" "+board[r][c]+" |", end="")
        print()
    print("+" + "---+"*COLS)

def valid_column(col):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(col) != 1:
        return False
    if col not in letters[:COLS]:
        return False
    return True

def column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r
    return -1  # Full column

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    while True:
        print_board(board)
        print("Player "+players[current]+", please enter a column:")
        inp = input().strip().upper()
        if not valid_column(inp):
            continue
        col = ord(inp) - ord("A")
        if column_full(board, col):
            # Lose turn
            current = (current + 1) % PLAYERS
            continue
        place_checker(board, col, players[current])
        if check_win(board, players[current]):
            print_board(board)
            print("Player "+players[current]+" won!")
            break
        if board_full(board):
            print_board(board)
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
