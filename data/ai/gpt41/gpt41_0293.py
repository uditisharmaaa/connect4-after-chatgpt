import random
import os

# ---- Constants ----
ROWS = 6
COLS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# ---- Game Functions ----

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    col_labels = '  ' + '   '.join(ALPHABET[:len(board[0])])
    line = '+' + ('---+' * len(board[0]))
    print(col_labels)
    for row in board:
        print(line)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(line)

def get_valid_column(input_col, cols):
    if len(input_col) != 1 or input_col.upper() not in ALPHABET[:cols]:
        return None
    return ALPHABET.index(input_col.upper())

def is_column_full(board, col):
    return all(row[col] != ' ' for row in board)

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Should not occur if checked before

def check_win(board, checker):
    rows, cols = len(board), len(board[0])
    # Horizontal
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal (downward)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal (upward)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# ---- Main Game Loop ----

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYER_COUNT]
    current_player = random.randint(0, PLAYER_COUNT - 1)
    clear_screen()
    print_board(board)
    while True:
        checker = players[current_player]
        print(f"Player {checker}, please enter a column:")
        valid_input = False
        while not valid_input:
            col_input = input().strip()
            col = get_valid_column(col_input, COLS)
            if col is None:
                print("Invalid input. Please enter a valid column letter (A-G).")
                continue
            if is_column_full(board, col):
                print("Column is full, turn is lost.")
                valid_input = True  # Lose turn if full column
                break
            place_checker(board, col, checker)
            valid_input = True
        clear_screen()
        print_board(board)
        # Win check
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        # Move to next player
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == '__main__':
    main()
