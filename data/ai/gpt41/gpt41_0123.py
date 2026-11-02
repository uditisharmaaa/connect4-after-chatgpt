import os
import random
import string
import sys

# --- CONFIGURABLE CONSTANTS ---
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = 2  # Set to 2 (can be changed to 3, 4, or 5 for testing/development)
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# --- UTILITY FUNCTIONS ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    """Creates and returns an empty board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Prints the board to the terminal in the specified format."""
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + '   '.join(col_labels))
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+' + '---+' * cols)

def get_player_checker(player_idx):
    """Returns the checker symbol for the given player index."""
    return CHECKERS[player_idx]

def get_valid_columns(cols):
    """Returns the list of valid uppercase column letters."""
    return [chr(ord('A') + i) for i in range(cols)]

def get_column_index(col_letter, cols):
    """Converts a column letter to column index."""
    if col_letter not in get_valid_columns(cols):
        return -1
    return ord(col_letter) - ord('A')

def is_column_full(board, col_idx):
    """Checks if a column is full."""
    return all(board[row][col_idx] != ' ' for row in range(ROWS))

def drop_checker(board, col_idx, checker):
    """Drops the checker in the lowest available row of the selected column.
       Returns the row index where the checker was placed, or None if the column is full."""
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row
    return None  # Column is full

def check_win(board, last_row, last_col, checker):
    """Checks if placing checker at (last_row, last_col) results in a win."""
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Count the placed checker itself
        # Check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Checks if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def get_player_input(player_checker):
    """Prompts the player for input and returns the selected column letter."""
    prompt = f"Player {player_checker}, please enter a column: "
    return input(prompt).strip().upper()

def validate_input(col_input, board, cols):
    """Validates the player input and returns (is_valid, reason) tuple."""
    if len(col_input) != 1:
        return False, "Input must be a single letter."
    if col_input not in get_valid_columns(cols):
        return False, "Input out of board range."
    col_idx = get_column_index(col_input, cols)
    if is_column_full(board, col_idx):
        return False, "Column is full."
    return True, ""

# --- MAIN GAME FUNCTION ---

def play_game():
    # Game initialization
    board = create_board(ROWS, COLS)
    player_checkers = CHECKERS[:PLAYERS]
    valid_columns = get_valid_columns(COLS)
    current_player = random.randint(0, PLAYERS - 1)

    clear_screen()
    print_board(board, COLS)

    while True:
        player_checker = player_checkers[current_player]
        while True:
            col_input = get_player_input(player_checker)
            is_valid, reason = validate_input(col_input, board, COLS)
            if not is_valid:
                print(f"Invalid input: {reason}")
                continue
            break

        col_idx = get_column_index(col_input, COLS)
        if is_column_full(board, col_idx):
            print("Column is full! You lose your turn.")
            # Forfeit turn if column is full (as per assignment)
            current_player = (current_player + 1) % PLAYERS
            continue

        # Place the checker in the selected column
        row_idx = drop_checker(board, col_idx, player_checker)

        clear_screen()
        print_board(board, COLS)

        # Check for win
        if check_win(board, row_idx, col_idx, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

# --- ENTRY POINT ---

if __name__ == '__main__':
    play_game()
