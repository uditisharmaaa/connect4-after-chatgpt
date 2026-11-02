import os
import random
import string

# ----------- CONSTANTS -----------
NUM_ROWS = 6               # Board height
NUM_COLS = 7               # Board width  (max 26)
NUM_PLAYERS = 2            # Between 2 and 5 players
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Valid checkers for up to 5 players

# ----------- FUNCTIONS -----------

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """
    Initialize an empty board filled with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """
    Display the board with appropriate formatting.
    """
    # Print column letters
    col_headers = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(col_headers)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    """
    Return a list of column indices where at least one cell is empty.
    """
    return [c for c in range(len(board[0])) if board[0][c] == ' ']

def ask_column(player_checker, valid_cols):
    """
    Prompt player for a valid column input. Keeps asking for input until valid.
    """
    valid_col_letters = [string.ascii_uppercase[c] for c in valid_cols]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in string.ascii_uppercase[:NUM_COLS]:
            print(f"Invalid input. Enter one of: {' '.join(string.ascii_uppercase[:NUM_COLS])}")
            continue
        col_idx = string.ascii_uppercase.index(col_input)
        if col_idx not in valid_cols:
            if col_idx in range(NUM_COLS):
                print("That column is full. Turn lost.")
                return None
            else:
                print(f"Column {col_input} is not on the board.")
            continue
        return col_idx

def place_checker(board, col, checker):
    """
    Place the player's checker into the chosen column.
    Return the row and column index where it landed, or None if the column is full.
    """
    for row in reversed(range(len(board))):  # Start from bottom row
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Should not happen if we check col_full beforehand

def is_within_bounds(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols

def check_for_win(board, checker):
    """
    Check all rows, columns, and diagonals for 4 in a row for the given checker.
    """
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            # Horizontal right
            if c + 3 < cols and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Vertical down
            if r + 3 < rows and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Diagonal down-right (\)
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Diagonal down-left (/)
            if r + 3 < rows and c - 3 >= 0 and all(board[r+i][c-i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    """
    Return True if the board is full and there is no winner.
    """
    return all(cell != ' ' for row in board for cell in row)

def switch_player(current_index, num_players):
    """
    Rotate to the next player index.
    """
    return (current_index + 1) % num_players

def main():
    # Game setup
    assert 2 <= NUM_PLAYERS <= 5, "Number of players must be 2..5"
    assert 1 <= NUM_COLS <= 26, "Number of columns must be 1..26"
    assert 1 <= NUM_ROWS

    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    player_names = [f"{chk}" for chk in player_checkers]

    # Randomly choose first player
    current_player_index = random.randrange(NUM_PLAYERS)
    clear_screen()
    print_board(board, NUM_COLS)
    print(f"Player {player_names[current_player_index]} starts!\n")

    # Gameplay loop
    while True:
        player_checker = player_checkers[current_player_index]
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("It's a draw! Board is full.")
            break

        # Ask for column
        col_chosen = ask_column(player_checker, valid_cols)
        clear_screen()

        if col_chosen is None:
            # Penalty for choosing a full column: lose turn
            print_board(board, NUM_COLS)
            print(f"Player {player_checker} loses the turn (column full).")
            current_player_index = switch_player(current_player_index, NUM_PLAYERS)
            continue

        # Place checker
        row, col = place_checker(board, col_chosen, player_checker)
        print_board(board, NUM_COLS)

        # Check for win
        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if check_for_draw(board):
            print("It's a draw! Board is full.")
            break

        # Next player
        current_player_index = switch_player(current_player_index, NUM_PLAYERS)

if __name__ == "__main__":
    main()
