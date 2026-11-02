import os
import random
import string

# Constants for the board and game configuration
ROWS = 6
COLS = 7
MAX_COLS = 26
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # For submission: must be 2 players as per instructions

# Assign checkers based on the number of players
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

def create_board(rows, cols):
    """Create and return an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board):
    """Print the game board in a formatted way."""
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)
    print("+" + "---+" * cols)
    for row in board:
        row_str = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(row_str)
        print("+" + "---+" * cols)

def select_first_player(num_players):
    """Randomly select the index of the first player."""
    return random.randint(0, num_players - 1)

def get_valid_column_input(board, cols):
    """Prompt player for a valid column and return its index."""
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in string.ascii_uppercase[:cols]:
            print(f"Invalid column. Must be a letter from A to {string.ascii_uppercase[cols-1]}.")
            continue
        col_index = ord(col_input) - ord('A')
        # Check if the top cell is empty (i.e., column not full)
        if board[0][col_index] != " ":
            print("Column is full. You lose your turn.")
            return None  # Column is full
        return col_index

def place_checker(board, col, checker):
    """Drop the checker in the given column, return the row where it landed."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None  # Should not happen due to validation

def check_direction(board, row, col, d_row, d_col, checker):
    """Check a direction for 4-in-a-row."""
    count = 0
    r, c = row, col
    rows, cols = len(board), len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += d_row
        c += d_col
    return count

def is_winner(board, row, col, checker):
    """Check all directions for a win starting from (row, col)."""
    # Directions: horizontal, vertical, diag1, diag2
    directions = [
        (0, 1),  # right
        (1, 0),  # down
        (1, 1),  # diag down-right
        (1, -1), # diag down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        count += check_direction(board, row + dr, col + dc, dr, dc, checker)
        # Check the opposite direction
        count += check_direction(board, row - dr, col - dc, -dr, -dc, checker)
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full."""
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def play_connect4():
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS
    current_player = select_first_player(NUM_PLAYERS)
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player]}, you start first.")

    while True:
        player_checker = players[current_player]
        print(f"Player {player_checker}, ", end="")
        col_index = get_valid_column_input(board, COLS)
        if col_index is None:
            # Lose turn if full column
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row_index = place_checker(board, col_index, player_checker)

        clear_screen()
        print_board(board)

        # Check winner
        if is_winner(board, row_index, col_index, player_checker):
            print(f"Player {player_checker} won!")
            break

        if is_board_full(board):
            print("The game is a draw.")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_connect4()
