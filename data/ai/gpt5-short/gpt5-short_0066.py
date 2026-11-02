import os
import random
import sys

# ========= Configuration Constants =========
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # Must match COLS
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']           # Up to 5 players
NUM_PLAYERS = 2                                      # Change between 2 and 5

# ========= Utility Functions =========
def clear_screen():
    """
    Clear the terminal screen. Uses 'clear' as requested.
    On Windows, 'clear' may not work; if needed, change to 'cls' or add a fallback.
    """
    os.system('clear')


def create_board(rows=ROWS, cols=COLS):
    """Create an empty board with given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board to the console.
    Top row is row 0; bottom is row ROWS-1.
    """
    # Print column labels
    print('   ' + '   '.join(COLUMN_LABELS))
    print('  +' + '---+' * COLS)

    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('  | ' + ' | '.join(row_cells) + ' |')
        print('  +' + '---+' * COLS)


def letter_to_col(letter):
    """Convert a column letter (A-G) to a 0-based column index. Returns None if invalid."""
    if not letter or len(letter) != 1:
        return None
    letter = letter.upper()
    if letter in COLUMN_LABELS:
        return COLUMN_LABELS.index(letter)
    return None


def get_next_open_row(board, col):
    """
    Return the row index where the next piece would land in the given column,
    or None if the column is full.
    Pieces fall to the bottom-most empty space.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None


def is_valid_move(board, col):
    """A move is valid if the column is within bounds and not full."""
    if col is None or col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '  # top cell empty => column has space


def drop_piece(board, row, col, symbol):
    """Place a player's symbol into the given row, col."""
    board[row][col] = symbol


def check_win(board, symbol):
    """
    Check for a win (4 in a row) for a specific symbol.
    Checks horizontal, vertical, and two diagonal directions.
    """
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and board[r][c+1] == symbol and
                board[r][c+2] == symbol and board[r][c+3] == symbol):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == symbol and board[r+1][c] == symbol and
                board[r+2][c] == symbol and board[r+3][c] == symbol):
                return True

    # Diagonal down-right (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and board[r+1][c+1] == symbol and
                board[r+2][c+2] == symbol and board[r+3][c+3] == symbol):
                return True

    # Diagonal up-right (/)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and board[r-1][c+1] == symbol and
                board[r-2][c+2] == symbol and board[r-3][c+3] == symbol):
                return True

    return False


def check_draw(board):
    """The game is a draw if the top row has no empty spaces and no wins have occurred."""
    return all(board[0][c] != ' ' for c in range(COLS))


def get_player_symbols(num_players):
    """
    Return the list of symbols for the number of players.
    Ensures num_players is between 2 and min(5, len(PLAYER_SYMBOLS)).
    """
    max_players = min(5, len(PLAYER_SYMBOLS))
    if num_players < 2 or num_players > max_players:
        raise ValueError(f"NUM_PLAYERS must be between 2 and {max_players}")
    return PLAYER_SYMBOLS[:num_players]


def prompt_move(current_symbol):
    """
    Prompt the user to enter a column (A-G). Validates format.
    Returns the column index or None (if invalid).
    """
    raw = input(f"Player {current_symbol}, choose a column (A-G): ").strip()
    if not raw:
        return None
    col = letter_to_col(raw[0])
    return col


def main():
    # Validate configuration
    try:
        symbols = get_player_symbols(NUM_PLAYERS)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Create game state
    board = create_board()
    start_index = random.randint(0, len(symbols) - 1)  # random first player
    current_index = start_index

    # Main game loop
    while True:
        clear_screen()
        print("Connect 4 - 6 rows x 7 columns")
        print(f"Players: {', '.join(symbols)}  |  First player (random): {symbols[start_index]}")
        print_board(board)

        current_symbol = symbols[current_index]

        # Get a valid move
        col = None
        while True:
            col = prompt_move(current_symbol)
            if col is None:
                print("Invalid input. Enter a single letter A-G.")
                continue
            if not is_valid_move(board, col):
                # Distinguish between out-of-range and full column where possible
                if col < 0 or col >= COLS:
                    print("That column is out of range. Please choose A-G.")
                else:
                    print(f"Column {COLUMN_LABELS[col]} is full. Choose another column.")
                continue
            break

        # Apply the move
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_symbol)

        # Check for win
        if check_win(board, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more valid moves.")
            break

        # Next player's turn (wrap around)
        current_index = (current_index + 1) % len(symbols)


if __name__ == "__main__":
    main()
