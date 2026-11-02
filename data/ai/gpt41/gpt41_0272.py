import os
import random
import sys

# ==== CONSTANTS ====
NUM_ROWS = 6           # Board rows
NUM_COLS = 7           # Board cols, max 26 (A-Z)
PLAYERS = 2            # Between 2 and 5

CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# ==== BOARD FUNCTIONS ====

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * NUM_COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * NUM_COLS)

# ==== GAME LOGIC ====

def get_valid_columns(board):
    valid_cols = []
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            valid_cols.append(col)
    return valid_cols

def get_column_index(input_str):
    input_str = input_str.strip().upper()
    if len(input_str) != 1:
        return None
    if input_str in COLUMN_LABELS:
        return COLUMN_LABELS.index(input_str)
    return None

def place_checker(board, col, checker):
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col  # Return the location for win checking
    return None  # Column full

def check_win(board, row, col, checker):
    def count_dir(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    directions = [(0,1), (1,0), (1,1), (1,-1)]  # horiz, vert, diag\, diag/
    for dr, dc in directions:
        count = 1  # count the placed checker
        count += count_dir(dr, dc)
        count += count_dir(-dr, -dc)
        if count >= 4:
            return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(NUM_COLS))

# ==== MAIN GAME LOOP ====

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = PLAYERS
    checkers = CHECKERS[:num_players]
    # Pick random first player
    curr_player = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        curr_checker = checkers[curr_player]
        # Prompt for move
        while True:
            try:
                user_input = input(f'Player {curr_checker}, please enter a column: ')
            except (EOFError, KeyboardInterrupt):
                print('\nGame exited.')
                sys.exit(0)

            col_idx = get_column_index(user_input)
            if col_idx is None or not (0 <= col_idx < NUM_COLS):
                print(f"Invalid input! Please enter a column label from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
                continue
            # Check column full
            if board[0][col_idx] != ' ':
                print("Column is full! You lose your turn.")
                # Lose turn
                row_col = None
                break
            else:
                row_col = place_checker(board, col_idx, curr_checker)
                break

        print_board(board)

        # If column wasn't full, else lose turn
        if row_col:
            row, col = row_col
            # Check win
            if check_win(board, row, col, curr_checker):
                print(f'Player {curr_checker} won!')
                break
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        curr_player = (curr_player + 1) % num_players

if __name__ == '__main__':
    main()
