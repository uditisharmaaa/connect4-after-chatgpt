import os
import random
import string

# ------------ CONSTANTS ------------ #

# Board dimensions
ROWS = 6
COLUMNS = 7  # max 26
MAX_COLUMNS = 26

# Player settings
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set as required; for final submission, keep as 2

# Win condition
TO_WIN = 4

# ------------ HELPER FUNCTIONS ------------ #

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    """Creates a 2D board with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current game board."""
    columns = len(board[0])
    # Print column letters
    header = '  ' + '   '.join(string.ascii_uppercase[:columns])
    print(header)
    print('+' + '---+' * columns)
    for row in board:
        print('|' + '|'.join(' {:1} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * columns)

def get_valid_column_input(board):
    """Prompts user for input and validates column choice."""
    columns = len(board[0])
    valid_columns = string.ascii_uppercase[:columns]
    while True:
        user_input = input().strip().upper()
        # Input must be a single uppercase letter within the range
        if len(user_input) == 1 and user_input in valid_columns:
            col = valid_columns.index(user_input)
            # Check at least one empty space
            if board[0][col] == ' ':
                return col
            else:
                print("Column is full! You lose your turn.")
                return None  # Turn lost if full
        else:
            print(f"Invalid input. Please enter a valid column ({valid_columns[0]}-{valid_columns[-1]}):")

def place_checker(board, col, checker):
    """Places a checker in the specified column."""
    rows = len(board)
    # start from bottom row and go up
    for r in reversed(range(rows)):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col  # row and column where placed
    # Should not reach here if checked before, but return None if full
    return None, None

def check_direction(board, start_row, start_col, d_row, d_col, checker):
    """Check a direction from a start position for TO_WIN in a row."""
    count = 0
    rows = len(board)
    cols = len(board[0])

    row, col = start_row, start_col

    # Go backward first
    while (0 <= row < rows) and (0 <= col < cols) and board[row][col] == checker:
        count += 1
        row -= d_row
        col -= d_col

    # Reset to original and go forward
    row, col = start_row + d_row, start_col + d_col
    while (0 <= row < rows) and (0 <= col < cols) and board[row][col] == checker:
        count += 1
        row += d_row
        col += d_col

    return count >= TO_WIN

def check_win(board, row, col, checker):
    """Checks whether the current move wins."""
    # Directions: (dr, dc) = (row direction, col direction)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1)   # diag down-left
    ]
    for d_row, d_col in directions:
        if check_direction(board, row, col, d_row, d_col, checker):
            return True
    return False

def board_full(board):
    """Checks if the board is full."""
    return all(cell != ' ' for cell in board[0])

# ------------ MAIN GAME FUNCTION ------------ #

def main():
    board = create_board(ROWS, COLUMNS)
    player_tokens = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    clear_screen()
    print_board(board)

    moves_played = 0
    max_moves = ROWS * COLUMNS
    winner = None

    while moves_played < max_moves:
        checker = player_tokens[current_player_idx]
        print(f"Player {checker}, please enter a column:")

        col = get_valid_column_input(board)
        if col is None:
            # Lose turn if column is full according to rules.
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        row, _ = place_checker(board, col, checker)
        moves_played += 1

        clear_screen()
        print_board(board)

        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            winner = checker
            break

        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    if not winner and board_full(board):
        print("It's a draw!")

if __name__ == "__main__":
    main()
