import os
import random
import sys

# ---------- CONSTANTS ----------
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # can set between 2 and 5
WIN_COUNT = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]
EMPTY_CELL = ' '

# ---------- FUNCTIONS ----------

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = '  ' + '   '.join(COLUMN_LABELS)
    print(header)
    # Print top border
    print('+' + '---+' * NUM_COLS)
    # Print rows
    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print('+' + '---+' * NUM_COLS)

def get_valid_column(board, player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in COLUMN_LABELS:
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        col = COLUMN_LABELS.index(col_input)
        if board[0][col] != EMPTY_CELL:
            print("That column is full. Turn lost!")
            return None  # Lose turn
        return col

def get_next_open_row(board, col):
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == EMPTY_CELL:
            return row
    return None

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY_CELL:
                return False
    return True

def check_win(board, checker):
    # Horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Positive diagonal (/)
    for r in range(WIN_COUNT - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Negative diagonal (\)
    for r in range(NUM_ROWS - WIN_COUNT + 1):
        for c in range(NUM_COLS - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def main():
    # Set up game
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    # Main game loop
    while True:
        player_checker = player_checkers[current_player]
        col = get_valid_column(board, player_checker)
        if col is None:
            # Current player loses turn due to full column
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row = get_next_open_row(board, col)
        if row is not None:
            board[row][col] = player_checker
        else:
            # This should never happen due to earlier check, but safeguard
            print("Unexpected error: column is full.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        print_board(board)

        # Check win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check draw
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
