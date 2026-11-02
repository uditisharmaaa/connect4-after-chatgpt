import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # can be set to 2-5 for other assignments
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    separator = '+' + '---+' * cols
    print(header)
    for row in board:
        print(separator)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(separator)

def get_valid_column_input(board, player_symbol):
    cols = len(board[0])
    col_labels = string.ascii_uppercase[:cols]
    while True:
        inp = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in col_labels:
            print("Invalid column. Try again.")
            continue
        col = col_labels.index(inp)
        if board[0][col] != ' ':
            print("Column is full. Turn lost.")
            return None  # Lose turn if column is full
        return col

def make_move(board, col, player_symbol):
    for r in reversed(range(len(board))):
        if board[r][col] == ' ':
            board[r][col] = player_symbol
            return r, col
    return None  # Shouldn't happen since we check before

def check_win(board, player_symbol):
    rows, cols = len(board), len(board[0])
    # Horizontal, Vertical, Diagonal /
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != player_symbol:
                continue
            # Horizontal
            if c + WIN_LENGTH <= cols and all(board[r][c+i] == player_symbol for i in range(WIN_LENGTH)):
                return True
            # Vertical
            if r + WIN_LENGTH <= rows and all(board[r+i][c] == player_symbol for i in range(WIN_LENGTH)):
                return True
            # Diagonal \
            if c + WIN_LENGTH <= cols and r + WIN_LENGTH <= rows and \
                all(board[r+i][c+i] == player_symbol for i in range(WIN_LENGTH)):
                return True
            # Diagonal /
            if c - WIN_LENGTH + 1 >= 0 and r + WIN_LENGTH <= rows and \
                all(board[r+i][c-i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS-1)
    clear_screen()
    print_board(board)
    while True:
        symbol = PLAYER_SYMBOLS[current_player]
        col = get_valid_column_input(board, symbol)
        if col is not None:
            row, _ = make_move(board, col, symbol)
        clear_screen()
        print_board(board)

        if col is not None and check_win(board, symbol):
            print(f"Player {symbol} won!")
            break
        if board_full(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
