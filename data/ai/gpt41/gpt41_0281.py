import random
import os
import string

# Constants (can be modified to support other setups)
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # can be 2, 3, 4, or 5

# Player checker symbols in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Board labels (for up to 26 columns)
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" " for _ in range(cols)])
    return board

def print_board(board):
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_column(input_str):
    if len(input_str) != 1:
        return False
    if input_str not in COLUMN_LABELS:
        return False
    return True

def get_next_open_row(board, col):
    # Start from bottom row, find first open
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            return row
    return None  # Column is full

def check_win(board, checker):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if (board[r][c] == checker and
                board[r][c+1] == checker and
                board[r][c+2] == checker and
                board[r][c+3] == checker):
                return True

    # Check vertical locations
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if (board[r][c] == checker and
                board[r+1][c] == checker and
                board[r+2][c] == checker and
                board[r+3][c] == checker):
                return True

    # Check positive slope diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True

    # Check negative slope diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True

    return False

def is_board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {PLAYER_CHECKERS[current_player]}, please enter a column:")

        input_ok = False
        while not input_ok:
            col_input = input().strip().upper()
            if not is_valid_column(col_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            col_index = COLUMN_LABELS.index(col_input)
            row_index = get_next_open_row(board, col_index)
            if row_index is None:
                print("Column is full. You lose your turn.")
                input_ok = True # Mark input as ok, but skip to next player
                row_index = None
            else:
                input_ok = True

        # Only place checker if column is not full
        if row_index is not None:
            board[row_index][col_index] = PLAYER_CHECKERS[current_player]
            # Check for win
            if check_win(board, PLAYER_CHECKERS[current_player]):
                clear_screen()
                print_board(board)
                print(f"Player {PLAYER_CHECKERS[current_player]} won!")
                break

            # Check draw
            if is_board_full(board):
                clear_screen()
                print_board(board)
                print("Game is a draw!")
                break

        # Next player (skip if column was full)
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
