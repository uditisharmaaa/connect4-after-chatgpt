import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

def get_valid_column(board, input_col):
    if len(input_col) != 1 or input_col not in COLUMN_LABELS:
        return None
    col = COLUMN_LABELS.index(input_col)
    if board[0][col] != ' ':
        return None
    return col

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return board.index(row)
    return None

def is_winner(board, checker):
    # Horizontal, vertical, diagonal checks
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] != checker:
                continue
            # horiz
            if c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4)):
                return True
            # vert
            if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                return True
            # diag down right
            if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4)):
                return True
            # diag up right
            if r - 3 >= 0 and c + 3 < COLUMNS and all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0]) # top row filled

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        print(f'Player {checker}, please enter a column:')
        col = None

        while col is None:
            usr_input = input().strip().upper()
            col = get_valid_column(board, usr_input)
            if col is None:
                print('Invalid column. Try again:')

        row_placed = drop_checker(board, col, checker)
        print_board(board)

        if is_winner(board, checker):
            print(f'Player {checker} won!')
            break
        if is_draw(board):
            print('The game is a draw!')
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
