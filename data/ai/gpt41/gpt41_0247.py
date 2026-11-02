import os
import random
import sys

# ------------------------ CONSTANTS/CONFIGS ------------------------
ROWS = 6                # Number of rows (default Connect 4)
COLUMNS = 7             # Number of columns (default 7)
MAX_COLUMNS = 26        # Max value for columns (for labeling by letters)
PLAYERS = 2             # Number of players (can be from 2 to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
EMPTY_CELL = ' '


# ------------------------ BOARD FUNCTIONS ------------------------

def create_board(rows, columns):
    """Create a board filled with EMPTY_CELL."""
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Clear screen and print the current state of the board with labels."""
    os.system('clear' if os.name == 'posix' else 'cls')
    cols = len(board[0])
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    # Print column labels
    print("  " + "   ".join(col_labels))
    # Print line above the board
    print("+" + "---+" * cols)
    # Print each row of the board from top to bottom
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)


def is_full(board):
    """Check if the board is full."""
    return all(board[0][col] != EMPTY_CELL for col in range(len(board[0])))


def get_lowest_empty_row(board, col):
    """Return the lowest empty row index for a given column, or None if full."""
    for row in reversed(range(len(board))):
        if board[row][col] == EMPTY_CELL:
            return row
    return None


# ------------------------ INPUT FUNCTIONS ------------------------

def get_player_input(player, board):
    """Prompt user for a column letter and validate input."""
    cols = len(board[0])
    valid_cols = [chr(ord('A') + i) for i in range(cols)]
    while True:
        user_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in valid_cols:
            print(f"Invalid input. Please enter one of these letters: {', '.join(valid_cols)}.")
            continue
        col_idx = ord(user_input) - ord('A')
        if get_lowest_empty_row(board, col_idx) is not None:
            return col_idx
        else:
            print("Column is full. You lose your turn!")
            return None


# ------------------------ CHECK WIN FUNCTIONS ------------------------

def check_win(board, checker):
    """Check for 4 in a row (horizontal, vertical, diagonal) for given checker."""
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            # Only check from a cell belonging to current player
            if board[row][col] != checker:
                continue

            # Horizontal
            if col + 3 < cols:
                if all(board[row][col + offset] == checker for offset in range(4)):
                    return True

            # Vertical
            if row + 3 < rows:
                if all(board[row + offset][col] == checker for offset in range(4)):
                    return True

            # Diagonal down-right
            if row + 3 < rows and col + 3 < cols:
                if all(board[row + offset][col + offset] == checker for offset in range(4)):
                    return True

            # Diagonal up-right
            if row - 3 >= 0 and col + 3 < cols:
                if all(board[row - offset][col + offset] == checker for offset in range(4)):
                    return True

    return False


# ------------------------ MAIN GAME LOOP ------------------------

def main():
    board = create_board(ROWS, COLUMNS)
    total_players = PLAYERS
    player_symbols = CHECKERS

    # Randomly select who goes first
    current_player_idx = random.randint(0, total_players - 1)

    print_board(board)

    # Game loop
    while True:
        current_symbol = player_symbols[current_player_idx]
        # Get player move
        col = get_player_input(current_symbol, board)
        if col is not None:
            row = get_lowest_empty_row(board, col)
            if row is not None:
                board[row][col] = current_symbol
            # If column full, player loses turn (already handled and told to player)

        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % total_players

if __name__ == "__main__":
    main()
