import os
import random

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
COLUMN_LABELS = ["A", "B", "C", "D", "E", "F", "G"]
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Symbols for 2 to 5 players

# Configure the number of players
NUM_PLAYERS = 2  # Change this between 2 and 5

# Ensure a valid number of players is set
if NUM_PLAYERS < 2 or NUM_PLAYERS > len(PLAYER_SYMBOLS):
    raise ValueError("Number of players must be between 2 and 5.")

# Initialize the game board
def create_board():
    return [[" " for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

# Clear the console screen
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

# Print the game board
def print_board(board):
    clear_screen()
    print(" " + " ".join(COLUMN_LABELS))  # Print column labels
    for row in board:
        print("|" + "|".join(row) + "|")
    print("=" * (2 * NUM_COLUMNS + 1))  # Print a separator line

# Check if a column is full
def is_column_full(board, col):
    return board[0][col] != " "

# Get the next available row in a column
def get_next_row(board, col):
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == " ":
            return row
    return None

# Check for a win
def check_win(board, symbol):
    # Check horizontal, vertical, and diagonal directions
    for r in range(NUM_ROWS):
        for c in range(NUM_COLUMNS):
            if (
                c + 3 < NUM_COLUMNS and all(board[r][c + i] == symbol for i in range(4)) or
                r + 3 < NUM_ROWS and all(board[r + i][c] == symbol for i in range(4)) or
                r + 3 < NUM_ROWS and c + 3 < NUM_COLUMNS and all(board[r + i][c + i] == symbol for i in range(4)) or
                r + 3 < NUM_ROWS and c - 3 >= 0 and all(board[r + i][c - i] == symbol for i in range(4))
            ):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(is_column_full(board, col) for col in range(NUM_COLUMNS))

# Validate the player's input
def validate_input(choice):
    if choice.upper() in COLUMN_LABELS:
        return COLUMN_LABELS.index(choice.upper())
    return None

# Main game loop
def play_game():
    # Initialize the board and choose the first player randomly
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_player = players[current_player_idx]
        print(f"Player {current_player}'s turn!")

        # Get and validate the player's input
        col = None
        while col is None:
            choice = input(f"Choose a column ({'/'.join(COLUMN_LABELS)}): ").strip()
            col = validate_input(choice)
            if col is None or is_column_full(board, col):
                print("Invalid choice. Try again.")
                col = None

        # Place the player's piece in the selected column
        row = get_next_row(board, col)
        board[row][col] = current_player

        # Check for a win or draw
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Move to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
