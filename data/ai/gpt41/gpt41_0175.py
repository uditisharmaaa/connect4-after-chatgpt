import os
import random
import string

# ====== Global Constants ======
NUM_ROWS = 6
NUM_COLS = 7
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Maximum 5 players supported
NUM_PLAYERS = 2  # Required by assignment
WIN_COUNT = 4

COLUMN_LABELS = list(string.ascii_uppercase)[:NUM_COLS]

# ====== Board Functions ======

def create_board(rows, cols):
    """Initialize board with whitespaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board in the required format, with column labels."""
    os.system('clear')  # For Unix/Linux
    header = '  ' + '   '.join(COLUMN_LABELS)
    print(header)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(row))

def is_valid_column(input_col):
    """Check if input_col is a valid column label."""
    return input_col in COLUMN_LABELS

def get_column_index(col_label):
    """Convert column label to column index."""
    try:
        return COLUMN_LABELS.index(col_label)
    except ValueError:
        return -1

def is_column_full(board, col):
    """Check if a column is already full."""
    return board[0][col] != " "

def drop_checker(board, col, checker):
    """Place checker in chosen column, at the lowest available row."""
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column is full

def board_full(board):
    """Check if the board is full (draw state)."""
    return all(cell != " " for cell in board[0])

# ====== Win Checking Functions ======

def check_winner(board, row, col, checker):
    """Check for WIN_COUNT in a row from (row, col) in all directions."""
    directions = [
        (1, 0),   # vertical
        (0, 1),   # horizontal
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        if count_consecutive(board, row, col, dr, dc, checker) + \
           count_consecutive(board, row, col, -dr, -dc, checker) - 1 >= WIN_COUNT:
            return True
    return False

def count_consecutive(board, row, col, dr, dc, checker):
    """Count consecutive checkers in (dr, dc) direction."""
    count = 0
    r, c = row, col
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

# ====== Input and Validation Functions ======

def ask_move(board, current_checker):
    """Get a validated move from the player."""
    while True:
        move = input(f"Player {current_checker}, please enter a column: ").strip()
        if len(move) == 1 and move.isalpha():
            move = move.upper()
            if is_valid_column(move):
                col_idx = get_column_index(move)
                if not is_column_full(board, col_idx):
                    return col_idx
                else:
                    print("That column is full! You lose your turn.")
                    return None
            else:
                print("Invalid column! Please enter a valid column label.")
        else:
            print("Invalid input! Please enter a single column letter.")

# ====== Main Game Function ======

def main():
    # Prepare game settings
    board = create_board(NUM_ROWS, NUM_COLS)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    start_player = random.randint(0, NUM_PLAYERS - 1)
    player_idx = start_player
    print_board(board)
    print(f"Player {checkers[player_idx]} starts!")

    while True:
        current_checker = checkers[player_idx]

        move = ask_move(board, current_checker)
        if move is None:
            # Player loses the turn if the column is full
            player_idx = (player_idx + 1) % NUM_PLAYERS
            continue

        place = drop_checker(board, move, current_checker)
        if place is None:
            # Shouldn't reach here due to validation, but just in case
            print("Error: Could not place checker, column full.")
            player_idx = (player_idx + 1) % NUM_PLAYERS
            continue

        print_board(board)

        row, col = place
        if check_winner(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        player_idx = (player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
