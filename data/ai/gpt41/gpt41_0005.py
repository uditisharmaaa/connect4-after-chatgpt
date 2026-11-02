import os
import random
import string

# === Constants ===
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change as needed (2-5 allowed)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_LEN = 4

# === Board Functions ===
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(string.ascii_uppercase[:COLS])
    print(header)
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

# === Logic Functions ===
def is_valid_column(col_input):
    if len(col_input) == 1 and col_input in string.ascii_uppercase[:COLS]:
        return True
    return False

def get_column_idx(col_input):
    return string.ascii_uppercase.index(col_input)

def place_checker(board, col, symbol):
    # Place checker in column; True if placed, False if column full
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = symbol
            return True
    return False

def column_full(board, col):
    return board[0][col] != ' '

def board_full(board):
    return all(row[col] != ' ' for row in board for col in range(COLS))

def check_winner(board, symbol):
    # Horizontal, Vertical, Diagonals
    for row in range(ROWS):
        for col in range(COLS):
            if (col + WIN_LEN <= COLS and
                all(board[row][col + i] == symbol for i in range(WIN_LEN))):
                return True
            if (row + WIN_LEN <= ROWS and
                all(board[row + i][col] == symbol for i in range(WIN_LEN))):
                return True
            if (col + WIN_LEN <= COLS and row + WIN_LEN <= ROWS and
                all(board[row + i][col + i] == symbol for i in range(WIN_LEN))):
                return True
            if (col - WIN_LEN + 1 >= 0 and row + WIN_LEN <= ROWS and
                all(board[row + i][col - i] == symbol for i in range(WIN_LEN))):
                return True
    return False

# === Game Loop ===
def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {symbol}, please enter a column:")

        while True:
            col_input = input().strip().upper()
            if not is_valid_column(col_input):
                print("Invalid input. Please enter a valid column (A-{}):".format(string.ascii_uppercase[COLS-1]))
                continue

            col = get_column_idx(col_input)
            if column_full(board, col):
                print("Column full. You lose your turn.")
                break  # Lose turn
            else:
                place_checker(board, col, symbol)
                break

        print_board(board)

        # Check win
        if check_winner(board, symbol):
            print(f"Player {symbol} won!")
            break

        # Check draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
