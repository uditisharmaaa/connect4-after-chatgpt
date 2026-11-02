import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Checker symbols
NUM_PLAYERS = 2  # Default number of players
EMPTY = " "  # Empty cell symbol

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Initialize a game board with all empty spaces."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board to the console."""
    clear_screen()
    # Print column headers
    column_headers = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(column_headers)
    print("+---" * len(board[0]) + "+")
    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, cols):
    """Check if the entered column is valid."""
    return column.isalpha() and len(column) == 1 and "A" <= column < chr(65 + cols)

def get_empty_row(board, col):
    """Find the lowest empty row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None

def place_checker(board, col, checker):
    """Place the checker's symbol in the lowest available row in the column."""
    row = get_empty_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def is_winner(board, checker):
    """Check if the player with 'checker' has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(board[0][col] != EMPTY for col in range(COLS))

def get_column_from_player(cols):
    """Prompt the player to choose a column and validate the input."""
    while True:
        column = input("Please enter a column letter: ").upper()
        if is_valid_column(column, cols):
            col_index = ord(column) - 65
            return col_index
        else:
            print("Invalid input. Enter a valid column letter (A-G).")

def main():
    """Main function to run the Connect 4 game."""
    # Initialization
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Randomly choose the first player
    print_board(board)

    while True:
        # Display current player's turn
        player_checker = PLAYERS[current_player]
        print(f"Player {player_checker}'s turn.")
        
        # Get valid column input
        column = get_column_from_player(COLS)

        # Place checker
        if not place_checker(board, column, player_checker):
            # If column is full
            print("Column is full. Try a different column.")
            continue

        # Print updated board
        print_board(board)

        # Check for a win
        if is_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
