import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to create an empty board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear terminal screen
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Function to drop a checker in the board
def drop_checker(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

# Function to check for a win
def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (/)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    # Initialize variables
    board = create_board()
    num_players = 2  # Set to 2 players
    players = CHECKERS[:num_players]
    current_player = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        checker = players[current_player]
        column_input = input(f"Player {checker}, please enter a column: ").upper()
        
        # Validate input
        if column_input not in [chr(i) for i in range(65, 65 + COLS)]:
            print("Invalid input. Please enter a letter corresponding to a column (A to G).")
            continue

        column = ord(column_input) - 65  # Convert letter to index

        # Attempt to drop the checker
        if drop_checker(board, column, checker):
            print_board(board)

            # Check for a win
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break

            # Check for a draw
            if check_draw(board):
                print("The game is a draw!")
                break

            # Move to the next player
            current_player = (current_player + 1) % num_players
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    main()
