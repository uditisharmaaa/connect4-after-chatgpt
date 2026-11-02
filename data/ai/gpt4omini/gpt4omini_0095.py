import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check if the input column is valid
def valid_column(column):
    return column.isalpha() and 'A' <= column <= chr(65 + COLS - 1)

# Get the numeric index of the column
def column_index(column):
    return ord(column) - 65

# Place the checker in the board
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Check horizontal win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
                
    # Check vertical win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal win (\ direction)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal win (/ direction)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game function
def connect_4():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    player_count = len(PLAYERS)

    while True:
        print_board(board)
        current_checker = PLAYERS[current_player_index]
        column = input(f"Player {current_checker}, please enter a column: ").upper()

        while not valid_column(column) or not place_checker(board, column_index(column), current_checker):
            print("Invalid input. Please try again.")
            column = input(f"Player {current_checker}, please enter a column: ").upper()

        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % player_count

if __name__ == "__main__":
    connect_4()
