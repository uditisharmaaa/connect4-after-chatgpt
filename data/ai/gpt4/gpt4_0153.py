import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLS)]  # ['A', 'B', 'C', ...]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(column):
    """Checks if the column is valid."""
    return column in COLUMN_LABELS

def get_column_index(column):
    """Gets the index of the column."""
    return COLUMN_LABELS.index(column)

def drop_checker(board, column, checker):
    """Attempts to drop the checker into the given column."""
    col_index = get_column_index(column)
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False  # Column is full

def is_draw(board):
    """Checks if the board is full, resulting in a draw."""
    for row in board:
        if ' ' in row:
            return False
    return True

def check_for_win(board, checker):
    """Checks if the given player has won."""
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == checker:
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == checker:
                return True

    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True

    # Check diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True

    return False

def main():
    # Initialize the game
    board = create_board()
    current_player_idx = random.randint(0, PLAYERS - 1)
    game_active = True

    print_board(board)

    # Main game loop
    while game_active:
        current_player = CHECKERS[current_player_idx]
        print(f"Player {current_player}, please enter a column:")
        player_input = input("> ").upper()

        # Validate input
        if not is_valid_column(player_input):
            print("Invalid input! Please enter a valid column.")
            continue

        # Attempt to drop checker
        if not drop_checker(board, player_input, current_player):
            print("This column is full! Please choose another column.")
            continue

        # Print updated board
        print_board(board)

        # Check for win
        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            game_active = False
            continue

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            game_active = False
            continue

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
