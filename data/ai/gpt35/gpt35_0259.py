import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # set between 2 and 5 as required
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players
CHECKERS = CHECKERS[:NUM_PLAYERS]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A, B, C ...
    col_headers = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print('  ' + '   '.join(col_headers))
    for r in range(len(board)):
        print('+' + '---+' * len(board[0]))
        row_str = '| ' + ' | '.join(board[r]) + ' |'
        print(row_str)
    print('+' + '---+' * len(board[0]))

def get_column_index(input_str, columns):
    if len(input_str) != 1 or input_str not in string.ascii_uppercase[:columns]:
        return -1
    return string.ascii_uppercase.index(input_str)

def is_valid_move(board, col):
    return board[0][col] == ' '

def place_checker(board, col, checker):
    """
    Places the checker into the lowest available spot in the given column.
    Assumes the move is valid.
    Returns the row index where the checker was placed.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # should never get here if move was validated

def is_board_full(board):
    return all(cell != ' ' for cell in board[0])

def check_line_win(line, checker):
    count = 0
    for c in line:
        if c == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    return False

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal at row
    if check_line_win(board[row], checker):
        return True

    # Check vertical at col
    vertical_line = [board[r][col] for r in range(rows)]
    if check_line_win(vertical_line, checker):
        return True

    # Check diagonal (top-left to bottom-right)
    diag1 = []
    start_row = row
    start_col = col
    # Move to top-leftmost
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    # Collect diag elements
    r, c = start_row, start_col
    while r < rows and c < cols:
        diag1.append(board[r][c])
        r += 1
        c += 1
    if check_line_win(diag1, checker):
        return True

    # Check diagonal (bottom-left to top-right)
    diag2 = []
    start_row = row
    start_col = col
    # Move to bottom-leftmost
    while start_row < rows - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    # Collect diag elements
    r, c = start_row, start_col
    while r >= 0 and c < cols:
        diag2.append(board[r][c])
        r -= 1
        c += 1
    if check_line_win(diag2, checker):
        return True

    return False

def get_player_input(player_checker, board):
    cols = len(board[0])
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        col = get_column_index(user_input, cols)
        if col == -1:
            # invalid column letter
            continue
        if not is_valid_move(board, col):
            # column full
            # According to spec: "If the column is already completely filled with checkers,
            # the turn is invalid and the player loses the turn."
            # So print nothing and return None
            return None
        return col

def main():
    board = create_board(ROWS, COLUMNS)

    current_player_idx = random.randint(0, NUM_PLAYERS -1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player_idx]
        col = get_player_input(checker, board)
        if col is None:
            # player loses turn
            current_player_idx = (current_player_idx +1) % NUM_PLAYERS
            continue
        row = place_checker(board, col, checker)
        print_board(board)
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        if is_board_full(board):
            print("Draw!")
            break
        current_player_idx = (current_player_idx +1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
