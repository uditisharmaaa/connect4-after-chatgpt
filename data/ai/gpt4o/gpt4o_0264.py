import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Extendable for up to 5 players
BOARD_WIDTH = 4  # Spaces between columns
WIN_CONDITION = 4

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(input_str):
    return len(input_str) == 1 and 'A' <= input_str <= chr(65 + COLS - 1)

def column_is_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col

def check_for_win(board, last_row, last_col):
    checker = board[last_row][last_col]

    # Horizontal
    count = 0
    for c in range(COLS):
        if board[last_row][c] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0

    # Vertical
    count = 0
    for r in range(ROWS):
        if board[r][last_col] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0

    # Positive diagonal
    count = 0
    start_row = last_row + min(last_col, ROWS - last_row - 1)
    start_col = last_col - min(last_col, ROWS - last_row - 1)
    while start_row >= 0 and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1

    # Negative diagonal
    count = 0
    start_row = last_row - min(last_col, last_row)
    start_col = last_col - min(last_col, last_row)
    while start_row < ROWS and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")

        col = None
        while col is None:
            input_str = input().upper()
            if is_valid_input(input_str):
                col = ord(input_str) - 65
                if column_is_full(board, col):
                    print("Column is full. Choose another column:")
                    col = None
            else:
                print("Invalid input. Enter a valid column letter:")

        last_row, last_col = place_checker(board, col, CHECKERS[current_player])

        if check_for_win(board, last_row, last_col):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
