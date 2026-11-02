import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Create the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    header = "  " + "   ".join(chr(65 + col) for col in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Validate input
def is_valid_input(choice, board):
    if len(choice) != 1 or not choice.isalpha():
        return False
    col = ord(choice.upper()) - 65
    return 0 <= col < len(board[0]) and board[0][col] == " "

# Find the lowest empty row in a column
def get_available_row(board, col):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return None

# Check for win
def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Check horizontally
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == checker and all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertically
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == checker and all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == checker and all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == checker and all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

# Main function
def connect_4():
    # Initialize the game
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column: ", end="")
        choice = input().strip()

        if not is_valid_input(choice, board):
            print("Invalid input! Please try again.")
            continue

        col = ord(choice.upper()) - 65
        row = get_available_row(board, col)
        if row is None:
            print("Column full! Please choose another column.")
            continue

        # Place the checker
        board[row][col] = current_player
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Alternate turns
        current_player_index = (current_player_index + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect_4()
