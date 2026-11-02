import os
import random
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Choose how many players will play (must be between 2 and 5)
NUM_PLAYERS = 2

# The available marks for players in play order.
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']


# =========================
# Utility functions
# =========================
def clear_screen():
    """
    Clear the console. The assignment requires os.system('clear').
    We'll try 'clear' first and attempt 'cls' as a fallback for Windows.
    """
    # Required by the prompt
    ret = os.system('clear')
    # Fallback (useful if someone runs it on Windows)
    if ret != 0:
        os.system('cls')


def create_board(rows, cols):
    """
    Create an empty board represented as a 2D list filled with ' ' (space).
    board[r][c] refers to row r and column c, with r=0 at the top.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board, players, current_player_idx):
    """
    Print the board with column labels and current player information.
    """
    print("Connect 4")
    print(f"Players: " + ", ".join(f"{i+1}:{players[i]}" for i in range(len(players))))
    print(f"Current turn: Player {current_player_idx + 1} ({players[current_player_idx]})")
    print()

    # Print column labels
    print("  " + " ".join(COLUMN_LABELS))

    # Print rows from top to bottom
    for r in range(len(board)):
        row_str = [board[r][c] for c in range(len(board[0]))]
        print("| " + " ".join(row_str))

    print()  # Blank line after the board


def col_from_label(label):
    """
    Convert a column label like 'A'..'G' (case-insensitive) to a column index 0..6.
    Return None if invalid.
    """
    if not label or len(label) != 1:
        return None
    label = label.upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None


def is_valid_location(board, col):
    """
    A move is valid if the top cell of the given column is empty (i.e., the column is not full).
    """
    return board[0][col] == ' '


def get_next_open_row(board, col):
    """
    Given a column, find the lowest empty row in that column.
    Return the row index, or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None


def drop_piece(board, row, col, mark):
    """
    Place a player's mark into the board at (row, col).
    """
    board[row][col] = mark


def is_draw(board):
    """
    The game is a draw if the top row has no empty spaces (i.e., no valid moves left).
    """
    return all(cell != ' ' for cell in board[0])


def check_win_from(board, row, col, mark):
    """
    Check for a 4-in-a-row that includes the cell (row, col) with the given mark.
    We check in four directions: horizontal, vertical, and two diagonals.
    """
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    def count_in_direction(dr, dc):
        """
        Count continuous marks starting from (row, col) in both + and - directions.
        Include the starting cell.
        """
        count = 1

        # Check the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == mark:
            count += 1
            r += dr
            c += dc

        # Check the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == mark:
            count += 1
            r -= dr
            c -= dc

        return count

    for dr, dc in directions:
        if count_in_direction(dr, dc) >= 4:
            return True
    return False


def get_player_input(players, current_player_idx):
    """
    Prompt the current player for input.
    Accepts:
      - A single letter A-G (case-insensitive) to choose a column
      - 'Q' to quit the game
    Returns:
      - ('quit', None) if player chooses to quit
      - ('move', col_index) for a valid column
    """
    mark = players[current_player_idx]
    while True:
        user_in = input(f"Player {current_player_idx + 1} ({mark}), choose column A-G (or Q to quit): ").strip()
        if not user_in:
            print("Please enter a column label A-G or Q to quit.")
            continue

        if user_in.upper() == 'Q':
            return ('quit', None)

        col = col_from_label(user_in)
        if col is None:
            print("Invalid input. Please enter a single letter A-G.")
            continue

        return ('move', col)


def main():
    # Validate NUM_PLAYERS and setup players
    if not (2 <= NUM_PLAYERS <= 5):
        print(f"NUM_PLAYERS={NUM_PLAYERS} is invalid. It must be between 2 and 5.")
        sys.exit(1)

    players = PLAYER_MARKS[:NUM_PLAYERS]

    # Create the board
    board = create_board(ROWS, COLS)

    # Choose a random starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Main game loop
    while True:
        clear_screen()
        print_board(board, players, current_player_idx)

        action, value = get_player_input(players, current_player_idx)

        if action == 'quit':
            print("Game ended by player. Goodbye!")
            break

        col = value

        # Validate that the chosen column is not full
        if not is_valid_location(board, col):
            print(f"Column {COLUMN_LABELS[col]} is full. Press Enter to choose again.")
            input()
            continue

        # Find the next open row and drop the piece
        row = get_next_open_row(board, col)
        mark = players[current_player_idx]
        drop_piece(board, row, col, mark)

        # Check for a win
        if check_win_from(board, row, col, mark):
            clear_screen()
            print_board(board, players, current_player_idx)
            print(f"Player {current_player_idx + 1} ({mark}) wins! Congratulations!")
            break

        # Check for a draw
        if is_draw(board):
            clear_screen()
            print_board(board, players, current_player_idx)
            print("It's a draw! No more valid moves.")
            break

        # Switch to the next player (cyclic)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
