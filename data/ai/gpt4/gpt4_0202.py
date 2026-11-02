import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear') # Clears the console
    # Print column labels
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(choice, board):
    """Check if a user input for a column is valid."""
    if len(choice) != 1 or not choice.isalpha():
        return False
    col_index = ord(choice.upper()) - 65
    return 0 <= col_index < COLUMNS and board[0][col_index] == " "

def get_column_index(choice):
    """Convert column letter to an index."""
    return ord(choice.upper()) - 65

def place_checker(board, col_index, symbol):
    """Place the player's checker in the specified column."""
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = symbol
            break

def check_winner(board, symbol):
    """Check if the current player has won the game."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [symbol] * 4:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonals (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game board is completely filled."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize the game
    board = create_board()
    num_players = 2  # Set to 2 for submission; can be updated for up to MAX_PLAYERS
    symbols = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)

    # Display the initial board
    print_board(board)

    # Game loop
    while True:
        # Current player information
        print(f"Player {symbols[current_player]}, it's your turn.")
        choice = input("Please enter a column: ").strip()

        # Validate input and process turn
        if is_valid_column(choice, board):
            col_index = get_column_index(choice)
            place_checker(board, col_index, symbols[current_player])
            print_board(board)

            # Check for win
            if check_winner(board, symbols[current_player]):
                print(f"Player {symbols[current_player]} won!")
                break

            # Check for draw
            if is_draw(board):
                print("The game is a draw!")
                break

            # Switch to the next player
            current_player = (current_player + 1) % num_players
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
