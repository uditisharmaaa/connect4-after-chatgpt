import os
import random
import sys

# ------------------- CONSTANTS -------------------
ROWS = 6  # Number of rows in the board
COLUMNS = 7  # Number of columns in the board (max 26)
NUM_PLAYERS = 2  # Number of players (2 to 5 allowed)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for each player
WIN_COUNT = 4  # How many checkers in a row needed to win
MAX_COLUMNS = 26  # Maximum columns (A-Z)

# ------------- UTILITY FUNCTIONS -----------------

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    cols = []
    for col in range(len(board[0])):
        if board[0][col] == " ":  # If the top cell is empty, it's a valid column
            cols.append(col)
    return cols

def input_column(board, player_checker):
    cols = len(board[0])
    letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in letters:
            print(f"Invalid input. Please enter one of these letters: {', '.join(letters)}")
            continue
        col_index = ord(col_input) - ord('A')
        if board[0][col_index] != " ":
            print(f"Column {col_input} is full. Turn lost.")
            return None  # Return None if column full (turn lost)
        return col_index

def drop_checker(board, col, checker):
    rows = len(board)
    # Start from bottom row and go up to find first empty slot
    for row in reversed(range(rows)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col  # Return the location where placed
    return None  # Should not happen if checked for valid column earlier

def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Count including current checker
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def get_next_player(curr, num_players):
    return (curr + 1) % num_players

# ------------------- MAIN GAME -------------------

def main():
    if COLUMNS > MAX_COLUMNS or COLUMNS < 1:
        print(f"Number of columns must be between 1 and {MAX_COLUMNS}.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        sys.exit(1)

    board = create_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly choose starting player
    current = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {player_checkers[current]} starts first!")
    input("Press Enter to begin...")

    winner = None
    while True:
        print_board(board)
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            print("It's a draw!")
            break
        player_symbol = player_checkers[current]
        col = input_column(board, player_symbol)
        if col is None:  # If column full, lose the turn
            current = get_next_player(current, NUM_PLAYERS)
            continue
        row, _ = drop_checker(board, col, player_symbol)
        if check_win(board, row, col, player_symbol):
            print_board(board)
            print(f"Player {player_symbol} won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current = get_next_player(current, NUM_PLAYERS)

if __name__ == "__main__":
    main()
