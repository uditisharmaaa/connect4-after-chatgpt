import os
import random
import string

# ------------------ CONSTANTS ---------------------
BOARD_ROWS = 6           # Number of rows (can be changed up to 26)
BOARD_COLS = 7           # Number of columns (can be changed up to 26)
NUM_PLAYERS = 2          # Number of players (between 2-5)

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

assert 2 <= NUM_PLAYERS <= 5, "Players must be between 2 and 5"
assert 1 <= BOARD_COLS <= 26, "Columns must be between 1 and 26"
assert 1 <= BOARD_ROWS <= 26, "Rows must be between 1 and 26"

COL_LETTERS = string.ascii_uppercase[:BOARD_COLS]        # e.g. 'A'...'G'

# ------------------ FUNCTIONS ---------------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """Creates a board with given rows and columns filled with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the board with proper formatting."""
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COL_LETTERS))
    print("+" + "---+" * BOARD_COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * BOARD_COLS)


def get_lowest_empty_row(board, col):
    """Returns the index of the lowest empty row in the specified column."""
    for row in reversed(range(BOARD_ROWS)):
        if board[row][col] == ' ':
            return row
    return None


def validate_input(inp, board):
    """Validates user input. Returns (True, col_index) if valid, else (False, reason)."""
    if len(inp) != 1 or inp not in COL_LETTERS:
        return False, "Invalid column letter. Please choose a valid column."
    col = COL_LETTERS.index(inp)
    if board[0][col] != ' ':
        return False, "Column is full. You lose your turn."
    return True, col


def place_checker(board, col, symbol):
    """Places the player's checker in the specified column."""
    row_index = get_lowest_empty_row(board, col)
    if row_index is not None:
        board[row_index][col] = symbol
        return row_index
    return None


def check_win(board, row, col, symbol):
    """Checks if inserting last checker at (row, col) makes symbol win."""
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False


def is_draw(board):
    """Checks if the board is full (draw)."""
    for col in range(BOARD_COLS):
        if board[0][col] == ' ':
            return False
    return True


# ------------------ MAIN GAME LOOP ---------------------

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    player_names = [f"Player {sym}" for sym in player_symbols]

    # Randomly choose who starts
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"{player_names[current_player]} starts!")
    input("Press Enter to start...")

    game_over = False

    while not game_over:
        symbol = player_symbols[current_player]
        name = player_names[current_player]

        print_board(board)
        print(f"{name}, please enter a column:")

        # Input processing, validation, turn handling
        valid_move = False
        col_index = None
        while not valid_move:
            user_input = input("> ").strip().upper()
            valid, result = validate_input(user_input, board)
            if not valid:
                print(result)
                # If input valid but column full, skip turn
                if "full" in result:
                    break   # lose turn
                else:
                    continue
            valid_move = True
            col_index = result

        # Handle placing checker (if move valid and not full column)
        if col_index is not None:
            row_index = place_checker(board, col_index, symbol)
            print_board(board)
            # Check win
            if check_win(board, row_index, col_index, symbol):
                print(f"{name} won!")
                game_over = True
                continue
            # Check draw
            if is_draw(board):
                print("The game is a draw!")
                game_over = True
                continue
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

    print("Game over.")


if __name__ == '__main__':
    main()
