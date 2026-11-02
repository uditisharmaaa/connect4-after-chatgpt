import os
import random
import string

# ----------- CONSTANTS -----------------

# Board dimensions (6 rows x 7 columns)
NUM_ROWS = 6
NUM_COLS = 7

# Players (between 2 and 5)
NUM_PLAYERS = 2

# Checker symbols for up to 5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']


# ---------- FUNCTIONS ------------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """Creates an empty board as a list of lists."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the Connect 4 board in a formatted way."""
    cols = len(board[0])
    
    # Print column labels as letters
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    
    # Print separator
    print("+" + "---+" * cols)
    
    # Print each row
    for row in board:
        row_line = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(row_line)
        print("+" + "---+" * cols)


def get_player_symbols(num_players):
    """Returns the list of playing symbols for the current number of players."""
    return PLAYER_SYMBOLS[:num_players]


def choose_first_player(num_players):
    """Randomly chooses a first player (returns index)."""
    return random.randint(0, num_players - 1)


def is_valid_column(input_str, num_cols):
    """Checks if the input string is a valid column letter in the board."""
    if len(input_str) != 1:
        return False
    col_letter = input_str.upper()
    allowed_cols = string.ascii_uppercase[:num_cols]
    return col_letter in allowed_cols


def is_column_full(board, col):
    """Returns True if the given column in the board is already full."""
    return board[0][col] != ' '  # Top cell filled? then full


def get_next_open_row(board, col):
    """
    Returns the bottom-most open row index for the given column.
    If the column is full, returns None.
    """
    for row in range(len(board) - 1, -1, -1):  # bottom to top
        if board[row][col] == ' ':
            return row
    return None


def place_checker(board, row, col, symbol):
    """Places player's symbol on the board at (row, col)."""
    board[row][col] = symbol


def check_for_win(board, symbol):
    """Checks if the player with 'symbol' has won."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal locations
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + offset] == symbol for offset in range(4)):
                return True

    # Check vertical locations
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + offset][c] == symbol for offset in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + offset][c + offset] == symbol for offset in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - offset][c + offset] == symbol for offset in range(4)):
                return True

    return False


def board_is_full(board):
    """Returns True if the board is full (draw)."""
    return all(board[0][col] != ' ' for col in range(len(board[0])))


def get_player_move(player_symbol, num_cols, board):
    """
    Prompts the player to input a column letter and validates it.
    Returns the (col_index, True) if valid and available,
    returns (col_index, False) if invalid (column full - turn lost),
    keeps asking if input is non-letter or outside board.
    """
    while True:
        move = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        # Check for valid column letter:
        if not is_valid_column(move, num_cols):
            print("Invalid column! Please enter a valid column letter (e.g., A, B, ...).")
            continue
        col_index = string.ascii_uppercase.index(move)
        if is_column_full(board, col_index):
            print("Column is full! You lose your turn.")
            return col_index, False
        return col_index, True


# ----------- MAIN PROGRAM --------------

def main():
    # Set up the game with constants at top
    board = create_board(NUM_ROWS, NUM_COLS)
    player_symbols = get_player_symbols(NUM_PLAYERS)
    current_player_idx = choose_first_player(NUM_PLAYERS)

    # Print starting board and info
    clear_screen()
    print_board(board)
    print(f"Players: {' '.join(player_symbols)}")
    print(f"Player {player_symbols[current_player_idx]} starts!\n")

    game_over = False

    while not game_over:
        player_symbol = player_symbols[current_player_idx]

        # Player input and move validation:
        col_index, valid_move = get_player_move(player_symbol, NUM_COLS, board)
        # Put the checker if the turn is not lost:
        if valid_move:
            row_index = get_next_open_row(board, col_index)
            place_checker(board, row_index, col_index, player_symbol)

            # Clear screen and print updated board:
            clear_screen()
            print_board(board)

            # Check for win
            if check_for_win(board, player_symbol):
                print(f"Player {player_symbol} won!")
                game_over = True
                continue

            # Check for draw:
            if board_is_full(board):
                print("The game is a draw.")
                game_over = True
                continue
        else:
            # Even if the column is full and invalid, still print board as feedback
            clear_screen()
            print_board(board)

        # Next player's turn (if not game over)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
