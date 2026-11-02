import os
import random
import string

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Supported: 2 to 5
CONNECT_N = 4

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Header with column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    # Top border
    print('+' + '---+' * COLS)
    # Rows
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {cell} ' for cell in row_cells) + '|')
        print('+' + '---+' * COLS)


def get_valid_column_input():
    while True:
        user_in = input('Please enter a column: ').strip()
        if not user_in:
            print(f'Invalid input. Enter a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.')
            continue
        user_in = user_in.upper()
        if user_in in COLUMN_LABELS:
            return user_in
        print(f'Invalid input. Enter a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.')


def drop_checker(board, col_idx, symbol):
    # Start from bottom row upwards
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = symbol
            return r
    return None  # Column full


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board, symbol):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < CONNECT_N and in_bounds(nr, nc) and board[nr][nc] == symbol:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= CONNECT_N:
                    return True
    return False


def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True


def main():
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError('NUM_PLAYERS must be between 2 and 5.')
    if not (1 <= COLS <= 26):
        raise ValueError('COLS must be between 1 and 26.')

    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show initial empty board
    clear_screen()
    print_board(board)

    # Inform starting player
    print(f'Player {PLAYER_SYMBOLS[current_player_idx]} starts.')

    while True:
        symbol = PLAYER_SYMBOLS[current_player_idx]
        print(f'Player {symbol},', end=' ')
        col_label = get_valid_column_input()
        col_idx = COLUMN_LABELS.index(col_label)

        placed_row = drop_checker(board, col_idx, symbol)
        if placed_row is None:
            # Column full -> turn is invalid and the player loses the turn
            clear_screen()
            print_board(board)
            print(f'Column {col_label} is full. Player {symbol} loses the turn.')
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a valid move, check for win/draw
        if check_win(board, symbol):
            clear_screen()
            print_board(board)
            print(f'Player {symbol} won!')
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Prepare for next turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        clear_screen()
        print_board(board)


if __name__ == '__main__':
    main()
