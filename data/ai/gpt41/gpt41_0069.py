import os
import random
import string

# --- Constants ---
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # 2-5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Creation ---
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    col_labels = "  " + "   ".join(string.ascii_uppercase[:COLS])
    divider = "+" + "---+" * COLS
    print(col_labels)
    for row in board:
        print(divider)
        print("| " + " | ".join(row) + " |")
    print(divider)

# --- Game Logic ---
def get_move(board, player):
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        # Validate if it's a single uppercase letter in the valid range
        if len(col) != 1 or col not in string.ascii_uppercase[:COLS]:
            print("Invalid input! Please enter a valid column letter.")
            continue
        col_idx = string.ascii_uppercase.index(col)
        # Check if the column is full
        if board[0][col_idx] != " ":
            print("Column is full! You lose your turn.")
            return None  # turn lost
        return col_idx

def make_move(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None

def is_winner(board, checker):
    # Horizontal, vertical, and both diagonals
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue
            # Horizontal
            if c + 3 < COLS and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Vertical
            if r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Diagonal down-right
            if r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Diagonal up-right
            if r - 3 >= 0 and c + 3 < COLS and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    while True:
        checker = CHECKERS[player_idx]
        col_idx = get_move(board, checker)
        if col_idx is not None:
            make_move(board, col_idx, checker)
            print_board(board)
            if is_winner(board, checker):
                print(f"Player {checker} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break
        player_idx = (player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
