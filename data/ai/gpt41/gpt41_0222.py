import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS_CHARS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')  # use 'clear' for Unix/Linux

def create_board(rows, cols):
    """Return an empty board (list of lists) of spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Display the board with column headers."""
    cols = len(board[0])
    # Print column letters
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(cols)])
    print(header)
    # Print separator
    print("+" + "---+" * cols)
    # Print each row
    for row in board:
        rowstr = "| " + " | ".join(row) + " |"
        print(rowstr)
        print("+" + "---+" * cols)

def get_player_input(player_char, cols):
    """Prompt player to select a column. Returns 0-based column index or None if invalid."""
    col_letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        choice = input(f"Player {player_char}, please enter a column: ").strip().upper()
        if len(choice) != 1 or choice not in col_letters:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = ord(choice) - ord('A')
        return col_idx

def place_checker(board, col, player_char):
    """Attempt to place checker in the chosen column. Return True if successful, False if full."""
    for row in reversed(board):  # start at bottom row
        if row[col] == " ":
            row[col] = player_char
            return True
    return False  # column full

def is_board_full(board):
    """Return True if board is full (no spaces)."""
    for row in board:
        if " " in row:
            return False
    return True

def check_winner(board, player_char):
    """Return True if player_char has 4 in a row somewhere."""
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != player_char:
                continue
            # Check horizontally
            if c <= cols - 4 and all(board[r][c + i] == player_char for i in range(4)):
                return True
            # Check vertically
            if r <= rows - 4 and all(board[r + i][c] == player_char for i in range(4)):
                return True
            # Check diagonal down-right
            if r <= rows - 4 and c <= cols - 4 and all(board[r + i][c + i] == player_char for i in range(4)):
                return True
            # Check diagonal up-right
            if r >= 3 and c <= cols - 4 and all(board[r - i][c + i] == player_char for i in range(4)):
                return True
    return False

def main():
    # Game configuration
    rows = ROWS
    cols = COLS
    num_players = MIN_PLAYERS  # For assignment, set to 2. Change for variants if desired.

    # Choose players' checkers in order.
    players = PLAYERS_CHARS[:num_players]

    # Initialize board
    board = create_board(rows, cols)

    # Choose a random first player
    current_player_idx = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    winner_found = False
    while True:
        player_char = players[current_player_idx]
        col_idx = get_player_input(player_char, cols)
        # Try to place checker. If column is full, skip turn with warning.
        if not place_checker(board, col_idx, player_char):
            print(f"Column {chr(ord('A')+col_idx)} is full. Player {player_char} loses the turn.")
            current_player_idx = (current_player_idx + 1) % num_players
            input("Press Enter to continue...")
            clear_screen()
            print_board(board)
            # skip win/draw check, go to next player
            continue

        clear_screen()
        print_board(board)

        # Check for win
        if check_winner(board, player_char):
            print(f"Player {player_char} won!")
            winner_found = True
            break

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
