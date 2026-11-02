import os
import random
import string

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLUMNS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column headers (A, B, C, ...)
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))
    # Board
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(sep)

def get_valid_column_input(valid_cols, current_checker):
    # Keep asking until a syntactically valid column letter is provided (A..)
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if user_input not in valid_cols:
            print("Invalid column. Please enter one of: " + ", ".join(valid_cols))
            continue
        return user_input

def drop_checker(board, col_index, checker):
    # Place checker in the lowest available row in the given column.
    # Returns the row index where placed, or None if column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return None

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
                        count += 1
                    else:
                        break
                if count == 4:
                    return True
    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Basic validations for configuration
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLUMNS < 1 or COLUMNS > 26:
        print("COLUMNS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLUMNS)
    valid_cols = [string.ascii_uppercase[i] for i in range(COLUMNS)]

    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    clear_screen()
    print_board(board)

    while True:
        current_checker = players[current_player_index]

        # Get a valid column letter (A..)
        col_letter = get_valid_column_input(valid_cols, current_checker)
        col_index = ord(col_letter) - ord('A')

        # Attempt to drop checker
        placed_row = drop_checker(board, col_index, current_checker)

        # Clear and print updated board each turn
        clear_screen()
        print_board(board)

        if placed_row is None:
            # Column is full: player loses the turn
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
        else:
            # Check for win
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            # Check for draw
            if check_draw(board):
                print("The game is a draw.")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
