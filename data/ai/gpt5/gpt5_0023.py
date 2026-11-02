import os
import random
import sys

# Constants (changeable for different configurations, but keep within constraints)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Checker symbols (must be in order as specified)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A.. up to number of columns (max 26)
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board, labels):
    # Header
    print('  ' + '   '.join(labels))
    # Separator
    sep = '+' + '---+' * len(labels)
    for r in range(len(board)):
        print(sep)
        row_cells = board[r]
        row_line = '|'
        for cell in row_cells:
            row_line += f' {cell} |'
        print(row_line)
    print(sep)


def is_valid_column_input(s, max_cols):
    if len(s) != 1:
        return False
    ch = s.upper()
    if not ('A' <= ch <= 'Z'):
        return False
    idx = ord(ch) - ord('A')
    return 0 <= idx < max_cols


def input_column(labels, max_cols, player_symbol):
    while True:
        user_in = input(f'Player {player_symbol}, please enter a column: ').strip().upper()
        if not is_valid_column_input(user_in, max_cols):
            last_label = labels[-1]
            print(f'Invalid input. Please enter a column letter between A and {last_label}.')
            continue
        return ord(user_in) - ord('A')


def place_checker(board, col_index, symbol):
    # Place at the lowest available row (from bottom up)
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = symbol
            return r
    return None  # Column full


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, diag down-right, diag down-left
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in dirs:
                end_r = r + dr * 3
                end_c = c + dc * 3
                if 0 <= end_r < rows and 0 <= end_c < cols:
                    win = True
                    for k in range(1, 4):
                        rr = r + dr * k
                        cc = c + dc * k
                        if board[rr][cc] != symbol:
                            win = False
                            break
                    if win:
                        return True
    return False


def is_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def validate_settings(rows, cols, num_players):
    if not (2 <= num_players <= 5):
        print('Error: NUM_PLAYERS must be between 2 and 5.', file=sys.stderr)
        sys.exit(1)
    if cols < 1 or cols > 26:
        print('Error: COLS must be between 1 and 26.', file=sys.stderr)
        sys.exit(1)
    if rows < 1:
        print('Error: ROWS must be at least 1.', file=sys.stderr)
        sys.exit(1)


def main():
    validate_settings(ROWS, COLS, NUM_PLAYERS)

    # Initialize
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    labels = column_labels(COLS)
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial board print
    clear_screen()
    print_board(board, labels)

    while True:
        player_symbol = players[current_idx]

        # Prompt for move (board shown before prompt)
        col_idx = input_column(labels, COLS, player_symbol)

        # Attempt to place checker
        placed_row = place_checker(board, col_idx, player_symbol)

        if placed_row is None:
            # Column full: turn lost
            clear_screen()
            print_board(board, labels)
            print(f'Column {labels[col_idx]} is full. Turn lost.')
            # Next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # Check for win or draw after a valid placement
        if check_win(board, player_symbol):
            clear_screen()
            print_board(board, labels)
            print(f'Player {player_symbol} won!')
            break

        if is_draw(board):
            clear_screen()
            print_board(board, labels)
            print("It's a draw!")
            break

        # Next player's turn
        clear_screen()
        print_board(board, labels)
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == '__main__':
    main()
