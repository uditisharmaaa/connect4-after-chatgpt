import os
import random

# Constants for board dimensions and player pieces
ROWS = 6
COLS = 7
PLAYER_PIECES = ['X', 'O', 'V', 'H', 'M']

# Function to create an empty game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the current state of the board
def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Print column headers A-G
    print("+" + "---+" * COLS)  # Print top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+" * COLS)  # Print row border

# Function to check if a column input is valid
def is_valid_input(col):
    if len(col) != 1 or not col.isalpha():
        return False
    col_index = ord(col.upper()) - 65  # Convert letter to index (A=0, B=1, ...)
    return 0 <= col_index < COLS

# Function to drop a checker into the specified column
def drop_checker(board, col, piece):
    col_index = ord(col.upper()) - 65  # Convert letter to index
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = piece
            return True
    return False

# Function to check for a win condition
def check_win(board, piece):
    # Check horizontal, vertical, and diagonal conditions for a win
    # Horizontal check
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == piece for i in range(4)):
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    # Diagonal check (top-left to bottom-right)
    for col in range(COLS - 3):
        for row in range(ROWS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True

    # Diagonal check (bottom-left to top-right)
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True

    return False

# Function to check for a draw condition
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board()
    players_count = 2  # Set number of players
    current_player = random.randint(0, players_count - 1)  # Randomly choose the first player

    while True:
        print_board(board)
        current_piece = PLAYER_PIECES[current_player]  # Get current player's piece
        col = input(f"Player {current_piece}, please enter a column: ").strip().upper()

        # Input validation
        while not is_valid_input(col) or not drop_checker(board, col, current_piece):
            print("Invalid input. Please try again.")
            col = input(f"Player {current_piece}, please enter a column: ").strip().upper()

        # Check for win
        if check_win(board, current_piece):
            print_board(board)
            print(f"Player {current_piece} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Alternate between players
        current_player = (current_player + 1) % players_count

# Start the game
if __name__ == "__main__":
    play_game()
