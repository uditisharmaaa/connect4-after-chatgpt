import os
import random
import string

# ====== CONSTANTS ======
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26  # for letter labeling, from 'A' to 'Z'
NUM_PLAYERS = 2  # Set from 2 to 5

PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']

# Truncate/check input constraints
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
assert 1 <= NUM_COLS <= MAX_COLS, f"Number of columns must be 1 to {MAX_COLS}"

# ====== GAME LOGIC ======
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    col_letters = [string.ascii_uppercase[i] for i in range(cols)]
    # Print column headers
    print()
    print('  ' + '   '.join(col_letters))
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def input_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    c = input_str.upper()
    if c < 'A' or c >= chr(ord('A') + cols):
        return False
    return True

def get_available_row(board, col):
    # Return the row index where checker will fall, or None if column full
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    
    # Horizontal
    for r in range(rows):
        for c in range(cols-3):
            if (board[r][c] == checker and
                board[r][c+1] == checker and
                board[r][c+2] == checker and
                board[r][c+3] == checker):
                return True
    # Vertical
    for r in range(rows-3):
        for c in range(cols):
            if (board[r][c] == checker and
                board[r+1][c] == checker and
                board[r+2][c] == checker and
                board[r+3][c] == checker):
                return True
    # Diagonal (down-right)
    for r in range(rows-3):
        for c in range(cols-3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True
    # Diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols-3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True
    return False

def main():
    # Initialize
    board = create_board(NUM_ROWS, NUM_COLS)
    checkers = PLAYER_MARKERS[:NUM_PLAYERS]
    players = list(range(NUM_PLAYERS))
    current_player = random.choice(players)
    clear_screen()
    print_board(board)

    while True:
        checker = checkers[current_player]
        # Prompt
        while True:
            inp = input(f"Player {checker}, please enter a column: ").strip().upper()
            if not input_valid_column(inp, NUM_COLS):
                print("Invalid input. Please enter a valid column letter (A to {}).".format(chr(ord('A')+NUM_COLS-1)))
                continue
            col = ord(inp) - ord('A')
            available_row = get_available_row(board, col)
            if available_row is None:
                print("Column is full. You lose your turn!")
                available_row = None
            break

        if available_row is not None:
            # Place checker
            board[available_row][col] = checker

        clear_screen()
        print_board(board)

        # Check for win
        if available_row is not None and check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        if available_row is not None:
            # Normal rotate
            current_player = (current_player + 1) % NUM_PLAYERS
        # else, leave current_player unchanged (turn lost due to full column)

if __name__ == '__main__':
    main()
