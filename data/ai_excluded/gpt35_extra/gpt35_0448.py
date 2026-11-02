import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Game settings (submission requires 2 players, 6x7 board)
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(headers))
    # Print horizontal border line
    line = "+" + "---+" * cols
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if col_char < 'A' or col_char >= chr(ord('A') + cols):
        return False
    return True

def column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col, checker):
    """
    Try to place the checker into the column.
    Checkers fall to the lowest empty row.
    Return True if placed, False if the column is full.
    """
    # Start from bottom row (ROWS-1) going upwards
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal (left to right)
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical (top to bottom)
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def input_column(player_checker, cols):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip()
        if not is_valid_column(inp, cols):
            # Invalid character or out of range column
            print("Invalid input. Please enter a valid uppercase letter within the board columns.")
            continue
        col = column_index(inp)
        return col

def main():
    board = create_board(ROWS, COLS)
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randrange(NUM_PLAYERS)
    print_board(board)
    # Initial player message
    # Loop until win or draw
    while True:
        player_checker = checkers[current_player_index]
        col = input_column(player_checker, COLS)
        placed = place_checker(board, col, player_checker)
        if not placed:
            # turn lost if column full
            print(f"Column {chr(ord('A')+col)} is full. Player {player_checker} loses a turn.")
        else:
            print_board(board)
            if check_winner(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            if board_full(board):
                print("The game is a draw.")
                break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
