import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column):
    return column.isalpha() and len(column) == 1 and 0 <= ord(column.upper()) - 65 < COLUMNS

def get_valid_column(board, player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if not is_valid_column(column):
            print("Invalid column. Please enter a valid column letter.")
            continue
        col_index = ord(column) - 65
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        return col_index

def drop_checker(board, col_index, symbol):
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = symbol
            return row_index

def check_for_win(board, row, col, symbol):
    # Direction vectors: horizontal, vertical, diagonal (main), diagonal (anti)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        for i in (-1, 1):  # Check both directions
            x, y = row, col
            while True:
                x += i * dx
                y += i * dy
                if 0 <= x < ROWS and 0 <= y < COLUMNS and board[x][y] == symbol:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    # Initialize board and game
    board = create_board()

    # Randomly choose the number of players (default to 2 for submission requirements)
    num_players = 2
    player_symbols = PLAYER_SYMBOLS[:num_players]

    # Randomly select starting player
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    # Game loop
    while True:
        current_symbol = player_symbols[current_player_index]
        col_index = get_valid_column(board, current_symbol)
        row_index = drop_checker(board, col_index, current_symbol)

        print_board(board)

        # Check win condition
        if check_for_win(board, row_index, col_index, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check draw condition
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
