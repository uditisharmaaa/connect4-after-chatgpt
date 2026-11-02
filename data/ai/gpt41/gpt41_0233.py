import os
import random

# -----------------------#
#  CONSTANTS AND GLOBALS #
# -----------------------#
ROWS = 6                  # Rows on the board
COLS = 7                  # Columns on the board (max 26; cols -> A-Z)
NUM_PLAYERS = 2           # Number of players (2-5)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

WIN_LENGTH = 4            # Number of checkers in a row to win

# --------------#
#  BOARD SETUP  #
# --------------#
def create_board(rows, cols):
    # Create a board filled with spaces
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # For Linux/Unix; use 'cls' for Windows
    cols = len(board[0])

    # Print columns header (A, B, C, ...)
    header = "  " + "   ".join([chr(ord('A') + c) for c in range(cols)])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        row_str = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(row_str)
        print('+' + '---+' * cols)

# -------------#
#  GAME LOGIC  #
# -------------#
def get_valid_columns(board):
    # Returns all columns that are not full (not filled at row 0)
    valid = []
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            valid.append(c)
    return valid

def input_column(board, player_symbol):
    cols = len(board[0])
    valid_columns = get_valid_columns(board)
    col_letters = [chr(ord('A') + c) for c in range(cols)]
    while True:
        col_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in col_letters:
            print(f"Invalid input! Please enter a column between A and {col_letters[-1]}.")
            continue
        col_index = ord(col_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print("Invalid column.")
            continue
        if col_index not in valid_columns:
            print("Column is full! You lose your turn.")
            return None  # Special case: lose turn
        return col_index

def place_checker(board, col_index, player_symbol):
    # Place the checker in the lowest empty row in the chosen column
    for row in reversed(range(len(board))):
        if board[row][col_index] == ' ':
            board[row][col_index] = player_symbol
            return row, col_index
    # Should not happen if checking for full column earlier

def check_winner(board, player_symbol):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c+i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r+i][c] == player_symbol for i in range(WIN_LENGTH)):
                return True
    # Diagonal (down-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    # Diagonal (up-right)
    for r in range(WIN_LENGTH-1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r-i][c+i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    return False

def is_draw(board):
    # If all top-row cells are filled, it's a draw
    return all(cell != ' ' for cell in board[0])

# -----------------#
#  MAIN GAME LOOP  #
# -----------------#
def main():
    # Board setup
    board = create_board(ROWS, COLS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Choose random player to start
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {player_symbols[current_player]} will start!\n")

    while True:
        player_symbol = player_symbols[current_player]
        col_index = input_column(board, player_symbol)
        if col_index is None:
            # Lose turn (column full only)
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row_index, col_index = place_checker(board, col_index, player_symbol)
        print_board(board)
        if check_winner(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
