import os
import random

# Constants for board dimensions
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Constants for player tokens (supports 2 to 5 players)
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """Create an empty board initialized with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board to the terminal."""
    print("  " + " ".join(COLUMN_LABELS))  # Print column labels
    for row in board:
        print("|" + "|".join(row) + "|")  # Print each row with vertical separators
    print("-" * (COLUMNS * 2 + 1))  # Bottom border

def get_player_count():
    """Ask for the number of players (2-5), validating the input."""
    while True:
        try:
            count = int(input("Enter number of players (2-5): "))
            if 2 <= count <= 5:
                return count
            else:
                print("Invalid number of players. Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 2 and 5.")

def get_move(player_token):
    """
    Prompt the player to enter a column letter.
    Validate the input and return the corresponding column index.
    """
    while True:
        move = input(f"Player {player_token}, choose a column (A-G): ").upper()
        if len(move) == 1 and move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print("Invalid input. Please enter a column letter from A to G.")

def make_move(board, col, player_token):
    """
    Drop the player's token into the chosen column, if space is available.
    Return True if move successful, False if column is full.
    """
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player_token
            return True
    return False  # Column is full

def check_winner(board, player_token):
    """
    Check all directions for a connect 4 for the given player token.
    Returns True if the player has won, else False.
    """

    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == player_token for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player_token for i in range(4)):
                return True

    # Check positively sloped diagonals (/)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == player_token for i in range(4)):
                return True

    # Check negatively sloped diagonals (\)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == player_token for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full, indicating a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    # Initialize game
    player_count = get_player_count()
    players = PLAYER_TOKENS[:player_count]

    # Choose random first player
    current_player_index = random.randint(0, player_count - 1)
    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        current_player_token = players[current_player_index]

        # Get move input and validate drop
        col = get_move(current_player_token)
        if not make_move(board, col, current_player_token):
            print("That column is full. Try a different one.")
            input("Press Enter to continue...")
            continue

        # Check for win
        if check_winner(board, current_player_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_player_token} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! The board is full with no winner.")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % player_count

if __name__ == "__main__":
    main()
