import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels"""
    print("  A B C D E F G")
    for row in board:
        print("+---" * BOARD_COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * BOARD_COLS)

def validate_input(player, column):
    """Validate user input"""
    if not column.isalpha():
        print("Invalid input. Please enter a letter.")
        return False
    column = ord(column.upper()) - 65
    if column < 0 or column >= BOARD_COLS:
        print("Invalid input. Please enter a letter between A and G.")
        return False
    return True

def place_checker(board, player, column):
    """Place a checker in the board"""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = CHECKERS[player]
            return True
    print("Column is full. Please choose another column.")
    return False

def check_win(board, player):
    """Check for a win in the board"""
    # Check horizontal
    for row in board:
        for i in range(BOARD_COLS - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == CHECKERS[player]:
                return True
    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == CHECKERS[player]:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == CHECKERS[player]:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == CHECKERS[player]:
                return True
    return False

def check_draw(board):
    """Check for a draw in the board"""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Create the board
    board = create_board()

    # Choose a random player to start
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        # Clear the screen and print the board
        os.system('clear')
        print_board(board)

        # Ask the current player for input
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ")

        # Validate the input
        if not validate_input(current_player, column):
            continue

        # Place the checker in the board
        column = ord(column.upper()) - 65
        if not place_checker(board, current_player, column):
            continue

        # Check for a win
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
