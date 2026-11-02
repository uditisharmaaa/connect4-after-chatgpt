import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Use 2 players and 7x6 board as per submission requirement
NUM_PLAYERS = 2
BOARD_ROWS = ROWS
BOARD_COLUMNS = COLUMNS
PLAYER_CHECKERS = PLAYERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    """Create a rows x columns board filled with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Print the current board state with column labels."""
    clear_screen()
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    # Print rows with borders
    row_line = '+' + '---+' * len(board[0])
    for row in board:
        print(row_line)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(row_line)


def input_to_column(user_input):
    """Convert column letter to board index (0-based)."""
    if len(user_input) != 1:
        return None
    col = ord(user_input) - ord('A')
    if 0 <= col < BOARD_COLUMNS:
        return col
    return None


def is_valid_input(user_input, board):
    """Check if the input is a valid column letter and column is not full."""
    col = input_to_column(user_input)
    if col is None:
        return False
    # If the top row in that column is occupied, column is full
    if board[0][col] != " ":
        return False
    return True


def place_checker(board, col, checker):
    """Place a checker in the lowest available space in the column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # column full, no placement possible
    return None


def check_line(line, checker):
    """Check if line has 4 consecutive checkers for the player."""
    count = 0
    for cell in line:
        if cell == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    return False


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        if check_line(board[r], checker):
            return True

    # Check vertical
    for c in range(cols):
        col_cells = [board[r][c] for r in range(rows)]
        if check_line(col_cells, checker):
            return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            diag = [board[r + i][c + i] for i in range(WIN_LENGTH)]
            if all(cell == checker for cell in diag):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            diag = [board[r - i][c + i] for i in range(WIN_LENGTH)]
            if all(cell == checker for cell in diag):
                return True

    return False


def check_draw(board):
    """Check if the board is full (no spaces left)."""
    for row in board:
        if " " in row:
            return False
    return True


def next_player_index(current_index):
    return (current_index + 1) % NUM_PLAYERS


def main():
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        checker = PLAYER_CHECKERS[current_player]
        prompt = f"Player {checker}, please enter a column: "
        user_input = input(prompt).strip().upper()

        if not is_valid_input(user_input, board):
            # Invalid input: letter or full column
            if len(user_input) == 1 and input_to_column(user_input) is not None:
                # Column is full -> player loses turn
                current_player = next_player_index(current_player)
                continue
            else:
                # Invalid letter input, ask again (turn not lost)
                continue

        col = input_to_column(user_input)
        place = place_checker(board, col, checker)
        if place is None:
            # Column is full - player loses turn
            current_player = next_player_index(current_player)
            continue  # skip win check, next player turn

        if check_winner(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = next_player_index(current_player)


if __name__ == "__main__":
    main()
