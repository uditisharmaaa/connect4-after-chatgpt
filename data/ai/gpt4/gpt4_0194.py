import os
import random

# Constants
ROWS = 6  # Number of rows on the board
COLUMNS = 7  # Number of columns on the board
MAX_PLAYERS = 5  # Maximum number of players
MIN_PLAYERS = 2  # Minimum number of players
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Checker symbols for players


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """Create an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the game board to the console."""
    # Print column headers
    print("  " + "   ".join([chr(65 + i) for i in range(cols)]))
    print("+" + "---+" * cols)  # Top border
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)  # Row border


def is_valid_column(column, board):
    """Check if the column is valid and not full."""
    if not column.isalpha() or len(column) != 1:  # Validate input type
        return False
    column = ord(column.upper()) - 65  # Convert letter to index
    if column < 0 or column >= len(board[0]):  # Validate bounds
        return False
    return board[0][column] == " "  # Check if the column has space


def drop_checker(board, column, symbol):
    """Drop a checker into the specified column."""
    column = ord(column.upper()) - 65  # Convert letter to index
    for row in reversed(board):  # Start from the bottom
        if row[column] == " ":
            row[column] = symbol
            return True
    return False


def check_winner(board, symbol):
    """Check if a player has won."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal wins
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c:c + 4] == [symbol] * 4:
                return True

    # Check vertical wins
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Check diagonal (\ direction) wins
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Check diagonal (/ direction) wins
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True

    return False


def is_draw(board):
    """Check if the game is a draw (no spaces left)."""
    return all(cell != " " for row in board for cell in row)


def main():
    # Initialize board and players
    board = create_board(ROWS, COLUMNS)
    players = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
    players = max(MIN_PLAYERS, min(MAX_PLAYERS, players))  # Clamp player count
    player_symbols = PLAYER_SYMBOLS[:players]

    # Randomly select the starting player
    current_player = random.randint(0, players - 1)

    # Main game loop
    while True:
        clear_screen()
        print_board(board, COLUMNS)
        current_symbol = player_symbols[current_player]
        print(f"Player {current_symbol}, it's your turn.")

        # Get valid column input
        while True:
            column = input("Please enter a column (A-G): ").strip().upper()
            if is_valid_column(column, board):
                break
            else:
                print("Invalid input. Try again.")

        # Place the checker
        drop_checker(board, column, current_symbol)

        # Check for win or draw
        if check_winner(board, current_symbol):
            clear_screen()
            print_board(board, COLUMNS)
            print(f"Player {current_symbol} won!")
            break
        if is_draw(board):
            clear_screen()
            print_board(board, COLUMNS)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player = (current_player + 1) % players


if __name__ == "__main__":
    main()
