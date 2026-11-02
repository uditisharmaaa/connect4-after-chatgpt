import os
import random
import string

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
NUM_PLAYERS = 2  # As per submission requirement: 2 players
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    """Creates and returns an empty game board filled with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the game board to the console with column labels."""
    clear_screen()
    # Column headers from A upwards
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def select_first_player(num_players):
    """Randomly selects the index of the first player."""
    return random.randint(0, num_players - 1)

def get_valid_input(prompt, valid_columns):
    """Prompts the user until a valid column letter is entered."""
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1:
            # Invalid input length
            continue
        if user_input not in valid_columns:
            # Not a valid column letter
            continue
        return user_input

def column_full(board, col_idx):
    """Checks if a column is completely filled on the board."""
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    """
    Places the checker in the specified column at the lowest available row.
    Returns True if placed, False if the column is full.
    """
    rows = len(board)
    for r in reversed(range(rows)):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """Checks if the given checker has four in a row anywhere on the board."""

    rows = len(board)
    cols = len(board[0])
    to_win = 4

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == to_win:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == to_win:
                    return True
            else:
                count = 0

    # Diagonal checks
    # Descending diagonal: top-left to bottom-right
    for r in range(rows - to_win + 1):
        for c in range(cols - to_win + 1):
            if all(board[r + i][c + i] == checker for i in range(to_win)):
                return True

    # Ascending diagonal: bottom-left to top-right
    for r in range(to_win - 1, rows):
        for c in range(cols - to_win + 1):
            if all(board[r - i][c + i] == checker for i in range(to_win)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full and there is no winner."""
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = select_first_player(NUM_PLAYERS)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        valid_columns = [chr(ord('A') + i) for i in range(COLUMNS)]
        prompt = f"Player {current_checker}, please enter a column: "

        # Get valid input from player
        col_letter = get_valid_input(prompt, valid_columns)
        col_idx = ord(col_letter) - ord('A')

        if column_full(board, col_idx):
            # Column full -> player loses turn (no re-try)
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        place_checker(board, col_idx, current_checker)

        # Check for win
        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw.")
            break

        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
