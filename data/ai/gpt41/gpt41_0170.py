import os
import random
import string
import sys

# Constants for board size and game setup
ROWS = 6                # Number of rows (default: 6)
COLUMNS = 7             # Number of columns (default: 7, max 26)
NUM_PLAYERS = 2         # Number of players (min 2, max 5)

# Valid checker symbols for up to five players
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Set up column labels ('A'...'Z')
COLUMN_LABELS = list(string.ascii_uppercase)[:COLUMNS]

def clear_screen():
    """
    Clear the terminal screen using os.system.
    """
    os.system('clear')

def create_board(rows, cols):
    """
    Create a 2D board (list of lists) initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the current board in the required format.
    """
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_valid_columns(board):
    """
    Return a list of indices for columns that are not full.
    """
    valid = []
    for col in range(COLUMNS):
        if board[0][col] == " ":
            valid.append(col)
    return valid

def get_player_input(player_checker, board):
    """
    Prompt the player for column input. Validate input and return column index.
    Invalid entries (non-letters, out-of-range, full columns) are handled.
    If column is completely full, the player loses their turn.
    """
    valid_columns = get_valid_columns(board)
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Input should be a single letter
        if len(user_input) != 1 or user_input not in COLUMN_LABELS:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_index = COLUMN_LABELS.index(user_input)
        if col_index not in valid_columns:
            if board[0][col_index] != " ":
                print("Column is full! You lose your turn.")
                return None
            else:
                print("Invalid input. Please select a non-full column.")
                continue
        return col_index

def place_checker(board, col, player_checker):
    """
    Place the checker's symbol at the lowest empty position in a column.
    """
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row, col
    return None  # Should not happen if checked before

def check_direction(board, row, col, dr, dc, player_checker):
    """
    Check in a specific direction for 4 in a row.
    dr, dc: row and col deltas. E.g., dr=1, dc=0 for down.
    Returns count of continuous player_checker in that direction (including origin).
    """
    count = 0
    r, c = row, col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, player_checker):
    """
    Check all 4 directions from (row, col) for win condition (4 in a row).
    Returns True if winning move.
    """
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Include the placed checker
        # Check in positive direction
        count += check_direction(board, row + dr, col + dc, dr, dc, player_checker)
        # Check in negative direction
        count += check_direction(board, row - dr, col - dc, -dr, -dc, player_checker)
        if count >= 4:
            return True
    return False

def is_draw(board):
    """
    Check if the board is full (draw).
    """
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    """
    Main game loop for Connect 4
    """
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    # Randomly pick the starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    # Game loop
    while True:
        player_checker = players[current_player_idx]

        col_index = get_player_input(player_checker, board)
        clear_screen()

        if col_index is None:
            # If player lost turn because the column is full
            print_board(board)
            if is_draw(board):
                print("It's a draw!")
                break
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        placement = place_checker(board, col_index, player_checker)
        print_board(board)

        row_placed, col_placed = placement

        # Check for win
        if check_win(board, row_placed, col_placed, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Alternate turns
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
