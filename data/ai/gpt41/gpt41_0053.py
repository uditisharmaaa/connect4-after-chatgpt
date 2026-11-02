import os
import random
import string

# --- CONSTANTS ---
ROWS = 6
COLS = 7
MAX_COLS = 26   # For flexible board resizing if needed
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change for more players (max 5)
WIN_LENGTH = 4

# --- FUNCTIONS ---

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Header
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(col_labels)) # column labels
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    # Returns a list of valid column indices (not full)
    return [c for c in range(len(board[0])) if board[0][c] == ' ']

def get_user_move(player_name, board):
    valid_columns = get_valid_columns(board)
    cols = len(board[0])
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        move = input(f"Player {player_name}, please enter a column: ").strip().upper()
        if len(move) != 1 or move not in col_labels:
            print("Invalid input. Enter a letter corresponding to a column (e.g. A-G).")
            continue
        col = col_labels.index(move)
        if col not in valid_columns:
            print("That column is full, you lose your turn.")
            return None # Lose turn if column is full
        return col

def place_checker(board, col, symbol):
    # Place checker in the lowest empty row of the column
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col
    return None

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def check_four(board, start_r, start_c, delta_r, delta_c, symbol):
    count = 0
    r, c = start_r, start_c
    while 0 <= r < len(board) and 0 <= c < len(board[0]):
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += delta_r
        c += delta_c
    return False

def check_win(board, symbol):
    rows, cols = len(board), len(board[0])
    # Check horizontal and vertical
    for r in range(rows):
        if check_four(board, r, 0, 0, 1, symbol):  # horizontal
            return True
    for c in range(cols):
        if check_four(board, 0, c, 1, 0, symbol):  # vertical
            return True
    # Diagonals (down-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == symbol for i in range(WIN_LENGTH)):
                return True
    # Diagonals (down-left)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, cols):
            if all(board[r + i][c - i] == symbol for i in range(WIN_LENGTH)):
                return True
    return False

# --- MAIN GAME LOOP ---
def main():
    board = create_board(ROWS, COLS)
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    while True:
        player_symbol = symbols[current]
        col = get_user_move(player_symbol, board)
        if col is None:
            # Lose turn if column is full
            current = (current + 1) % NUM_PLAYERS
            continue
        place_checker(board, col, player_symbol)
        clear_screen()
        print_board(board)
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
