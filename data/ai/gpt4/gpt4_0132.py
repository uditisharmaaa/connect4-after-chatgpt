import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

# Function to initialize the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Function to validate the player's input
def is_valid_input(column, board):
    if column.isalpha() and len(column) == 1:
        col_index = ord(column.upper()) - 65
        if 0 <= col_index < len(board[0]):
            if board[0][col_index] == " ":
                return True
    return False

# Function to place a checker on the board
def place_checker(column, player, board):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = player
            return

# Function to check for a win
def check_win(board, player):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check diagonal (down-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(len(board[0])))

# Main function to run the game
def connect_4():
    global ROWS, COLUMNS
    board = create_board(ROWS, COLUMNS)

    # Set up players and randomly select the first player
    num_players = 2  # Change this to add more players (max 5)
    players = PLAYERS[:num_players]
    current_player = random.choice(players)

    print_board(board)
    print(f"Player {current_player} will start the game!")

    while True:
        # Prompt player for input
        print_board(board)
        column = input(f"Player {current_player}, please enter a column: ").strip()

        # Validate input
        if not is_valid_input(column, board):
            print("Invalid input. Try again.")
            continue

        # Place the checker
        place_checker(column, current_player, board)

        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % num_players]

# Run the game
if __name__ == "__main__":
    connect_4()
