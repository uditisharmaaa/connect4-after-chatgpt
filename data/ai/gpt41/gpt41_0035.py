import os
import random
import string

# -------------------------------
# Constants (Adjust if needed)
# -------------------------------
ROWS = 6
COLUMNS = 7                  # Up to 26 supported (A-Z)
NUM_PLAYERS = 2              # 2 to 5 supported
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# -------------------------------
# Helper Functions
# -------------------------------

def clear_screen():
    """Clears terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates a blank board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Displays the board."""
    columns = len(board[0])
    # Header letters
    header = "  " + "   ".join(string.ascii_uppercase[:columns])
    separator = "+" + ("---+" * columns)
    print(header)
    print(separator)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(separator)

def get_valid_input(prompt, valid_columns):
    """Gets a valid column input from the user."""
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1 or user_input not in valid_columns:
            print(f"Invalid input. Please enter one of {', '.join(valid_columns)}.")
            continue
        return user_input

def get_next_open_row(board, col):
    """Finds the next open row in the specified column. Returns -1 if full."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, row, col, checker):
    """Places the player's checker at specified position."""
    board[row][col] = checker

def is_board_full(board):
    """Determine whether the board is fully filled."""
    return all(cell != " " for row in board for cell in row)

def check_winner(board, row, col, checker):
    """Checks if placing a checker at (row, col) wins the game."""
    return (check_line(board, row, col, checker, 0, 1) + check_line(board, row, col, checker, 0, -1) + 1 >= WIN_LENGTH or  # Horizontal
            check_line(board, row, col, checker, 1, 0) + check_line(board, row, col, checker, -1, 0) + 1 >= WIN_LENGTH or  # Vertical
            check_line(board, row, col, checker, 1, 1) + check_line(board, row, col, checker, -1, -1) + 1 >= WIN_LENGTH or # Diagonal /
            check_line(board, row, col, checker, 1, -1) + check_line(board, row, col, checker, -1, 1) + 1 >= WIN_LENGTH)   # Diagonal \

def check_line(board, row, col, checker, delta_row, delta_col):
    """Checks one direction for consecutive checkers."""
    count = 0
    r, c = row + delta_row, col + delta_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def next_player(current, total):
    """Returns index of next player."""
    return (current + 1) % total

# -------------------------------
# Main Game Logic
# -------------------------------

def main():
    # Sanity checks for settings
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLUMNS <= 26):
        print("Error: COLUMNS must be between 1 and 26.")
        return

    random.seed()
    board = create_board(ROWS, COLUMNS)
    player_tokens = CHECKERS[:NUM_PLAYERS]
    player_names = [f"Player {token}" for token in player_tokens]
    valid_columns = list(string.ascii_uppercase[:COLUMNS])  # "A".."G" for 7 cols

    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        print(f"{player_names[current_player]} ({player_tokens[current_player]}), please enter a column:")

        # Input phase
        col_letter = get_valid_input("> ", valid_columns)
        col_index = ord(col_letter) - ord('A')

        row_index = get_next_open_row(board, col_index)
        if row_index == -1:
            print("That column is full. Turn lost. Press Enter to continue...")
            input()
            current_player = next_player(current_player, NUM_PLAYERS)
            continue

        # Place the checker
        place_checker(board, row_index, col_index, player_tokens[current_player])

        # Check for win
        if check_winner(board, row_index, col_index, player_tokens[current_player]):
            clear_screen()
            print_board(board)
            print(f"{player_names[current_player]} ({player_tokens[current_player]}) won!")
            break

        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = next_player(current_player, NUM_PLAYERS)

if __name__ == "__main__":
    main()
