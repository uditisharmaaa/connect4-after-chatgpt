import os
import random
import string

# ------------ Constants -------------
ROWS = 6              # Number of rows in the board
COLS = 7              # Number of columns in the board (max 26)
NUM_PLAYERS = 2       # Number of players (2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Symbols used for players
WIN_LENGTH = 4        # Number of checkers in a row needed to win


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """Create and return a board with the given rows and columns."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the game board to the console."""
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    sep = "+" + "---+" * cols
    print(header)
    print(sep)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(sep)


def get_valid_columns(board):
    """Returns a list of column indices where a checker can be placed."""
    valid = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid.append(col)
    return valid


def get_player_move(board, current_player):
    """Prompt the player for a column selection, validate, and return the selected column index."""
    valid_columns = get_valid_columns(board)
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]

    while True:
        move = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(move) != 1:
            print("Please enter a single column letter.")
            continue
        if move not in valid_letters:
            print("Invalid column. Please enter a valid column letter.")
            continue
        col = valid_letters.index(move)
        if col not in valid_columns:
            print("This column is full. You lose your turn.")
            return None
        return col


def place_checker(board, col, checker):
    """Place a checker in the specified column. Returns row where it was placed, or None if not placed."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None


def check_winner(board, row, col, checker):
    """Check all directions from (row, col) for WIN_LENGTH checkers in a row."""
    def count_direction(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        return count

    directions = [ (0, 1),   # Horizontal right
                   (1, 0),   # Vertical down
                   (1, 1),   # Diagonal down-right
                   (1, -1)   # Diagonal down-left
                 ]
    for r_step, c_step in directions:
        count = 1
        count += count_direction(r_step, c_step)
        count += count_direction(-r_step, -c_step)
        if count >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    """Returns True if the board is full (draw)."""
    return all(cell != " " for cell in board[0])  # Top row filled


def game():
    # --- Setup ---
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    col_letters = string.ascii_uppercase[:COLS]

    # Randomly select starting player
    current_idx = random.randrange(NUM_PLAYERS)
    clear_screen()
    print_board(board)

    while True:
        checker = players[current_idx]
        col = get_player_move(board, checker)
        if col is None:
            # Invalid (full) column, lose turn
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        row = place_checker(board, col, checker)

        clear_screen()
        print_board(board)

        if check_winner(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    game()
