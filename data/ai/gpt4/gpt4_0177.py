import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

# Create the game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Check for valid input
def validate_input(user_input, board):
    if user_input not in COLUMN_LABELS:
        return False
    column_index = COLUMN_LABELS.index(user_input)
    # Check if the column is full
    return any(row[column_index] == " " for row in board)

# Place the checker in the board
def place_checker(board, column, checker):
    column_index = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return

# Check for a win
def check_win(board, checker):
    # Check horizontal win
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if (board[row][col] == board[row + 1][col] == 
                board[row + 2][col] == board[row + 3][col] == checker):
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if (board[row][col] == board[row + 1][col + 1] == 
                board[row + 2][col + 2] == board[row + 3][col + 3] == checker):
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == board[row - 1][col + 1] == 
                board[row - 2][col + 2] == board[row - 3][col + 3] == checker):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_game():
    # Create the board and choose random first player
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Game loop
    while True:
        # Print the board
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")

        # Get and validate the input
        user_input = input().strip().upper()
        while not validate_input(user_input, board):
            print("Invalid input. Please enter a valid column:")
            user_input = input().strip().upper()

        # Place the checker on the board
        place_checker(board, user_input, CHECKERS[current_player])

        # Check for a win
        if check_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
