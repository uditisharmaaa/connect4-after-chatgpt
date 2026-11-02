import os
import random
import string

# Constants (change to try other board/player settings)
ROWS = 6           # Number of rows in the board
COLS = 7           # Number of columns in the board (max=26)
NUM_PLAYERS = 2    # 2-5 players

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])

# Create and initialize the board as a list of lists
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the current game board
def print_board(board):
    os.system('clear')  # or 'cls' on Windows
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Get the column index from user input
def get_column_index(input_letter):
    if input_letter in COLUMN_LABELS:
        return COLUMN_LABELS.index(input_letter)
    return -1

# Check if player's move is valid
def is_valid_move(board, col):
    if 0 <= col < COLS:
        # If the top cell in the column is empty, move is possible
        return board[0][col] == " "
    return False

# Place checker in the correct row for a column (lowest available)
def make_move(board, col, symbol):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col
    return None  # Column is full (shouldn't happen if move is valid)

# Check for 4-in-a-row win: horizontal, vertical, diagonals
def check_win(board, symbol):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == symbol for i in range(4)):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == symbol for i in range(4)):
                return True
    # Diagonal (\)
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == symbol for i in range(4)):
                return True
    # Diagonal (/)
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == symbol for i in range(4)):
                return True
    return False

# Check if board is full (draw)
def is_board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

# Get and validate the player's input
def get_player_move(board, player_symbol):
    while True:
        move = input(f"Player {player_symbol}, please enter a column: ")
        move = move.strip().upper()
        if len(move) != 1 or move not in COLUMN_LABELS:
            print("Invalid input. Enter a letter from the column headers (e.g., A-G).")
            continue
        col_idx = get_column_index(move)
        if not is_valid_move(board, col_idx):
            print("Column full or invalid. Try another column.")
            continue
        return col_idx

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS-1)
    print_board(board)
    print(f"Player {PLAYER_SYMBOLS[current_player]} starts!")
    while True:
        print_board(board)
        col = get_player_move(board, PLAYER_SYMBOLS[current_player])
        row, col = make_move(board, col, PLAYER_SYMBOLS[current_player])
        if check_win(board, PLAYER_SYMBOLS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a draw! No more moves.")
            break
        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
