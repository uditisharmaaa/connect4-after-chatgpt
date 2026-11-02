import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = 2  # Only 2 for submission (can be up to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    col_labels = '  ' + '   '.join(string.ascii_uppercase[:cols])
    sep = '+' + '---+' * cols
    clear_screen()
    print(col_labels)
    for row in board:
        print(sep)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(sep)

def get_valid_input(prompt, cols):
    valid_cols = set(string.ascii_uppercase[:cols])
    while True:
        col = input(prompt).upper()
        if len(col) != 1 or col not in valid_cols:
            print(f"Invalid input. Please enter a letter A-{string.ascii_uppercase[cols-1]}.")
            continue
        return string.ascii_uppercase.index(col)

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column full

def board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def win_check(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue
            # Horizontal
            if c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4)):
                return True
            # Vertical
            if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                return True
            # Diagonal /
            if r <= ROWS - 4 and c >= 3 and all(board[r + i][c - i] == checker for i in range(4)):
                return True
            # Diagonal \
            if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4)):
                return True
    return False

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS - 1)
    print_board(board, COLS)
    print(f"Player {players[current]} starts!")
    input("Press Enter to begin...")
    while True:
        print_board(board, COLS)
        player = players[current]
        col = get_valid_input(f"Player {player}, please enter a column: ", COLS)
        if not place_checker(board, col, player):
            print("Column full! Turn lost.")
        else:
            if win_check(board, player):
                print_board(board, COLS)
                print(f"Player {player} won!")
                break
            if board_full(board):
                print_board(board, COLS)
                print("Game is a draw!")
                break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
