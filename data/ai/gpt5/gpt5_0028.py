import os
import random
import string
import sys

# ---------------------- Configuration (constants) ----------------------
ROWS = 6
COLS = 7           # Max 26
NUM_PLAYERS = 2    # Between 2 and 5
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# ---------------------- Utility and Game Functions ----------------------
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    if cols > 26:
        cols = 26
    return [string.ascii_uppercase[i] for i in range(cols)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with column letters
    header = '  ' + '   '.join(labels)
    sep = '+' + '+'.join(['---'] * cols) + '+'

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f' {board[r][c]} ')
        print('|' + '|'.join(row_cells) + '|')
        print(sep)

def get_players(num_players):
    if num_players < 2 or num_players > 5:
        num_players = 2
    return CHECKERS[:num_players]

def input_column(prompt, valid_labels):
    while True:
        s = input(prompt).strip()
        if len(s) != 1:
            print("Invalid input. Enter exactly one uppercase letter corresponding to a column.")
            continue
        ch = s.upper()
        if ch not in valid_labels:
            print("Invalid column. Please enter a valid column letter shown above.")
            continue
        return ch

def drop_checker(board, col_idx, checker):
    """
    Attempts to place checker in the given column.
    Returns (placed: bool, row_idx: int or None)
    If the column is full, returns (False, None) and turn is lost.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = checker
            return True, r
    return False, None

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, r, c):
    """
    Check if the checker just placed at (r, c) creates a win.
    """
    checker = board[r][c]
    if checker == ' ':
        return False

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = 1
        total += count_in_direction(board, r, c, dr, dc, checker)
        total += count_in_direction(board, r, c, -dr, -dc, checker)
        if total >= WIN_LENGTH:
            return True
    return False

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# ---------------------- Main Game Loop ----------------------
def main():
    # Validate dimensions
    rows = max(1, ROWS)
    cols = max(1, min(COLS, 26))

    board = create_board(rows, cols)
    players = get_players(NUM_PLAYERS)
    labels = column_labels(cols)
    label_to_index = {ch: i for i, ch in enumerate(labels)}

    # Randomly choose starting player
    current_player_idx = random.randrange(len(players))

    # Initial board display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "

        # Get input column (validated as existing label)
        chosen_label = input_column(prompt, labels)
        col_idx = label_to_index[chosen_label]

        # Attempt to drop checker
        placed, row_idx = drop_checker(board, col_idx, current_checker)

        # Clear and print updated board before reporting results of move
        clear_screen()
        print_board(board)

        if not placed:
            print(f"Column {chosen_label} is full. Player {current_checker} loses the turn.")
            # Lose turn: move to next player
            current_player_idx = (current_player_idx + 1) % len(players)
            continue

        # Check for win
        if is_winning_move(board, row_idx, col_idx):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % len(players)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
