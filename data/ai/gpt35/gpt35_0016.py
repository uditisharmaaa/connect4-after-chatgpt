import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # can be from 2 to 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LABELS = string.ascii_uppercase[:COLS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board with separators
    line_sep = "+" + "---+"*COLS
    for row in board:
        print(line_sep)
        print("| " + " | ".join(row) + " |")
    print(line_sep)

def is_valid_column(col_char):
    return col_char in COLUMN_LABELS

def get_column_index(col_char):
    return COLUMN_LABELS.index(col_char)

def column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # place checker in lowest empty cell in column col_idx
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # Column full
    return None, None

def check_win(board, checker, last_row, last_col):
    # Directions: (row_delta, col_delta)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def next_player_index(current_idx):
    return (current_idx + 1) % PLAYERS

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_idx]
        # Prompt until valid input (if column full, turn lost)
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if (len(user_input) == 1 and is_valid_column(user_input)):
                col_idx = get_column_index(user_input)
                if column_full(board, col_idx):
                    # Column full - turn lost
                    valid_input = True
                    placed_row = None
                    placed_col = None
                else:
                    placed_row, placed_col = place_checker(board, col_idx, current_checker)
                    valid_input = True
            else:
                # Invalid input, ask again
                continue
        
        print_board(board)
        
        # If checker was placed, check win
        if placed_row is not None and placed_col is not None:
            if check_win(board, current_checker, placed_row, placed_col):
                print(f"Player {current_checker} won!")
                break
            if board_full(board):
                print("The game is a draw.")
                break
        # If checker was not placed (column full), turn lost; just next player
        current_player_idx = next_player_index(current_player_idx)

if __name__ == "__main__":
    main()
