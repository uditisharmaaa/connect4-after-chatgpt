import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

def is_valid_column(column_char):
    return column_char in COLUMN_LABELS

def column_index(column_char):
    return ord(column_char) - ord('A')

def is_column_full(board, col_idx):
    return board[0][col_idx] != ' '

def place_checker(board, col_idx, checker):
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # column full

def check_win(board, checker, row, col):
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down right
        (1, -1)   # diagonal down left
    ]

    for dr, dc in directions:
        count = 1

        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False

def is_draw(board):
    # Draw if no empty spaces in top row
    return all(cell != ' ' for cell in board[0])

def get_player_input(current_checker):
    while True:
        inp = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            continue
        if not is_valid_column(inp):
            continue
        col_idx = column_index(inp)
        return col_idx

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = players[current_player_idx]

        col_idx = get_player_input(current_checker)

        if is_column_full(board, col_idx):
            # column full: lose turn, but print board and continue to next player
            print_board(board)
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        row_idx, col_idx_place = place_checker(board, col_idx, current_checker)
        print_board(board)

        if check_win(board, current_checker, row_idx, col_idx_place):
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
