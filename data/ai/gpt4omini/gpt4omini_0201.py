import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # You can modify this for more players if needed

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+---" + "+---" * (COLS - 1) + "+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row data
        print("+---" + "+---" * (COLS - 1) + "+")  # Row border

# Check if the position in the column is valid
def is_valid_column(board, col):
    return 0 <= col < COLS and board[0][col] == " "

# Find the lowest empty row in a column
def get_lowest_row(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            return row
    return -1  # This means the column is full

# Place a checker in the board
def place_checker(board, col, checker):
    row = get_lowest_row(board, col)
    if row != -1:  # If there's space
        board[row][col] = checker
        return True
    return False

# Check for a win in all directions
def check_win(board, checker):
    # Check horizontal, vertical, and both diagonals
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontal
                if c + 3 < COLS and all(board[r][c+i] == checker for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4)):
                    return True
                # Check diagonal (down-right)
                if r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == checker for i in range(4)):
                    return True
                # Check diagonal (down-left)
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r+i][c-i] == checker for i in range(4)):
                    return True
    return False

# Check for a draw
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)  # Randomly select the first player
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column (A-G): ")
        user_input = input().strip().upper()

        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input! Please enter a letter from A to G.")
            continue

        column = ord(user_input) - 65  # Convert A-G to 0-6

        if is_valid_column(board, column):
            place_checker(board, column, current_player)
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break

            if is_draw(board):
                print("The game is a draw!")
                break

            # Switch player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full or invalid! Please try again.")

if __name__ == "__main__":
    play_game()
