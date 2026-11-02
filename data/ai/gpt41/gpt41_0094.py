import os
import random

# ================== CONSTANTS ==================
ROWS = 6         # Number of rows in the board
COLUMNS = 7      # Number of columns in the board (Max 26)
NUM_PLAYERS = 2  # Number of players (between 2 and 5)
WIN_COUNT = 4    # Number of checkers in a row needed to win

PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

# =============== GAME BOARD METHODS ===============
def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

# =============== INPUT VALIDATION ===============
def is_valid_column_input(col_input, columns):
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    col_input = col_input.upper()
    if col_input not in COLUMN_LABELS[:columns]:
        return False
    return True

def get_free_row(board, column_index):
    # Returns the index of the lowest free row in the specified column, or -1 if it is full
    for row in reversed(range(len(board))):
        if board[row][column_index] == ' ':
            return row
    return -1

def is_board_full(board):
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            return False
    return True

# =============== WIN CHECKING ===============
def check_for_win(board, marker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == marker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == marker for i in range(WIN_COUNT)):
                return True

    # Diagonal check (top left to bottom right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == marker for i in range(WIN_COUNT)):
                return True

    # Diagonal check (bottom left to top right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == marker for i in range(WIN_COUNT)):
                return True
    return False

# =============== GAME LOOP ===============
def main():
    board = create_board(ROWS, COLUMNS)
    player_markers = PLAYER_MARKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {player_markers[current_player]} starts!\nPress Enter to begin.")
    input()

    while True:
        print_board(board)
        marker = player_markers[current_player]
        valid_input = False

        while not valid_input:
            move = input(f"Player {marker}, please enter a column: ").strip().upper()
            if not is_valid_column_input(move, COLUMNS):
                print("Invalid input. Enter a single column letter (e.g. A-G).")
                continue

            col_idx = COLUMN_LABELS.index(move)
            row_idx = get_free_row(board, col_idx)
            if row_idx == -1:
                print("Column is full! You lose your turn.")
                valid_input = True  # Lose the turn!
                continue
            else:
                board[row_idx][col_idx] = marker
                valid_input = True

                # After placing, check for win
                if check_for_win(board, marker):
                    print_board(board)
                    print(f"Player {marker} won!")
                    return

                # Check for draw
                if is_board_full(board):
                    print_board(board)
                    print("The board is full! It's a draw.")
                    return

        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
