import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
EMPTY_SLOT = " "
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

# Create and initialize the game board
def create_board():
    return [[EMPTY_SLOT for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board to the console
def print_board(board):
    os.system('clear')  # Clear the screen
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Check if a column is full
def is_valid_move(board, col):
    return board[0][col] == EMPTY_SLOT

# Place a checker in the chosen column
def drop_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == EMPTY_SLOT:
            board[row][col] = checker
            return True
    return False

# Check for a win condition
def check_win(board, checker):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal \ win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal / win
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row+i][col-i] == checker for i in range(4)):
                return True

    return False

# Check for a draw condition
def check_draw(board):
    return all(board[0][col] != EMPTY_SLOT for col in range(COLUMNS))

# Get the column index from the player's input
def get_column_index(choice):
    if choice in COLUMN_LABELS:
        return COLUMN_LABELS.index(choice)
    return -1

# Main game loop
def play_game():
    # Initialize board
    board = create_board()
    num_players = 2  # Can be set to any value up to MAX_PLAYERS
    player_checkers = PLAYERS[:num_players]

    # Choose a random starting player
    current_player = random.randint(0, num_players - 1)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {player_checkers[current_player]}'s turn")

        # Get player input
        while True:
            column_choice = input("Please enter a column: ").strip().upper()
            column_index = get_column_index(column_choice)
            if column_index != -1 and is_valid_move(board, column_index):
                break
            print("Invalid input. Try again.")

        # Place the checker
        drop_checker(board, column_index, player_checkers[current_player])

        # Check for win or draw
        if check_win(board, player_checkers[current_player]):
            print_board(board)
            print(f"Player {player_checkers[current_player]} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game()
