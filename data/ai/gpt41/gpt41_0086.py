import os
import random

# CONSTANTS
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # To map columns to letters
CONNECT = 4
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # For submission; change if you want more players

COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    print("  ", end='')
    for label in COLUMN_LABELS[:len(board[0])]:
        print(f" {label}  ", end='')
    print()
    print("+" + "---+"*len(board[0]))
    # Print rows
    for row in board:
        print("|", end='')
        for cell in row:
            print(f" {cell} |", end='')
        print()
        print("+" + "---+"*len(board[0]))

def get_valid_column_input(board):
    while True:
        col_input = input(f"Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in COLUMN_LABELS[:len(board[0])]:
            print("Invalid input! Please enter a valid column letter.")
            continue
        col_index = ord(col_input) - ord('A')
        if board[0][col_index] != " ":
            print("That column is full. You lose your turn.")
            return None  # Indicates full column (turn lost)
        return col_index

def place_checker(board, col, symbol):
    # Start from bottom, place at first empty spot
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col
    return None, None  # Column is full, shouldn't be reached due to prior validation

def is_within_board(row, col, rows, columns):
    return 0 <= row < rows and 0 <= col < columns

def check_win(board, row, col, symbol):
    directions = [
        (0, 1),   # horizontal (right)
        (1, 0),   # vertical (down)
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1  # Count includes current position
        # Check forward direction
        r, c = row + dr, col + dc
        while is_within_board(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while is_within_board(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= CONNECT:
            return True
    return False

def check_draw(board):
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Random first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    
    winner = None

    while True:
        symbol = player_symbols[current_player]
        print(f"Player {symbol}, ", end="")
        col_index = get_valid_column_input(board)
        # Lose turn if column is full
        if col_index is None:
            current_player = (current_player + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        row_index, _ = place_checker(board, col_index, symbol)
        clear_screen()
        print_board(board)

        if check_win(board, row_index, col_index, symbol):
            print(f"Player {symbol} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
