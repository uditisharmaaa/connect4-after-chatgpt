import os
import random

# Constants for the board dimensions and the number of players
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checker symbols for up to 5 players, indexed by player number
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates and returns an empty game board."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Prints the game board."""
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(NUM_COLS)))
    print("+---" * NUM_COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLS + "+")

def is_valid_input(input_str):
    """Checks whether the input is valid (a single letter) for column selection."""
    return len(input_str) == 1 and 'A' <= input_str <= chr(65 + NUM_COLS - 1)

def is_column_full(board, col_index):
    """Checks if a given column is already full."""
    return board[0][col_index] != " "

def drop_checker(board, col_index, checker):
    """Drops the checker into the specified column."""
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_for_win(board, checker):
    """Checks if the current player has won the game."""
    # Check horizontal win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right) win
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right) win
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(NUM_COLS))

def play_game():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        
        # Current player's turn
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().strip().upper()
        
        # Validate user input
        if not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column ID.")
            continue

        col_index = ord(user_input) - 65  # Convert from 'A' to column index
        
        # Check for a full column
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue

        # Place the checker
        drop_checker(board, col_index, CHECKERS[current_player])

        # Check for a win
        if check_for_win(board, CHECKERS[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for a draw
        if check_for_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
