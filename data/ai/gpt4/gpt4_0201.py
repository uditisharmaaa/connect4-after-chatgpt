import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# Function to create an empty board
def create_board(rows, columns):
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    column_labels = "  " + "   ".join(chr(65 + col) for col in range(len(board[0])))
    print(column_labels)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# Function to check if a column is valid for a move
def is_valid_column(board, col):
    return 0 <= col < len(board[0]) and board[0][col] == EMPTY_CELL

# Function to place checker in the column
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == EMPTY_CELL:
            row[col] = checker
            return

# Function to check for a win
def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (/)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Function to check if the board is full (draw)
def is_draw(board):
    return all(cell != EMPTY_CELL for row in board for cell in row)

# Main game function
def connect_4():
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Fixed to 2 players, but can be adjusted if needed
    players = PLAYERS[:num_players]
    current_player = random.choice(players)

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLUMNS - 1)}):", end=" ")
        player_input = input().strip().upper()

        # Validate input
        if len(player_input) != 1 or not player_input.isalpha() or not ('A' <= player_input <= 'A' + str(COLUMNS - 1)):
            print("Invalid input! Please enter a valid column letter.")
            continue

        column = ord(player_input) - 65  # Convert column letter to index

        if not is_valid_column(board, column):
            print("Invalid move! Column is full or out of range.")
            continue

        # Place the checker
        place_checker(board, column, current_player)

        # Print the updated board
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % num_players]

# Run the game
if __name__ == "__main__":
    connect_4()
