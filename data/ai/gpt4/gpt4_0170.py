import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Function to create an empty board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    # Print column headers
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))  # A, B, C, ...
    print("+---" * COLS + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Function to get a valid column choice from the current player
def get_valid_column(player, board):
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column) != 1 or not ('A' <= column < chr(65 + COLS)):
            print("Invalid input. Please enter a valid column (e.g., A-G).")
            continue
        col_index = ord(column) - 65
        if board[0][col_index] != " ":
            print("That column is full. Choose another one.")
            continue
        return col_index

# Function to place a checker in the selected column
def place_checker(board, col, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return

# Function to check for a win
def check_win(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and all(board[row][col + i] == symbol for i in range(1, 4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == symbol and all(board[row + i][col] == symbol for i in range(1, 4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == symbol and all(board[row + i][col + i] == symbol for i in range(1, 4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and all(board[row - i][col + i] == symbol for i in range(1, 4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    # Game setup
    board = create_board()
    num_players = 2  # Set to 2 by default for the assignment
    players = PLAYER_SYMBOLS[:num_players]
    current_player = random.choice(players)  # Randomly select the first player

    print_board(board)

    while True:
        # Player turn
        print(f"It's {current_player}'s turn.")
        col = get_valid_column(current_player, board)
        place_checker(board, col, current_player)

        # Print updated board
        print_board(board)

        # Check for a win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_idx = players.index(current_player)
        current_player = players[(current_idx + 1) % num_players]

if __name__ == "__main__":
    main()
