import os
import random
import string

# --------- Constants -----------
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2   # Set to 2 for submission; can be 2-5
CONNECT_N = 4
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])

# --------- Functions -----------

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    print(" ", end="")
    for col in COLUMN_LABELS:
        print(f" {col} ", end="")
    print()
    # Print rows
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * COLUMNS)

def get_valid_column(board, prompt):
    while True:
        col_in = input(prompt).strip().upper()
        if len(col_in) != 1 or col_in not in COLUMN_LABELS:
            print(f"Invalid input. Please enter a column (A-{COLUMN_LABELS[-1]}).")
            continue
        col_idx = COLUMN_LABELS.index(col_in)
        # Check if the column is full
        if board[0][col_idx] != " ":
            print("Column is full. You lose your turn!")
            return None
        return col_idx

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return board.index(row)  # Return row index
    return None  # Should not happen; column full check before

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down right
        (1, -1),  # Diagonal down left
    ]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row, col
            while True:
                r += dr * step
                c += dc * step
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= CONNECT_N:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    while True:
        checker = players[current]
        prompt = f"Player {checker}, please enter a column: "
        col = get_valid_column(board, prompt)
        clear_screen()
        if col is None:
            print_board(board)
            current = (current + 1) % NUM_PLAYERS
            continue
        row = place_checker(board, col, checker)
        print_board(board)
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
