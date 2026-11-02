import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Can support up to 5 players

# Board Initialization
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    cols = len(board[0])
    # Print column headers
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(cols)])
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    return [i for i in range(len(board[0])) if board[0][i] == " "]

def letter_to_col(letter):
    if letter in string.ascii_uppercase:
        return ord(letter) - ord('A')
    return -1

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def is_full(board):
    return all(cell != " " for cell in board[0])

def check_winner(board, checker):
    rows, cols = len(board), len(board[0])
    win_len = 4
    
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Horizontal
            if c <= cols - win_len and all(board[r][c + i] == checker for i in range(win_len)):
                return True
            # Vertical
            if r <= rows - win_len and all(board[r + i][c] == checker for i in range(win_len)):
                return True
            # Diagonal Down-Right
            if r <= rows - win_len and c <= cols - win_len and all(board[r + i][c + i] == checker for i in range(win_len)):
                return True
            # Diagonal Up-Right
            if r >= win_len - 1 and c <= cols - win_len and all(board[r - i][c + i] == checker for i in range(win_len)):
                return True
    return False

def main():
    board = create_board(ROWS, COLS)
    player_count = PLAYERS
    checkers = CHECKERS[:player_count]
    current_player = random.randint(0, player_count - 1)
    print_board(board)

    while True:
        col_labels = [chr(ord('A') + i) for i in range(COLS)]
        checker = checkers[current_player]
        valid_cols = get_valid_columns(board)

        # Input loop
        while True:
            inp = input(f"Player {checker}, please enter a column: ").strip().upper()
            if len(inp) == 1 and inp in col_labels:
                col = letter_to_col(inp)
                if col in valid_cols:
                    if place_checker(board, col, checker):
                        break
                else:
                    if col >= 0 and col < COLS:
                        print("Column is full; turn is lost.")
                        current_player = (current_player + 1) % player_count
                        break
                    else:
                        print("Invalid column.")
            else:
                print("Invalid input. Please enter a letter corresponding to a column.")

        print_board(board)
        # Check for win or draw
        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break
        if is_full(board):
            print("It's a draw!")
            break
        # Alternate player
        current_player = (current_player + 1) % player_count

if __name__ == "__main__":
    main()
