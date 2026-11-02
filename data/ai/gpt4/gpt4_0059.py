import os
import random

# Global constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # A, B, C, ...

# Function to clear the screen
def clear_screen():
    os.system('clear')  # For Linux/Unix

# Function to create the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    # Print column labels
    print("  ", "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")

    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Function to validate user input
def validate_input(column, board):
    if column not in COLUMN_LABELS:
        return False
    col_index = COLUMN_LABELS.index(column)
    if board[0][col_index] != " ":  # Check if the column is full
        return False
    return True

# Function to place a checker in the column
def place_checker(board, column, checker):
    col_index = COLUMN_LABELS.index(column)
    for row in range(ROWS - 1, -1, -1):  # Place from the bottom up
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return

# Function to check for a win
def check_win(board, last_checker):
    # Horizontal, Vertical, Diagonal checks
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] != last_checker:
                continue

            # Check horizontal
            if col <= COLUMNS - 4 and all(board[row][col + i] == last_checker for i in range(4)):
                return True

            # Check vertical
            if row <= ROWS - 4 and all(board[row + i][col] == last_checker for i in range(4)):
                return True

            # Check diagonal (\)
            if row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row + i][col + i] == last_checker for i in range(4)):
                return True

            # Check diagonal (/)
            if row >= 3 and col <= COLUMNS - 4 and all(board[row - i][col + i] == last_checker for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game loop
def connect_4():
    # Initialize the board
    board = create_board()

    # Randomly pick the first player
    current_player = random.randint(0, PLAYERS - 1)

    # Main game logic
    while True:
        clear_screen()
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, it's your turn!")

        while True:
            column = input("Please enter a column: ").strip().upper()
            if validate_input(column, board):
                break
            print("Invalid input. Try again.")

        # Place the checker in the board
        place_checker(board, column, CHECKERS[current_player])

        # Check for a win
        if check_win(board, CHECKERS[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect_4()
