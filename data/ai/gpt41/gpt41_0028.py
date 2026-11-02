import os
import random
import string

# ========== Constants (Adjustable) ==========
BOARD_ROWS = 6
BOARD_COLS = 7     # Max 26
PLAYER_COUNT = 2   # Range 2-5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# ========== Helper Functions ==========

def clear_screen():
    os.system('clear')  # For Linux/Unix terminals

def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board in the required format."""
    cols = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    divider = '+' + '---+' * cols
    print(header)
    for row in board:
        print(divider)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(divider)

def get_valid_columns(board):
    """Returns a list of column indices that have at least one empty cell."""
    return [c for c in range(len(board[0])) if board[0][c] == ' ']

def input_column(board, player):
    cols = len(board[0])
    valid_columns = get_valid_columns(board)
    allowed_cols_labels = [string.ascii_uppercase[i] for i in valid_columns]
    while True:
        inp = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in string.ascii_uppercase[:cols]:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = string.ascii_uppercase.index(inp)
        if col not in valid_columns:
            if col >= cols:
                print("Column does not exist. Try again.")
            else:
                print("Column is full. You lose your turn!")
            return None  # Lose turn if column is full
        return col

def drop_checker(board, col, checker):
    """Places checker in the lowest available row in specified column."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Shouldn't hit this if called with a valid/available column

def check_win(board, checker):
    """Check all directions for 4 in a row."""
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Horizontal
            if c + 3 < cols and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Vertical
            if r + 3 < rows and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Diagonal down-right
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Diagonal up-right
            if r - 3 >= 0 and c + 3 < cols and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """True if top row is full."""
    return all(cell != ' ' for cell in board[0])

def next_player(cur_idx, total):
    return (cur_idx + 1) % total

def board_dimensions():
    return BOARD_ROWS, BOARD_COLS

def get_player_checker(idx):
    return CHECKERS[idx]

# ========== Main Game Function ==========

def main():
    rows, cols = board_dimensions()
    players = [get_player_checker(i) for i in range(PLAYER_COUNT)]
    board = create_board(rows, cols)

    # Randomly select starting player
    current_player_idx = random.randint(0, PLAYER_COUNT-1)
    clear_screen()
    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        # Only show loss of turn if user inputs a valid but full column
        col = input_column(board, player_checker)
        if col is not None:
            drop_checker(board, col, player_checker)
            clear_screen()
            print_board(board)

            # Check for win/draw
            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            elif check_draw(board):
                print("It's a draw!")
                break
            else:
                current_player_idx = next_player(current_player_idx, PLAYER_COUNT)
        else:
            print(f"Player {player_checker} loses turn.")
            current_player_idx = next_player(current_player_idx, PLAYER_COUNT)

if __name__ == '__main__':
    main()
