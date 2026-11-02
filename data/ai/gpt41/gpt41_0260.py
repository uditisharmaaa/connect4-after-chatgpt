import random
import os
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
BLANK = ' '

def clear_screen():
    os.system('clear')  # Or 'cls' for Windows

def create_board(rows=NUM_ROWS, cols=NUM_COLS):
    return [[BLANK for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column letters
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join([' {} '.format(cell) for cell in row]) + '|')
        print('+' + '---+' * cols)

def get_checkers(num_players):
    return CHECKERS[:num_players]

def get_valid_columns(board):
    cols = len(board[0])
    valids = []
    for c in range(cols):
        if board[0][c] == BLANK:
            valids.append(c)
    return valids

def column_from_letter(letter):
    if letter.upper() in string.ascii_uppercase:
        return ord(letter.upper()) - ord('A')
    else:
        return -1

def is_valid_column(col_letter, board):
    col_index = column_from_letter(col_letter)
    cols = len(board[0])
    if col_index < 0 or col_index >= cols:
        return False
    if board[0][col_index] != BLANK:
        return False
    return True

def place_checker(board, col, checker):
    # Place checker in lowest empty row in column
    for row in reversed(range(len(board))):
        if board[row][col] == BLANK:
            board[row][col] = checker
            return row, col
    return None, None

def is_board_full(board):
    return all(cell != BLANK for cell in board[0])

def win_direction(board, checker, row, col, delta_row, delta_col):
    count = 0
    n = len(board)
    m = len(board[0])
    r, c = row, col
    while 0 <= r < n and 0 <= c < m and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col

    r, c = row - delta_row, col - delta_col
    while 0 <= r < n and 0 <= c < m and board[r][c] == checker:
        count += 1
        r -= delta_row
        c -= delta_col

    return count >= 4

def check_win(board, checker, row, col):
    # 4 directions: Horizontal, Vertical, Diagonal /
    directions = [
        (0, 1),  # Right/Left
        (1, 0),  # Down/Up
        (1, 1),  # Diagonal Down-Right / Up-Left
        (1, -1)  # Diagonal Down-Left / Up-Right
    ]
    for dr, dc in directions:
        if win_direction(board, checker, row, col, dr, dc):
            return True
    return False

def prompt_column(player, valid_cols, board):
    while True:
        user_input = input(f"Player {player}, please enter a column: ").strip()
        if len(user_input) != 1 or user_input.upper() not in string.ascii_uppercase:
            print("Invalid input! Enter a single uppercase letter (A-{0}).".format(
                chr(ord('A')+len(board[0])-1)))
            continue
        col = column_from_letter(user_input)
        if col not in range(len(board[0])):
            print(f"Column {user_input} is out of range!")
            continue
        if board[0][col] != BLANK:
            print(f"Column {user_input} is full! Choose another.")
            continue
        return col

def main():
    # Initialization
    board = create_board(NUM_ROWS, NUM_COLS)
    checkers = get_checkers(NUM_PLAYERS)
    player_names = [c for c in checkers]
    player_num = random.randint(0, NUM_PLAYERS - 1)  # Random player
    clear_screen()
    print_board(board)

    moves = 0
    while True:
        cur_checker = checkers[player_num]
        available = get_valid_columns(board)
        if not available:
            print("It's a draw!")
            break

        col = prompt_column(cur_checker, available, board)
        row, col_placed = place_checker(board, col, cur_checker)
        moves += 1

        clear_screen()
        print_board(board)
        if check_win(board, cur_checker, row, col_placed):
            print(f"Player {cur_checker} won!")
            break

        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player
        player_num = (player_num + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
