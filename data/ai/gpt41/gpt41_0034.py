import os
import random
import string

# Constants
ROWS = 6                             # Number of rows
COLS = 7                             # Number of columns (max 26)
PLAYERS = 2                          # Number of players (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M'] # Player checker symbols

# Initialize available checkers for current game
PLAYER_SYMBOLS = CHECKERS[:PLAYERS]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty board initialized with whitespaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    # Print column labels
    column_labels = list(string.ascii_uppercase[:COLS])
    header = '  ' + '   '.join(column_labels)
    print(header)
    print('+' + '---+'*COLS)
    # Print rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+'*COLS)

def get_valid_column(board, input_char):
    """Validates and returns the column index if the input is valid, else None."""
    input_char = input_char.strip().upper()
    valid_labels = list(string.ascii_uppercase[:COLS])
    if len(input_char) != 1 or input_char not in valid_labels:
        return None
    col = valid_labels.index(input_char)
    # Check if the column is not full
    if board[0][col] != ' ':
        return None
    return col

def place_checker(board, col, checker):
    """
    Places the checker in the lowest available row of the given column.
    Returns the row index where the checker was placed, or None if the column is full.
    """
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return None

def is_board_full(board):
    """Checks if the board is full."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def check_win(board, last_row, last_col, checker):
    """
    Checks if there's a connect 4 starting with the last placed checker.
    Returns True if the player has won; otherwise, False.
    """
    # Directions: (delta_row, delta_col)
    directions = [
        ( 0,  1), # Horizontal
        ( 1,  0), # Vertical
        ( 1,  1), # Diagonal down (to right)
        ( 1, -1), # Diagonal down (to left)
    ]

    for dr, dc in directions:
        count = 1
        # Scan forward
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Scan backward
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def main():
    # Initialize the board
    board = create_board()

    # Randomly pick who starts
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    print(f"Player {PLAYER_SYMBOLS[current_player]} starts! Press Enter to continue...")
    input()

    # Game loop
    winner = None
    while True:
        print_board(board)
        player_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {player_symbol}, please enter a column:")

        # Input loop: keep prompting until a valid move is made or column is full
        col = None
        while col is None:
            user_input = input('> ')
            col_candidate = get_valid_column(board, user_input)
            # If column is full, return None. Must penalize and lose turn in this case.
            if col_candidate is not None:
                row_candidate = place_checker([row.copy() for row in board], col_candidate, player_symbol)
                if row_candidate is not None:
                    col = col_candidate
                else:
                    print(f"Column {user_input.upper()} is full! You lose your turn.")
                    col = None
                    break  # Lose turn, go to next player
            else:
                print("Invalid column! Please enter a valid column letter (e.g., A, B, ...). Try again...")

        # Only actually place the checker if column was valid and not full
        if col is not None:
            row = place_checker(board, col, player_symbol)

            # Check for win from the newest checker
            if check_win(board, row, col, player_symbol):
                print_board(board)
                print(f"Player {player_symbol} won!")
                break

        # After move or losing turn, check if board is full (draw)
        if is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
