import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(inp):
    return len(inp) == 1 and inp.isalpha() and 'A' <= inp <= chr(65 + COLS - 1)

def is_column_full(board, col):
    return board[0][col] != " "

def get_next_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1

def place_checker(board, col, checker):
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = checker
        return True
    return False

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Check diagonal \
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True
    # Check diagonal /
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()

        if is_valid_input(user_input):
            col = ord(user_input) - 65
            if not is_column_full(board, col):
                if place_checker(board, col, current_checker):
                    print_board(board)
                    if check_win(board, current_checker):
                        print(f"Player {current_checker} won!")
                        break
                    if check_draw(board):
                        print("The game is a draw!")
                        break
                    current_player_index = (current_player_index + 1) % PLAYERS
            else:
                print("Column is full, you lose a turn!")
        else:
            print("Invalid input, please enter a valid column letter.")

if __name__ == "__main__":
    main()
