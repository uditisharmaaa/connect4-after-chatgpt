import os
import random
import string

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to between 2 and 5 to support more players if desired
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create an empty board as a list of lists."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels
    col_labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(col_labels)
    # Print separator
    print("+" + "---+" * cols)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def random_first_player(num_players):
    return random.randint(0, num_players - 1)

def get_valid_columns(board):
    """Returns a list of column indices that are not full."""
    cols = len(board[0])
    valid = []
    for col in range(cols):
        if board[0][col] == " ":
            valid.append(col)
    return valid

def get_column_input(board):
    """Prompt for column until input is valid."""
    cols = len(board[0])
    valid_cols = get_valid_columns(board)
    col_letters = string.ascii_uppercase[:cols]
    valid_letters = [col_letters[c] for c in valid_cols]
    while True:
        col_input = input(f"Please enter a column ({'/'.join(col_letters)}): ").strip().upper()
        if len(col_input) != 1 or col_input not in col_letters:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_index = col_letters.index(col_input)
        if col_index not in valid_cols:
            print("Column full or not allowed. Try another column.")
            continue
        return col_index

def make_move(board, col, checker):
    """
    Place checker in lowest available row in given column.
    Returns the row index where placed, or None if column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    """Check a line (delta_row, delta_col direction) for 4-in-a-row."""
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_row, start_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def is_winner(board, row, col, checker):
    """Check if placing at (row, col) makes checker win."""
    # Directions: (dr, dc)
    directions = [
        (0, 1),   # Horizontal (right)
        (1, 0),   # Vertical (down)
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        # Count checkers in both directions from the point, including this one
        count = 1
        # Forward direction
        count += check_direction(board, row + dr, col + dc, dr, dc, checker)
        # Backward direction
        count += check_direction(board, row - dr, col - dc, -dr, -dc, checker)
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Game is draw if all cells in top row are occupied."""
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random_first_player(NUM_PLAYERS)

    print_board(board)
    print(f"Player {players[current_player]} starts!")

    while True:
        checker = players[current_player]
        print_board(board)
        print(f"Player {checker}, it's your turn.")
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("The board is full. The game is a draw!")
            break

        col = get_column_input(board)
        row = make_move(board, col, checker)
        if row is None:
            # This shouldn't happen due to validation, but handle anyway
            print("This column is full. You lost your turn!")
            pass  # According to rules, player loses turn

        else:
            if is_winner(board, row, col, checker):
                print_board(board)
                print(f"Player {checker} won!")
                break
            elif is_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
