import os
import random
import string

# ==== CONSTANTS ====
ROWS = 6  # number of rows (default: 6)
COLS = 7  # number of columns (default: 7, max: 26)
NUM_PLAYERS = 2  # (between 2-5)

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
assert 1 <= COLS <= 26, "Columns must be between 1 and 26."
assert ROWS >= 1, "Board must have at least 1 row."


# ==== FUNCTIONS ====
def clear_screen():
    os.system('clear')

def create_board():
    """Create a 2D board with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the board in the specified format."""
    clear_screen()
    letters = list(string.ascii_uppercase[:COLS])
    header = "  " + "   ".join(letters)
    separator = "+" + "---+" * COLS
    print(header)
    print(separator)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(separator)

def get_player_symbols():
    """Return the list of player symbols for the game."""
    return PLAYER_SYMBOLS[:NUM_PLAYERS]

def get_col_from_input(col_input):
    """Convert column letter to column index. Return None if invalid."""
    if len(col_input) != 1 or col_input not in string.ascii_uppercase[:COLS]:
        return None
    return string.ascii_uppercase.index(col_input)

def is_valid_column(col_input):
    """Check if input corresponds to a valid column index."""
    return get_col_from_input(col_input) is not None

def get_next_open_row(board, col):
    """Return the row index where the checker will fall, or None if column is full."""
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            return row
    return None

def place_checker(board, row, col, symbol):
    """Place the player's checker at the specified location."""
    board[row][col] = symbol

def check_win(board, symbol):
    """Check for a win (horizontally, vertically, or diagonally) for symbol."""
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def select_starting_player():
    """Return randomly chosen player index."""
    return random.randint(0, NUM_PLAYERS - 1)

def get_player_input(player_symbol, board):
    """Prompt and validate the player input for column choice."""
    letters = list(string.ascii_uppercase[:COLS])
    while True:
        inp = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if not is_valid_column(inp):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = get_col_from_input(inp)
        if get_next_open_row(board, col) is None:
            print("Column is full. You lose your turn.")
            return None  # turn lost
        return col

# ==== MAIN GAME FUNCTION ====
def connect4():
    board = create_board()
    player_symbols = get_player_symbols()
    player_idx = select_starting_player()
    print_board(board)
    print(f"Player {player_symbols[player_idx]} starts!")
    
    while True:
        print_board(board)
        col = get_player_input(player_symbols[player_idx], board)
        if col is None:
            # Column is full, player loses the turn
            player_idx = (player_idx + 1) % NUM_PLAYERS
            continue
        row = get_next_open_row(board, col)
        place_checker(board, row, col, player_symbols[player_idx])

        # Check for win
        if check_win(board, player_symbols[player_idx]):
            print_board(board)
            print(f"Player {player_symbols[player_idx]} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        player_idx = (player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect4()
