import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def get_random_player():
    return random.randint(0, len(PLAYER_SYMBOLS) - 1)

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column.upper() <= chr(65 + COLS - 1)

def drop_checker(board, column, player_symbol):
    col_index = ord(column.upper()) - 65
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = player_symbol
            return row, col_index
    return None

def check_win(board, row, col):
    symbol = board[row][col]
    return (check_direction(board, row, col, 1, 0) or  # Horizontal
            check_direction(board, row, col, 0, 1) or  # Vertical
            check_direction(board, row, col, 1, 1) or  # Diagonal \
            check_direction(board, row, col, 1, -1))   # Diagonal /

def check_direction(board, row, col, delta_row, delta_col):
    symbol = board[row][col]
    count = 1

    for direction in [1, -1]:
        r, c = row + direction * delta_row, col + direction * delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            if count == 4:
                return True
            r += direction * delta_row
            c += direction * delta_col

    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = initialize_board()
    current_player = get_random_player()
    
    print_board(board)

    while True:
        player_symbol = PLAYER_SYMBOLS[current_player]
        column = input(f"Player {player_symbol}, please enter a column (A-{chr(65 + COLS - 1)}): ")

        while not is_valid_input(column):
            column = input("Invalid input. Please enter a valid column: ")

        position = drop_checker(board, column, player_symbol)
        if position is None:
            print("Column is full. Try another column.")
            continue

        row, col = position
        print_board(board)

        if check_win(board, row, col):
            print(f"Player {player_symbol} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % len(PLAYER_SYMBOLS)

if __name__ == "__main__":
    main()
