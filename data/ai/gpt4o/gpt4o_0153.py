import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Extend this if more players are added
BOARD_COLUMNS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', ..., 'G']

# Initialize the board
def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(BOARD_COLUMNS))
    print("+---+" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" * COLUMNS + "+")

# Get a valid column input from player
def get_valid_column():
    while True:
        column = input("Please enter a column: ").upper()
        if column in BOARD_COLUMNS:
            return BOARD_COLUMNS.index(column)
        else:
            print(f"Invalid input. Please select from {BOARD_COLUMNS}")

# Place a checker on the board
def place_checker(board, column, checker):
    for row in reversed(board):  # Start placing from the bottom
        if row[column] == " ":
            row[column] = checker
            return True
    print("Column is full. You lose this turn.")
    return False

# Check for a win
def check_for_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

# Check for draw
def check_for_draw(board):
    for row in board:
        if " " in row:  # If there's any empty space, not draw yet
            return False
    return True

def main():
    # Initialize game settings
    board = initialize_board(ROWS, COLUMNS)
    players = [CHECKERS[i] for i in range(MAX_PLAYERS)]
    current_player_index = random.randint(0, MAX_PLAYERS - 1)

    print_board(board)  # Initial print of board

    # Game loop
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn.")
        col_index = get_valid_column()
        
        if place_checker(board, col_index, current_player):
            print_board(board)
            if check_for_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_for_draw(board):
                print("The game is a draw!")
                break

        # Switch player
        current_player_index = (current_player_index + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
