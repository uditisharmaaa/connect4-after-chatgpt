import os
import random
import string

# ---- Constants ----
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # as per submission instructions

# ---- Board Initialization ----
def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = '  ' + '   '.join(string.ascii_uppercase[:len(board[0])])
    print(col_labels)
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+' + '---+' * len(board[0]))

# ---- Input & Game Mechanics ----
def get_valid_column(board):
    while True:
        inp = input("Please enter a column: ").upper()
        if len(inp) == 1 and inp in string.ascii_uppercase[:len(board[0])]:
            col = ord(inp) - ord('A')
            if board[0][col] == ' ':
                return col
            else:
                print("Column is full. You lose your turn.")
                return None  # Lose turn if column is full
        else:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col, symbol):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col

def check_win(board, symbol):
    rows, cols = len(board), len(board[0])
    # Horizontal & Vertical & Diagonal
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            # Horizontal
            if c + 3 < cols and all(board[r][c+i] == symbol for i in range(4)):
                return True
            # Vertical
            if r + 3 < rows and all(board[r+i][c] == symbol for i in range(4)):
                return True
            # Diagonal /
            if r + 3 < rows and c - 3 >= 0 and all(board[r+i][c-i] == symbol for i in range(4)):
                return True
            # Diagonal \
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == symbol for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for cell in board[0])

# ---- Game Loop ----
def main():
    board = create_board(ROWS, COLUMNS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    player = random.randint(0, NUM_PLAYERS-1)
    print_board(board)
    while True:
        print(f"Player {player_symbols[player]}, ", end='')
        col = get_valid_column(board)
        if col is None:  # Column full; lose turn
            player = (player + 1) % NUM_PLAYERS
            continue
        row, _ = drop_checker(board, col, player_symbols[player])
        print_board(board)
        if check_win(board, player_symbols[player]):
            print(f"Player {player_symbols[player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        player = (player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
