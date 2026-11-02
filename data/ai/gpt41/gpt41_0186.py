import random
import os
import string
import sys

# ========== CONSTANTS ==========
NUM_ROWS = 6
NUM_COLS = 7  # Max 26
NUM_PLAYERS = 2  # Change this for more players, max 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# ========== BOARD CREATION/PRINTING FUNCTIONS ==========
def create_board(rows, cols):
    # Create a rows x cols 2D list initialized with spaces
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Clear the terminal screen
    os.system('clear')

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    col_labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(col_labels)
    # Print separator
    print("+" + "---+" * cols)
    # Print rows of the board
    for row in board:
        print("|" + "|".join(f" {cell}" for cell in row) + "|")
        print("+" + "---+" * cols)

# ========== INPUT VALIDATION ==========
def get_valid_column_input(board, current_player):
    cols = len(board[0])
    valid_columns = string.ascii_uppercase[:cols]
    while True:
        move = input(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column: ").strip().upper()
        if len(move) != 1 or move not in valid_columns:
            print(f"Invalid input. Enter a single column letter from {valid_columns[0]} to {valid_columns[-1]}.")
            continue
        col_idx = valid_columns.index(move)
        # If column full, warn the player (and do not lose turn unless completely filled)
        if board[0][col_idx] != ' ':
            print("That column is full! You lose your turn.")
            return None  # Invalid move: player loses turn
        return col_idx

# ========== GAME LOGIC ==========
def place_checker(board, col_idx, symbol):
    # Place checker in the lowest available row in the column for symbol
    for row in reversed(range(len(board))):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = symbol
            return row, col_idx  # For win checking
    return None  # Should not happen if checked correctly

def check_win(board, symbol):
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            # Only check from the positions that have the player's symbol
            if board[r][c] != symbol:
                continue
            # Horizontal check
            if c + 3 < cols and all(board[r][c+i] == symbol for i in range(4)):
                return True
            # Vertical check
            if r + 3 < rows and all(board[r+i][c] == symbol for i in range(4)):
                return True
            # Diagonal down-right
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == symbol for i in range(4)):
                return True
            # Diagonal up-right
            if r - 3 >= 0 and c + 3 < cols and all(board[r-i][c+i] == symbol for i in range(4)):
                return True
    return False

def is_board_full(board):
    # If any top cell is still empty, board is not full
    return all(cell != ' ' for cell in board[0])

# ========== MAIN GAME ==========
def main():
    if NUM_COLS > 26:
        print("Error: Maximum number of columns is 26 due to labeling!")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: Only 2-5 players supported.")
        sys.exit(1)

    # Assign symbols to players
    active_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Create & display initial board
    board = create_board(NUM_ROWS, NUM_COLS)
    first_player = random.randint(0, NUM_PLAYERS - 1)
    current_player = first_player

    print_board(board)
    print(f"Randomly selected Player {active_symbols[first_player]} to start!")

    game_over = False
    winner = None

    while not game_over:
        print_board(board)
        col_idx = get_valid_column_input(board, current_player)
        if col_idx is None:
            # Column full: skip this player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        symbol = active_symbols[current_player]
        # Place checker for player
        row, col = place_checker(board, col_idx, symbol)

        # Check win
        if check_win(board, symbol):
            print_board(board)
            print(f"Player {symbol} won!")
            game_over = True
            winner = symbol
            break
        elif is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
            break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
