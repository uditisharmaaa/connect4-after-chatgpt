import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2  # Change this as needed for 2-5 players
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYER_COUNT]

def initialize_board():
    """Create a 2D board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen before printing the board
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    print("+---" * COLUMNS + "+")

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_char):
    """Check if the input is a valid column."""
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    column_index = ord(input_char.upper()) - 65
    return 0 <= column_index < COLUMNS

def place_checker(board, column, player_symbol):
    """Place the player's checker in the correct column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player_symbol
            return True
    return False

def check_win(board, player_symbol):
    """Check for a win condition for player_symbol."""
    # Check horizontal, vertical, and diagonal lines for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            if check_line(board, row, col, player_symbol):
                return True
    return False

def check_line(board, row, col, player_symbol):
    """Check all lines starting from a specific position."""
    return (check_direction(board, row, col, player_symbol, 1, 0) or  # Horizontal
            check_direction(board, row, col, player_symbol, 0, 1) or  # Vertical
            check_direction(board, row, col, player_symbol, 1, 1) or  # Diagonal /
            check_direction(board, row, col, player_symbol, 1, -1))   # Diagonal \

def check_direction(board, row, col, player_symbol, delta_row, delta_col):
    """Check a specific direction for 4 in a row."""
    in_a_row = 0
    for i in range(4):
        r = row + delta_row * i
        c = col + delta_col * i
        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_symbol:
            in_a_row += 1
        else:
            break
    return in_a_row == 4

def is_draw(board):
    """Check if the board is full and the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, PLAYER_COUNT - 1)

    while True:
        print_board(board)
        player_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {player_symbol}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if is_valid_input(user_input):
                column_index = ord(user_input) - 65
                if place_checker(board, column_index, player_symbol):
                    break
                else:
                    print("Column is full. Choose another column:")
            else:
                print("Invalid input. Enter a valid column:")

        if check_win(board, player_symbol):
            print_board(board)
            print(f"Player {player_symbol} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYER_COUNT

play_game()
