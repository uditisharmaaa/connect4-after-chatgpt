import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Functions
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(ALPHABET[:COLS])
    print(header)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(input_value):
    return input_value in ALPHABET[:COLS]

def drop_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check rows
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + offset] == checker for offset in range(4)):
                return True

    # Check columns
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + offset][col] == checker for offset in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + offset][col + offset] == checker for offset in range(4)):
                return True

    # Check diagonals (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + offset][col - offset] == checker for offset in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main code
def main():
    # Initialize game variables
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player]} goes first!")

    while True:
        # Prompt player for input
        current_checker = PLAYER_CHECKERS[current_player]
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        # Validate input
        if not is_valid_input(user_input):
            print("Invalid input. Please choose a valid column.")
            continue

        col_index = ALPHABET.index(user_input)

        # Drop checker
        if not drop_checker(board, col_index, current_checker):
            print("Column is full. Please choose a different column.")
            continue

        # Print updated board
        print_board(board)

        # Check for winner
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
