import os
import random
import string
import sys

# Constants (Change dimensions and PLAYERS for different configuration)
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2  # between 2 and 5
CHECKERS_LIST = ['X', 'O', 'V', 'H', 'M']
CHECKERS = CHECKERS_LIST[:PLAYERS]

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    # Print column letters
    header = '  ' + '   '.join(string.ascii_uppercase[:columns])
    print(header)
    print('+' + '---+'*columns)
    for r in range(rows):
        row_str = '|'
        for c in range(columns):
            row_str += ' {} |'.format(board[r][c])
        print(row_str)
        print('+' + '---+'*columns)

def get_valid_columns(board):
    cols = []
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            cols.append(c)
    return cols

def get_player_input(board, player_checker):
    columns = len(board[0])
    valid_letters = string.ascii_uppercase[:columns]
    valid_columns = get_valid_columns(board)
    col = -1
    while True:
        user_in = input(f'Player {player_checker}, please enter a column: ').strip().upper()
        if len(user_in) != 1 or user_in not in valid_letters:
            print(f'Invalid input. Please enter a letter from A to {valid_letters[-1]}.')
            continue
        col = ord(user_in) - ord('A')
        if col < 0 or col >= columns:
            print(f'Column out of range. Please enter from A to {valid_letters[-1]}.')
            continue
        if col not in valid_columns:
            print('Column is full. Your turn is lost.')
            return None # lose the turn for filled columns
        break
    return col

def drop_checker(board, col, checker):
    rows = len(board)
    for r in range(rows-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col
    return None

def check_for_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    in_row = 4
    # Horizontal
    for r in range(rows):
        for c in range(cols - in_row + 1):
            if all(board[r][c+i] == checker for i in range(in_row)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - in_row + 1):
            if all(board[r+i][c] == checker for i in range(in_row)):
                return True
    # Diagonal \
    for r in range(rows - in_row + 1):
        for c in range(cols - in_row + 1):
            if all(board[r+i][c+i] == checker for i in range(in_row)):
                return True
    # Diagonal /
    for r in range(in_row-1, rows):
        for c in range(cols - in_row + 1):
            if all(board[r-i][c+i] == checker for i in range(in_row)):
                return True
    return False

def check_for_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    # Input validation for constants
    if not (2 <= PLAYERS <= 5):
        print("Number of PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLUMNS <= MAX_COLUMNS):
        print(f"Number of columns must be between 1 and {MAX_COLUMNS}.")
        return

    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    print(f"Randomly selected Player {CHECKERS[current_player]} to start.")

    while True:
        print_board(board)
        player_checker = CHECKERS[current_player]
        col = get_player_input(board, player_checker)
        if col is not None:
            # place checker and get row, col
            loc = drop_checker(board, col, player_checker)
            if loc:
                if check_for_win(board, player_checker):
                    print_board(board)
                    print(f"Player {player_checker} won!")
                    break
                if check_for_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    break
            else:
                # Should not happen due to input validation, but just in case
                print("Column is full. Turn lost.")
        # Invalid column or full column: skip to next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
