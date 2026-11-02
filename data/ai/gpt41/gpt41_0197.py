import os
import random

# === Constants (You can change these for flexible sizes/players) ===
ROWS = 6
COLUMNS = 7  # max 26!
NUM_PLAYERS = 2  # between 2 and 5
PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COL_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

# === Functions ===
def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COL_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def valid_column(col_str):
    return len(col_str) == 1 and col_str in COL_LABELS

def get_column_index(col_str):
    return COL_LABELS.index(col_str)

def col_full(board, col):
    return all(board[row][col] != ' ' for row in range(ROWS))

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Should not happen if checked with col_full()

def input_column(player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if not valid_column(col_input):
            print("Invalid input! Please enter a valid column letter.")
            continue
        col = get_column_index(col_input)
        if col_full(board, col):
            print("That column is full! You lose your turn.")
            return None
        return col

def in_bounds(row, col):
    return 0 <= row < ROWS and 0 <= col < COLUMNS

def check_win(board, checker):
    # Horizontal, Vertical, Diagonal (2)
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] != checker:
                continue
            # Directions: right, down, down-right, down-left
            for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
                count = 1
                for k in range(1, 4):
                    nr, nc = row + dr*k, col + dc*k
                    if in_bounds(nr, nc) and board[nr][nc] == checker:
                        count += 1
                    else:
                        break
                if count == 4:
                    return True
    return False

def board_full(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# === Main Game ===
if __name__ == "__main__":
    board = create_board()
    current = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    while True:
        player = PLAYER_CHARS[current]
        col = input_column(player)
        if col is None:
            # Column full: player loses turn, per assignment description
            current = (current + 1) % NUM_PLAYERS
            continue
        row, _ = place_checker(board, col, player)
        print_board(board)
        if check_win(board, player):
            print(f"Player {player} won!")
            break
        if board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS
