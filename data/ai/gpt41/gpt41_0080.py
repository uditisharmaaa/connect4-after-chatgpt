import os
import random
import sys

# --- CONSTANTS ---

# Dimensions (rows x columns)
ROWS = 6
COLUMNS = 7

# Maximum players: 2-5
NUM_PLAYERS = 2

# Allow for up to 26 columns (A-Z)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

# --- FUNCTIONS ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board():
    """Creates and returns a 2D board with given ROWS and COLUMNS."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the Connect 4 board in specified format."""
    clear_screen()
    # Print header
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

def get_next_open_row(board, col):
    """Returns the lowest empty row index for the given column, or None if full."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            return row
    return None

def is_valid_column(input_col):
    """Checks whether the input is a valid column label on the board."""
    return input_col in COLUMN_LABELS

def is_column_full(board, col):
    """Checks if the specified column is full."""
    return board[0][col] != ' '

def place_checker(board, row, col, checker):
    """Places the player's checker in the board at [row][col]."""
    board[row][col] = checker

def check_win(board, checker):
    """Checks if the provided checker has a sequence of 4 in any direction."""
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Diagonal down-right (\)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Diagonal up-right (/)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Checks if the board is fully filled and no player has won."""
    for row in board:
        if ' ' in row:
            return False
    return True

def get_player_input(player_checker, board):
    """Prompts and validates player input."""
    prompt = f"Player {player_checker}, please enter a column: "
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter ONE letter corresponding to a column.")
            continue
        if not is_valid_column(user_input):
            print(f"Invalid column. Please choose from: {', '.join(COLUMN_LABELS)}")
            continue
        col = COLUMN_LABELS.index(user_input)
        if is_column_full(board, col):
            print("Column is full. You lose your turn!")
            return None
        return col

def main():
    # 1. Initialize
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS-1)
    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts!")

    game_over = False

    while not game_over:
        print_board(board)
        col = get_player_input(CHECKERS[current_player], board)
        if col is None:
            # Lose turn if column is full
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row = get_next_open_row(board, col)
        if row is not None:
            place_checker(board, row, col, CHECKERS[current_player])
        else:
            # Should not occur, as already checked
            print("Unexpected error: could not place checker.")
            sys.exit(1)

        if check_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Alternate player
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
