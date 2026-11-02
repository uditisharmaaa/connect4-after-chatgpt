import os
import random
import string

# ====== CONFIGURABLE CONSTANTS ======
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set to 2 for submission

# ====== BOARD FUNCTIONS ======

def create_board(rows, cols):
    """Create a board initialized with whitespaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board):
    """Display the board with column labels."""
    cols = len(board[0])
    # Column headers
    col_labels = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(col_labels))
    # Top border
    print("+" + "---+" * cols)
    # Rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

# ====== GAMEPLAY FUNCTIONS ======

def get_next_open_row(board, col):
    """Return the lowest empty row in the given column, or None if full."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None

def validate_input(choice, board):
    """Check if input is a single valid column letter and if column exists."""
    cols = len(board[0])
    if len(choice) != 1 or choice not in string.ascii_uppercase[:cols]:
        return False
    return True

def is_column_full(board, col):
    """Check if the specified column is full."""
    return board[0][col] != " "

def check_win(board, row, col, checker):
    """Check all directions for a connect-4 win starting from last placed checker."""
    def count(dx, dy):
        r, c = row+dx, col+dy
        cnt = 0
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            cnt += 1
            r += dx
            c += dy
        return cnt

    # Horizontal
    total = 1 + count(0, 1) + count(0, -1)
    if total >= 4:
        return True
    # Vertical
    total = 1 + count(1, 0) + count(-1, 0)
    if total >= 4:
        return True
    # Diagonal /
    total = 1 + count(-1, 1) + count(1, -1)
    if total >= 4:
        return True
    # Diagonal \
    total = 1 + count(1, 1) + count(-1, -1)
    if total >= 4:
        return True

    return False

def check_draw(board):
    """Check if all columns are full and no winner."""
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(player_checker, board):
    """Prompt player until a valid column is chosen or forfeits turn if full."""
    cols = len(board[0])
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not validate_input(choice, board):
            print("Invalid input. Please enter a valid column letter (A-{})".format(string.ascii_uppercase[cols-1]))
            continue
        col = string.ascii_uppercase.index(choice)
        if is_column_full(board, col):
            print("Column is full! You lose your turn.")
            return None  # Forfeit turn
        return col

def random_starting_player(num_players):
    return random.randint(0, num_players-1)

# ====== MAIN GAME LOOP ======

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player = random_starting_player(NUM_PLAYERS)
    player_checkers = CHECKERS[:NUM_PLAYERS]

    clear_screen()
    print_board(board)

    while True:
        player_checker = player_checkers[current_player]
        col = get_player_input(player_checker, board)
        
        if col is None:
            # Forfeit turn due to full column
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row = get_next_open_row(board, col)
        if row is not None:
            board[row][col] = player_checker
        else:
            # Should not happen due to above check, but just in case
            print("Unexpected error: column", col, "is full!")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        clear_screen()
        print_board(board)

        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break
        elif check_draw(board):
            print("Game is a draw!")
            break
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
