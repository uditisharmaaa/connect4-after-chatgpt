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
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  ", end="")
    for i in range(COLS):
        print(letters[i], end="   ")
    print()
    print("+---"*COLS + "+")
    for r in range(ROWS):
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
        print("+---"*COLS + "+")

def get_column_input(player):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        col = input("Player " + player + ", please enter a column: ")
        if len(col) != 1:
            continue
        if not col.isalpha():
            continue
        col = col.upper()
        if col not in letters[:COLS]:
            continue
        return letters.index(col)

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical check
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right check
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right check
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
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
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current]
        col = get_column_input(checker)
        success = place_checker(board, col, checker)
        if not success:
            # lose turn
            current = (current + 1) % PLAYERS
        else:
            print_board(board)
            if check_win(board, checker):
                print("Player " + checker + " won!")
                break
            if board_full(board):
                print("Game is a draw!")
                break
            current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
