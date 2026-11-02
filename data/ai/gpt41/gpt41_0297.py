import random
import os
import sys

# ----- CONSTANTS -----
ROWS = 6                # Number of rows
COLS = 7                # Number of columns (max 26, cols named by uppercase letters)
NUM_PLAYERS = 2         # Number of players (2-5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker for each player
CONNECT = 4             # Number of checkers in a row needed to win

# ----- FUNCTIONS -----

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create a game board initialized with whitespace."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current board state."""
    cols = len(board[0])
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    """Return a list of column indices that are not full."""
    valid = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid.append(col)
    return valid

def input_column(board, current_checker):
    """Prompt for column input, validate input, and return chosen column index (0-based)."""
    cols = len(board[0])
    valid_cols = get_valid_columns(board)
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ")
        if len(user_input) != 1 or not user_input.isupper():
            print("Invalid input! Please enter a single uppercase letter (A-G).")
            continue
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print("Invalid column! Please enter a letter within the board range.")
            continue
        if col_index not in valid_cols:
            print("That column is full! You lose your turn.")
            return None   # Player loses turn
        return col_index

def drop_checker(board, col, checker):
    """Drop checker in the selected column. Returns row index where checker landed."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None  # Column full, should not happen with proper validation

def check_direction(board, r, c, dr, dc, checker):
    """Check for CONNECT in a specific direction from (r, c)."""
    count = 0
    for i in range(CONNECT):
        rr = r + dr * i
        cc = c + dc * i
        if rr < 0 or rr >= len(board) or cc < 0 or cc >= len(board[0]):
            return False
        if board[rr][cc] != checker:
            return False
        count += 1
    return count == CONNECT

def check_win(board, last_row, last_col, checker):
    """Check if the last move makes the player win."""
    # Check all four directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # Horizontal (right)
        (1, 0),   # Vertical (down)
        (1, 1),   # Diagonal (\)
        (1, -1)   # Diagonal (/)
    ]
    for dr, dc in directions:
        # To cover all possibilities, look from -(CONNECT-1) to +(CONNECT-1)
        for i in range(-CONNECT+1, 1):
            sr = last_row + dr*i
            sc = last_col + dc*i
            if check_direction(board, sr, sc, dr, dc, checker):
                return True
    return False

def check_draw(board):
    """Returns True if the board is full (draw)."""
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

# ----- MAIN GAME FUNCTION -----
def main():
    # Use only first NUM_PLAYERS checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]

    board = create_board(ROWS, COLS)
    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS-1)
    clear_screen()
    print_board(board)
    # Game loop
    winner = None
    while True:
        checker = player_checkers[current_player]
        valid_cols = get_valid_columns(board)
        if len(valid_cols) == 0:
            if check_draw(board):
                print("It's a draw!")
                break

        # Take turn
        col_index = input_column(board, checker)
        if col_index is None:
            # Player loses turn if chosen column is full
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row_index = drop_checker(board, col_index, checker)
        clear_screen()
        print_board(board)

        # Check for win, draw
        if check_win(board, row_index, col_index, checker):
            print(f"Player {checker} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
