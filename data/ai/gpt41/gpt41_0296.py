import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # Maximum allowed columns (A-Z)
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # As per submission instructions
WIN_CONDITION = 4

# --- Utility functions ---

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers
    headers = '  ' + '   '.join(string.ascii_uppercase[:cols])
    sep = '+' + ('---+' * cols)
    print(headers)
    print(sep)
    for row in board:
        line = '| ' + ' | '.join(row) + ' |'
        print(line)
        print(sep)

def valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    if inp.upper() not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_column_index(inp):
    return string.ascii_uppercase.index(inp.upper())

def is_column_full(board, col_idx):
    return all(row[col_idx] != ' ' for row in board)

def place_checker(board, col_idx, checker):
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # Should only happen if column full

def board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win_from(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down right
        (1, -1),  # Diagonal down left
    ]
    for dr, dc in directions:
        count = 1
        # Check one way
        r, c = row+dr, col+dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # And the opposite way
        r, c = row-dr, col-dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

# --- Main game loop ---

def main():
    # Set up the board and player checkers
    board = create_board(ROWS, COLUMNS)
    checkers = CHECKERS[:NUM_PLAYERS]
    player_names = [f"Player {ch}" for ch in checkers]

    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    winner = None
    while True:
        player_checker = checkers[current_player]
        player_name = player_names[current_player]
        print(f"{player_name}, please enter a column:")

        # Read and validate input
        while True:
            inp = input().strip()
            if not valid_column_input(inp, COLUMNS):
                print("Invalid input. Please enter a valid column letter (A-{}):".format(string.ascii_uppercase[COLUMNS-1]))
                continue
            col_idx = get_column_index(inp)
            if is_column_full(board, col_idx):
                print("Column is full! Turn lost.")
                break  # Lose the turn
            # Valid input and space available; continue
            pos = place_checker(board, col_idx, player_checker)
            clear_screen()
            print_board(board)
            if check_win_from(board, *pos, player_checker):
                winner = player_name
            break  # Go to next player or end game

        # End game if win or full board (draw)
        if winner:
            print(f"{player_name} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
