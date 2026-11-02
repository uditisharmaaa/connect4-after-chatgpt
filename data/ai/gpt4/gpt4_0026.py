import os
import random

# Constants
ROWS = 6  # Number of rows
COLS = 7  # Number of columns
NUM_PLAYERS = 2  # Change this for more players
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Symbols for players, max 5 players
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Column labels

# Function to create an empty board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clears the screen
    header = "  ".join(ALPHABET[:COLS])
    print(f"  {header}")
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Function to validate user input
def validate_input(column, board):
    if len(column) != 1 or column not in ALPHABET[:COLS]:
        return False
    col_idx = ALPHABET.index(column)
    if board[0][col_idx] != " ":
        return False  # Column is full
    return True

# Function to place a checker in the selected column
def place_checker(column, symbol, board):
    col_idx = ALPHABET.index(column)
    for row in range(ROWS - 1, -1, -1):  # Start checking from the bottom
        if board[row][col_idx] == " ":
            board[row][col_idx] = symbol
            return row, col_idx  # Return the position where checker was placed

# Function to check for a win
def check_win(board, row, col, symbol):
    # Check directions: horizontal, vertical, diagonal (both directions)

    # Horizontal
    count = 0
    for c in range(COLS):
        count = count + 1 if board[row][c] == symbol else 0
        if count >= 4:
            return True

    # Vertical
    count = 0
    for r in range(ROWS):
        count = count + 1 if board[r][col] == symbol else 0
        if count >= 4:
            return True

    # Diagonal (\)
    count = 0
    r, c = row, col
    while r > 0 and c > 0:  # Move to the top-left
        r, c = r - 1, c - 1
    while r < ROWS and c < COLS:  # Traverse diagonal
        count = count + 1 if board[r][c] == symbol else 0
        if count >= 4:
            return True
        r, c = r + 1, c + 1

    # Diagonal (/)
    count = 0
    r, c = row, col
    while r > 0 and c < COLS - 1:  # Move to the top-right
        r, c = r - 1, c + 1
    while r < ROWS and c >= 0:  # Traverse diagonal
        count = count + 1 if board[r][c] == symbol else 0
        if count >= 4:
            return True
        r, c = r + 1, c - 1

    return False

# Function to check for a draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main function to play the game
def play_game():
    # Initialization
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Randomly select the first player

    # Game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player]}'s turn")
        column = input("Please enter a column: ").strip().upper()

        # Validate input
        if not validate_input(column, board):
            print("Invalid input, please try again.")
            continue

        # Place the checker
        row, col = place_checker(column, players[current_player], board)

        # Check for a win
        if check_win(board, row, col, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

# Entry point
if __name__ == "__main__":
    play_game()
