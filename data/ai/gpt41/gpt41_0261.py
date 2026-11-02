import os
import random
import string

# --- Constants (change as needed; for submission set rows=6, cols=7, num_players=2) ---
ROWS = 6
COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# --- Helper Functions ---
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    os.system('clear')
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    return [i for i in range(len(board[0])) if board[0][i] == " "]

def input_column(valid_cols, cols):
    while True:
        user = input("Please enter a column: ").strip().upper()
        if len(user) != 1 or user not in string.ascii_uppercase[:cols]:
            print("Invalid input. Enter a letter between A and", string.ascii_uppercase[cols-1])
            continue
        col = string.ascii_uppercase.index(user)
        if col not in valid_cols:
            print("Column is full or invalid. Choose another one.")
            continue
        return col

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return board.index(row)
    return None

# --- Win Checking ---
def check_winner(board, row, col, checker):
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1, -1]:
            r, c = row, col
            while True:
                r += dr * d
                c += dc * d
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_full(board):
    return all(cell != " " for cell in board[0])

# --- Game Loop ---
def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)

    print_board(board, COLS)
    print(f"Player {players[current]} will start!\n")

    while True:
        print_board(board, COLS)
        print(f"Player {players[current]}, ", end="")
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("Game is a draw!")
            break
        col = input_column(valid_cols, COLS)
        row = drop_checker(board, col, players[current])
        if row is not None and check_winner(board, row, col, players[current]):
            print_board(board, COLS)
            print(f"Player {players[current]} won!")
            break
        elif is_full(board):
            print_board(board, COLS)
            print("Game is a draw!")
            break
        # Next player's turn
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
