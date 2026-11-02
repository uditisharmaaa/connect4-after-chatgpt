import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Available checkers for players
PLAYER_COUNT = 2  # Number of players (can be adjusted, max 5)

# Function to clear the console
def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

# Function to create an empty board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    column_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(COLS))
    print(column_labels)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Function to place a checker on the board
def place_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False  # Column is full

# Function to check for a win condition
def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            # Check horizontal
            if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                return True
            # Check vertical
            if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                return True
            # Check diagonal (bottom-left to top-right)
            if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                return True
            # Check diagonal (top-left to bottom-right)
            if row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Function to get a valid column from the player
def get_valid_column(board, player):
    while True:
        column_input = input(f"Player {player}, please enter a column: ").upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + COLS - 1):
            column = ord(column_input) - ord('A')
            if board[0][column] == " ":
                return column
            else:
                print("Column is full. Choose another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

# Main game function
def connect_four():
    # Initialize game state
    board = create_board()
    players = PLAYERS[:PLAYER_COUNT]
    current_player = random.choice(players)

    # Start the game
    clear_screen()
    print_board(board)

    while True:
        # Get and validate player input
        print(f"Player {current_player}'s turn.")
        column = get_valid_column(board, current_player)

        # Place the checker
        place_checker(board, column, current_player)

        # Clear screen and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = players.index(current_player)
        current_player = players[(current_player_index + 1) % PLAYER_COUNT]

# Run the game
if __name__ == "__main__":
    connect_four()
