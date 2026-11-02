import os
import random

# CONSTANTS
ROWS = 6                # Number of rows on the board
COLS = 7                # Number of columns on the board (max 26)
NUM_PLAYERS = 2         # Number of players (between 2 and 5)
WIN_CONDITION = 4       # Number of checkers in a row needed to win
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

def clear_screen():
    """Clear the terminal screen using 'clear' command."""
    os.system('clear')

def create_board(rows, cols):
    """Create the game board as a 2D list filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current board state with column labels and separators."""
    clear_screen()
    cols = len(board[0])
    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(col_labels))
    # Print each row with separators
    for r in range(len(board)):
        print("+---" * cols + "+")
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * cols + "+")

def is_valid_column_input(col_input, cols):
    """Check if the input is a valid uppercase letter representing a column."""
    if len(col_input) != 1:
        return False
    if not ('A' <= col_input <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(col_input):
    """Convert column letter (A-G) to board column index (0-6)."""
    return ord(col_input) - ord('A')

def place_checker(board, col, checker):
    """
    Attempt to place checker in the given column.
    Returns True if placed successfully, False if column is full.
    The checker falls to the lowest empty row in the column.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col  # Return position where checker was placed
    return None  # Column full

def check_win(board, row, col, checker):
    """
    Check all directions from the last placed checker for a win condition.
    Returns True if the player has 4 in a row (horizontally, vertically, diagonally).
    """
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows, cols = len(board), len(board[0])

    for dr, dc in directions:
        count = 1  # Count includes the placed checker itself

        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    """Return True if the board has no empty space left, otherwise False."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLS)

    # Players and their checkers based on number of players
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    # Main game loop
    while True:
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input loop for valid column input
        while True:
            col_input = input(prompt).strip().upper()
            if not is_valid_column_input(col_input, COLS):
                # Invalid input (not a single uppercase letter A-G)
                continue
            col_idx = get_column_index(col_input)
            # Try to place checker; if column full, player loses turn
            placed_pos = place_checker(board, col_idx, current_checker)
            if placed_pos is None:
                # Column full - player loses turn (no re-entry)
                break
            else:
                # Valid placement made - break input loop
                break

        # If checker placed, check if player wins
        if placed_pos is not None:
            print_board(board)
            r, c = placed_pos
            if check_win(board, r, c, current_checker):
                print(f"Player {current_checker} won!")
                return
            if board_full(board):
                print("Game is a draw!")
                return
        else:
            # Column full, placed_pos None -> player loses turn
            print_board(board)

        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
