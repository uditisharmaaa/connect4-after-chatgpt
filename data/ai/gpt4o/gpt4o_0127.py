import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2

CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(65 + i) for i in range(COLUMNS)]  # ['A', 'B', 'C', ...]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def is_valid_column(col_input):
    return col_input in COLUMN_LABELS

def is_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] == checker:
                return True
    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == checker:
                return True
    # Check diagonal ascending
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == checker:
                return True
    # Check diagonal descending
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == checker:
                return True
    return False

def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        
        col_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid column input, try again.")
            continue
            
        col = COLUMN_LABELS.index(col_input)
        row = get_next_open_row(board, col)
        
        if row is None:
            print("Column is full, you lose your turn.")
        else:
            board[row][col] = current_checker
            print_board(board)
            
            if is_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            if is_draw(board):
                print("It's a draw!")
                break
            
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
