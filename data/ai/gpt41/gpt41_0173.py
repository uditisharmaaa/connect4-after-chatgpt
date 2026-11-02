import os
import random

# --- Constants ---
ROWS = 6
COLUMNS = 7   # Max: 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

# --- Functions ---
def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_column(column):
    return column in COLUMN_LABELS

def is_column_full(board, col_idx):
    return board[0][col_idx] != " "

def drop_checker(board, col_idx, checker):
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # Column full

def check_winner(board, checker):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def get_player_input(board, player_checker):
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not (len(move) == 1 and move.isalpha()):
            print("Invalid input! Please enter a single letter A-{0}.".format(COLUMN_LABELS[-1]))
            continue
        if not is_valid_column(move):
            print("Invalid column! Please enter a letter A-{0}.".format(COLUMN_LABELS[-1]))
            continue
        col_idx = COLUMN_LABELS.index(move)
        if is_column_full(board, col_idx):
            print("That column is full! You lose your turn.")
            return None
        return col_idx

# --- Main Game Loop ---
def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)

    while True:
        player = players[current]
        col_idx = get_player_input(board, player)
        # Skip turn if column is full
        if col_idx is None:
            current = (current + 1) % NUM_PLAYERS
            continue

        rowcol = drop_checker(board, col_idx, player)
        clear_screen()
        print_board(board)

        if check_winner(board, player):
            print(f"Player {player} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
