import os
import random
import string

# === Constants ===
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # For submission: set to 2

# === Functions ===

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_valid_columns(board):
    return [i for i in range(len(board[0])) if board[0][i] == ' ']

def get_column_input(board):
    valid_cols = get_valid_columns(board)
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    while True:
        inp = input().strip().upper()
        if len(inp) != 1 or inp not in col_labels:
            print("Invalid input. Please enter a valid column letter.")
            continue
        idx = col_labels.index(inp)
        if idx not in valid_cols:
            print("Column full! You lose your turn.")
            return None  # Caller will handle turn skip for full columns
        return idx

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return board.index(row), col

def check_win(board, last_row, last_col, checker):
    directions = [
        (0, 1), (1, 0), (1, 1), (1, -1)  # horiz, vert, diag down, diag up
    ]
    for dr, dc in directions:
        count = 1
        # Forward dir
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Backward dir
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

# === Main Game ===

def main():
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        print(f"Player {players[current]}, please enter a column:")
        col = get_column_input(board)
        if col is None:  # Full column, lose turn
            current = (current + 1) % NUM_PLAYERS
            continue
        row, _ = place_checker(board, col, players[current])
        if check_win(board, row, col, players[current]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current]} won!")
            game_over = True
        elif is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
