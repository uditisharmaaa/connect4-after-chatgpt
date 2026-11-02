import os
import random
import string

# === CONFIGURABLE CONSTANTS ===
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2-5

PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    col_labels = ' '.join(f'  {c} ' for c in string.ascii_uppercase[:COLS])
    sep_line = '+' + ('---+' * COLS)
    print(col_labels)
    for row in board:
        print(sep_line)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(sep_line)

def get_valid_input(board):
    valid_cols = [string.ascii_uppercase[i] for i in range(COLS)]
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in valid_cols:
            print("Invalid column. Try again.")
            continue
        col_idx = valid_cols.index(col_input)
        if board[0][col_idx] != ' ':
            print("That column is full. You lose your turn!")
            return None  # according to assignment, lose turn
        return col_idx

def place_checker(board, col, token):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = token
            return row, col
    return None  # should not happen if checked before

def check_line(line, token):
    count = 0
    for c in line:
        if c == token:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_win(board, token):
    # HORIZONTAL
    for row in board:
        if check_line(row, token):
            return True
    # VERTICAL
    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        if check_line(col, token):
            return True
    # DIAGONAL (bottom-left to top-right)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == token:
                # Down-right diagonal
                try:
                    if all(board[r + i][c + i] == token for i in range(4)):
                        return True
                except IndexError:
                    pass
                # Down-left diagonal
                try:
                    if all(r + i < ROWS and c - i >= 0 and board[r + i][c - i] == token for i in range(4)):
                        return True
                except IndexError:
                    pass
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    current = random.randrange(NUM_PLAYERS)
    clear_screen()
    print_board(board)
    while True:
        player_token = tokens[current]
        print(f"Player {player_token}, ", end='')
        col_idx = get_valid_input(board)
        if col_idx is None:
            current = (current + 1) % NUM_PLAYERS
            continue

        place_checker(board, col_idx, player_token)
        clear_screen()
        print_board(board)

        if check_win(board, player_token):
            print(f"Player {player_token} won!")
            break
        if is_draw(board):
            print("Game is a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
