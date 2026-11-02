import os
import random

# Constants for the board dimensions and player checkers
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+" + "---+" * COLS)  # Row border

def get_valid_input(player):
    """Prompt the player for a valid column input."""
    while True:
        column = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if column in [chr(65 + i) for i in range(COLS)]:
            return ord(column) - 65  # Return index instead of letter
        print("Invalid input. Please enter a letter corresponding to a column.")

def drop_checker(board, column, checker):
    """Drop the checker into the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """Check for a winning condition for the specified checker."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][c] != ' ' for c in range(COLS))

def play_connect4():
    """Main gameplay function."""
    board = create_board()
    random_player_index = random.randint(0, len(PLAYERS) - 1)
    current_player_index = random_player_index

    print_board(board)

    while True:
        current_checker = PLAYERS[current_player_index]
        column = get_valid_input(current_checker)

        if drop_checker(board, column, current_checker):
            print_board(board)

            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Please choose another column.")

# Run the game
if __name__ == "__main__":
    play_connect4()
