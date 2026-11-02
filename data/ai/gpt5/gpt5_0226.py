import os
import random
import sys
from typing import List

# ==============================
# Configuration (Submission requires 6x7 and 2 players)
# ==============================
ROWS = 6
COLS = 7          # Must be <= 26 (A..Z)
NUM_PLAYERS = 2   # Between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"]  # In order; we will slice by NUM_PLAYERS

# ==============================
# Utility functions
# ==============================

def clear_screen():
    """
    Clear the terminal screen. Uses 'clear' as per Linux/Unix requirement.
    """
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """
    Create a board with given dimensions initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]):
    """
    Print the board with column headers labeled A.. and cell borders.
    The board is printed top row first, as in the example.
    """
    rows = len(board)
    cols = len(board[0])

    # Header letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal border for each row
    h_border = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(h_border)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("|" + "|".join(f" {cell} " for cell in row_cells) + "|")
    print(h_border)


def get_valid_column_letter(prompt: str, max_cols: int) -> str:
    """
    Prompt the user until they provide a valid uppercase column letter within range.
    Invalid inputs (numbers, out-of-range letters, multiple chars, blank) are rejected.
    Returns a single uppercase letter A.. corresponding to a valid column.
    """
    valid_letters = [chr(ord('A') + i) for i in range(max_cols)]
    while True:
        user_in = input(prompt).strip().upper()
        if len(user_in) == 1 and user_in in valid_letters:
            return user_in
        # Inform user and reprompt (turn is not lost for invalid inputs)
        print(f"Invalid input. Please enter one of: {', '.join(valid_letters)}")


def column_index_from_letter(letter: str) -> int:
    """
    Convert column letter (A..) to zero-based index.
    """
    return ord(letter) - ord('A')


def is_column_full(board: List[List[str]], col: int) -> bool:
    """
    A column is full if the top cell is not empty.
    """
    return board[0][col] != " "


def drop_checker(board: List[List[str]], col: int, token: str) -> bool:
    """
    Drop a checker into the specified column for the given token.
    The checker occupies the lowest available space in that column.
    Returns True if placed, False if column is full.
    """
    if is_column_full(board, col):
        return False
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return True
    return False  # Should not reach here if top wasn't full


def has_won(board: List[List[str]], token: str) -> bool:
    """
    Check for 4 in a row for the given token horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0])
    needed = 4

    # Horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == token:
                count += 1
                if count >= needed:
                    return True
            else:
                count = 0

    # Vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == token:
                count += 1
                if count >= needed:
                    return True
            else:
                count = 0

    # Diagonal down-right (\)
    for r in range(rows):
        for c in range(cols):
            # Check only if enough space to the bottom-right
            if r + needed - 1 < rows and c + needed - 1 < cols:
                if all(board[r + k][c + k] == token for k in range(needed)):
                    return True

    # Diagonal up-right (/)
    for r in range(rows):
        for c in range(cols):
            # Check only if enough space to the top-right
            if r - (needed - 1) >= 0 and c + needed - 1 < cols:
                if all(board[r - k][c + k] == token for k in range(needed)):
                    return True

    return False


def is_draw(board: List[List[str]]) -> bool:
    """
    A draw occurs if the board fills up (no spaces in the top row) and nobody has won.
    """
    return all(cell != " " for cell in board[0])


def select_starting_player(num_players: int) -> int:
    """
    Randomly select a starting player index in [0, num_players-1].
    """
    return random.randint(0, num_players - 1)


def next_player_index(current: int, total: int) -> int:
    """
    Get the next player's index in round-robin fashion.
    """
    return (current + 1) % total


# ==============================
# Main game loop
# ==============================

def main():
    # Validate configuration bounds
    cols = max(1, min(COLS, 26))  # Cap at 26 columns (A..Z)
    rows = max(1, ROWS)
    num_players = max(2, min(NUM_PLAYERS, 5))
    player_tokens = TOKENS[:num_players]

    board = create_board(rows, cols)
    current_player = select_starting_player(num_players)

    while True:
        clear_screen()
        print_board(board)
        current_token = player_tokens[current_player]
        prompt = f"Player {current_token}, please enter a column: "
        col_letter = get_valid_column_letter(prompt, cols)
        col_index = column_index_from_letter(col_letter)

        # Try to drop checker; if column is full, player loses the turn
        if not drop_checker(board, col_index, current_token):
            print(f"Column {col_letter} is full. Turn lost.")
            current_player = next_player_index(current_player, num_players)
            # Small pause-like behavior: reprint board on next iteration
            continue

        # After a successful move, check win/draw
        if has_won(board, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = next_player_index(current_player, num_players)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print("\nGame interrupted.")
        sys.exit(0)
