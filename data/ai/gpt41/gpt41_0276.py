import os
import random
import string

# ----- CONSTANTS -----
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change to test with different player counts (2-5 supported)
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Make sure no more players than available symbols
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"

# ----- FUNCTIONS -----

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create an empty board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column letters."""
    cols = len(board[0])
    # Print column headers (A, B, ...)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print("+" + "---+"*cols)
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print("+" + "---+"*cols)

def get_column_index(col_input, cols):
    """Return column index from letter input, or None if invalid."""
    if len(col_input) == 1 and col_input in string.ascii_uppercase[:cols]:
        return string.ascii_uppercase.index(col_input)
    return None

def is_column_full(board, col_idx):
    """Check if a column is full."""
    return all(row[col_idx] != " " for row in board)

def drop_checker(board, col_idx, symbol):
    """Drop a checker into the board, returns the row index, or None if column is full."""
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = symbol
            return row_idx
    return None

def valid_input(user_input, cols):
    """Checks if user input is a valid column letter."""
    return user_input and len(user_input) == 1 and user_input in string.ascii_uppercase[:cols]

def check_win(board, last_row, last_col, symbol):
    """Check board for a win after last move."""
    # Directions: (row_step, col_step)
    directions = [
        (0, 1),   # horiz.
        (1, 0),   # vert.
        (1, 1),   # diag down-right
        (1, -1)   # diag down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Is board full?"""
    return all(cell != " " for row in board for cell in row)

def choose_first_player(num_players):
    """Return random first player index."""
    return random.randint(0, num_players-1)

def main():
    board = create_board(ROWS, COLS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = choose_first_player(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {player_symbols[current_player]}, please enter a column:")

        col_input = input().strip().upper()
        # Validate input
        if not valid_input(col_input, COLS):
            print("Invalid input. Please enter a valid column letter.")
            input("Press Enter to continue...")
            continue
        col_idx = get_column_index(col_input, COLS)
        if is_column_full(board, col_idx):
            print("Column is full! You lose your turn.")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        # Place checker
        row_idx = drop_checker(board, col_idx, player_symbols[current_player])

        # Win check
        if check_win(board, row_idx, col_idx, player_symbols[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {player_symbols[current_player]} won!")
            break
        # Draw check
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
