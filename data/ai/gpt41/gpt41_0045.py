import os
import random
import string

# === Constants ===
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2                # Set this to 2 for submission
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# === Board Functions ===
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, columns):
    os.system('clear')
    col_labels = '   '.join(string.ascii_uppercase[:columns])
    print(f"  {col_labels}")
    print('+' + '---+'*columns)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+'*columns)

# === Move and Validation ===
def get_column_input(columns):
    while True:
        col = input("Please enter a column: ").strip().upper()
        if len(col) == 1 and col in string.ascii_uppercase[:columns]:
            return ord(col) - ord('A')
        print("Invalid input. Please enter a valid column letter.")

def is_full(column, board):
    return board[0][column] != ' '

def place_checker(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return row
    return -1 # Should never get here if checked properly

# === Win/Draw Checking ===
def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLUMNS

def check_win(board, row, col, checker):
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]
    for dr, dc in directions:
        count = 1
        for step in (1, -1):
            r, c = row, col
            while True:
                r += dr * step
                c += dc * step
                if in_bounds(r, c) and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# === Main Game ===
def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    cur = random.randint(0, NUM_PLAYERS-1)
    print_board(board, COLUMNS)
    print(f"Player {players[cur]} starts!")
    while True:
        print_board(board, COLUMNS)
        print(f"Player {players[cur]},", end=' ')
        col = get_column_input(COLUMNS)
        if is_full(col, board):
            print("Column full! You lose your turn.")
        else:
            row = place_checker(board, col, players[cur])
            if check_win(board, row, col, players[cur]):
                print_board(board, COLUMNS)
                print(f"Player {players[cur]} won!")
                return
            if board_full(board):
                print_board(board, COLUMNS)
                print("It's a draw!")
                return
        cur = (cur + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
