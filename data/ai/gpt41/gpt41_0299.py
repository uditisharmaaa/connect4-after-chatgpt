import os
import random
import sys

# === CONSTANTS ===
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
MAX_PLAYERS = 5
MIN_PLAYERS = 2
MAX_COLUMNS = 26
# Game settings (required by assignment: 6 rows x 7 columns, 2 players)
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# === UTILITY FUNCTIONS ===

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    """Creates a blank board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board with column letters."""
    col_labels = "  "
    for i in range(len(board[0])):
        col_labels += " " + chr(ord('A') + i) + "  "
    print(col_labels)

    horizontal_line = "+" + "---+"*len(board[0])
    for row in board:
        print(horizontal_line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(horizontal_line)

def select_start_player(num_players):
    """Randomly selects a starting player index."""
    return random.randint(0, num_players-1)

def column_letter_to_index(letter):
    """Converts a column letter to a 0-based index."""
    if len(letter) != 1 or not letter.isalpha() or not letter.isupper():
        return -1
    idx = ord(letter) - ord('A')
    return idx

def is_column_full(board, col_idx):
    """Checks if a column is full."""
    return all(board[row][col_idx] != " " for row in range(len(board)))

def board_full(board):
    """Returns True if the board is full."""
    return all(is_column_full(board, col) for col in range(len(board[0])))

def get_valid_input(board):
    """Keeps prompting user until a valid column letter is entered."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input: input must be a single letter")
            continue
        col_idx = column_letter_to_index(user_input)
        if col_idx < 0 or col_idx >= len(board[0]):
            print("Invalid input: column not on the board")
            continue
        if is_column_full(board, col_idx):
            print("Column is full! You lose your turn.")
            return None  # Indicate turn lost
        return col_idx

def drop_checker(board, col_idx, symbol):
    """Drops a checker in the specified column, returns row index placed at."""
    for row in range(len(board)-1, -1, -1):  # Start from bottom row
        if board[row][col_idx] == " ":
            board[row][col_idx] = symbol
            return row
    return -1  # Should not happen if validated before

def check_win(board, row, col, symbol):
    """Checks for a win from (row, col) for the given symbol."""

    def count_direction(drow, dcol):
        r, c = row + drow, col + dcol
        count = 0
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
            r += drow
            c += dcol
        return count

    # Four directions: horizontal, vertical, diagonal /
    # and diagonal \
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]

    for drow, dcol in directions:
        total = 1  # Starting with the last placed checker
        total += count_direction(drow, dcol)
        total += count_direction(-drow, -dcol)
        if total >= WIN_LENGTH:
            return True
    return False

def all_checkers():
    return PLAYER_SYMBOLS[:NUM_PLAYERS]

def game_loop(board, num_players):
    """Main game loop."""
    players = all_checkers()
    player_names = [f"Player {s}" for s in players]
    current = select_start_player(num_players)
    game_over = False

    clear_screen()
    print_board(board)

    while not game_over:
        symbol = players[current]
        name = player_names[current]
        print(f"{name} ({symbol}), ", end="")
        col = None
        col = get_valid_input(board)
        if col is None:
            # Full column, player loses turn:
            current = (current + 1) % num_players
            clear_screen()
            print_board(board)
            continue
        row = drop_checker(board, col, symbol)
        clear_screen()
        print_board(board)
        if check_win(board, row, col, symbol):
            print(f"{name} won!")
            game_over = True
            break
        if board_full(board):
            print("It's a draw!")
            game_over = True
            break
        current = (current + 1) % num_players

# === MAIN ===

def main():
    # Sanity checks for assignment constraints
    assert MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS, "Invalid number of players"
    assert 1 <= NUM_COLS <= MAX_COLUMNS, "Invalid number of columns"
    board = create_board(NUM_ROWS, NUM_COLS)
    game_loop(board, NUM_PLAYERS)

if __name__ == "__main__":
    main()
