import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4

# Game settings (submission requirement)
NUM_PLAYERS = 2
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Validate constants for safety
assert 1 <= ROWS <= 100, "ROWS must be positive and reasonable"
assert 1 <= COLUMNS <= MAX_COLUMNS, f"COLUMNS must be between 1 and {MAX_COLUMNS}"
assert MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS, f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}"

# Slice only the required players' checkers
PLAYERS = PLAYERS_CHECKERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    # Create board as a list of lists, row-major order, filled with spaces
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers: letters starting from 'A'
    headers = '  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    # Print rows and horizontal separators
    horizontal_line = '+' + '---+' * len(board[0])
    for r in range(len(board)):
        print(horizontal_line)
        # For each cell in the row print "| X "
        row_str = '| ' + ' | '.join(board[r]) + ' |'
        print(row_str)
    print(horizontal_line)

def get_valid_column_input(current_player):
    """Prompt player for a column letter. Repeat until valid or column full (turn lost)."""
    valid_letters = [chr(ord('A') + i) for i in range(COLUMNS)]
    while True:
        choice = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(choice) != 1:
            # invalid - length must be 1
            continue
        if choice not in valid_letters:
            continue
        col_index = ord(choice) - ord('A')
        return col_index

def place_checker(board, col, checker):
    """
    Place the checker in the lowest available row in the given column.
    Return True if placed, False if the column is full.
    """
    # iterate from bottom row upwards
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # Directions: right, down, diagonal down-right, diagonal down-left
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while in_bounds(nr, nc) and board[nr][nc] == checker:
                    count += 1
                    if count == WIN_COUNT:
                        return True
                    nr += dr
                    nc += dc
    return False

def check_draw(board):
    # If any space in top row is empty, not a draw yet
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    # Select random starting player index
    current_player_index = random.randint(0, NUM_PLAYERS-1)
    
    print_board(board)

    while True:
        checker = PLAYERS[current_player_index]
        col = get_valid_column_input(checker)

        placed = place_checker(board, col, checker)
        if not placed:
            # Column full => player loses the turn
            # Simply advance to next player without placing
            # So print the board without change and continue
            print_board(board)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        print_board(board)

        # Check win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("Game ends in a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
