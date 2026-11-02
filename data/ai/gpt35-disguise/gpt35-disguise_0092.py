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
    for r in range(ROWS):
        row = []
        for c in range(COLS):
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
        print("+" + "---+" * COLS)
        print("|", end="")
        for c in range(COLS):
            print(f" {board[r][c]} |", end="")
        print()
    print("+" + "---+" * COLS)

def valid_column(input_col):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(input_col) != 1:
        return False
    if input_col not in letters[:COLS]:
        return False
    return True

def place_checker(board, col, checker):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal down-left check
    for r in range(ROWS - 3):
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
    players = PLAYERS
    checkers_list = CHECKERS[:players]
    current_player = random.randint(0, players -1)
    print_board(board)
    while True:
        checker = checkers_list[current_player]
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {checker}, please enter a column: ")
            col_input = col_input.strip().upper()
            if not valid_column(col_input):
                # invalid input, ask again
                continue
            col_index = ord(col_input) - ord('A')
            if col_index < 0 or col_index >= COLS:
                continue
            if board[0][col_index] != " ":
                # column full, turn lost
                valid_input = True
                break
            if place_checker(board, col_index, checker):
                valid_input = True
            else:
                # no space to place checker
                valid_input = True  # lose turn

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("Game is a draw!")
            break

        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
