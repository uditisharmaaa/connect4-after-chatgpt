import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column, board):
    return column.isalpha() and column.upper() in map(chr, range(65, 65 + COLS)) and board[0][ord(column.upper()) - 65] == " "

def drop_checker(column, checker, board):
    col_index = ord(column.upper()) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_winner(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != " " and (
                check_direction(board, row, col, 0, 1) or  # Horizontal
                check_direction(board, row, col, 1, 0) or  # Vertical
                check_direction(board, row, col, 1, 1) or  # Diagonal /
                check_direction(board, row, col, 1, -1)   # Diagonal \
            ):
                return board[row][col]
    return None

def check_direction(board, row, col, d_row, d_col):
    start_val = board[row][col]
    for i in range(1, 4):
        r, c = row + i * d_row, col + i * d_col
        if r < 0 or r >= ROWS or c < 0 or c >= COLS or board[r][c] != start_val:
            return False
    return True

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip()

        if not is_valid_column(column, board):
            print("Invalid column. Try again.")
            continue

        drop_checker(column, CHECKERS[current_player], board)
        print_board(board)

        winner = check_winner(board)
        if winner:
            print(f"Player {winner} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    play_game()
