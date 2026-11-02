import os
import random
import sys

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

# Game settings/constants
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]  # In order, as specified


def clear_screen():
    # Linux/Unix terminal as per assignment
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Up to 26 columns labeled A..Z
    if cols > 26:
        raise ValueError("Maximum of 26 columns supported.")
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with column labels
    header = "  " + "   ".join(labels)
    print(header)

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def next_player_index(current, total):
    return (current + 1) % total


def get_valid_input(cols):
    labels = column_labels(cols)
    valid_set = set(labels)
    while True:
        user_in = input("Player input (column letter): ").strip()
        if not user_in:
            print("Invalid input. Please enter a column letter.")
            continue
        ch = user_in[0].upper()
        if ch in valid_set:
            return ch
        else:
            print("Invalid input. Please enter one of:", " ".join(labels))


def drop_checker(board, col_index, checker):
    """
    Attempts to place the checker in the given column.
    Returns the row index where the checker was placed, or None if column is full.
    """
    rows = len(board)
    # Start from bottom-most row moving upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return None


def check_direction(board, start_r, start_c, delta_r, delta_c, checker):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    while 0 <= r < rows and 0 <= c < cols:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += delta_r
        c += delta_c
    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal for each row
    for r in range(rows):
        if check_direction(board, r, 0, 0, 1, checker):
            return True

    # Check vertical for each column
    for c in range(cols):
        if check_direction(board, 0, c, 1, 0, checker):
            return True

    # Check diagonal down-right (top rows and leftmost cols as starts)
    # Start positions that can fit 4 in diag
    for r in range(rows):
        # from each row, start at col 0
        if check_direction(board, r, 0, 1, 1, checker):
            return True
    for c in range(1, cols):
        # from each col, start at row 0
        if check_direction(board, 0, c, 1, 1, checker):
            return True

    # Check diagonal up-right
    for r in range(rows):
        if check_direction(board, r, 0, -1, 1, checker):
            return True
    for c in range(1, cols):
        if check_direction(board, rows - 1, c, -1, 1, checker):
            return True

    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def game_loop(rows, cols, num_players):
    # Validate number of players
    if not (2 <= num_players <= 5):
        print("Number of players must be between 2 and 5.")
        sys.exit(1)

    # Prepare players' checkers
    players = CHECKERS[:num_players]

    # Create board
    board = create_board(rows, cols)

    # Randomly select first player
    current_player_idx = random.randrange(num_players)

    # Initial board print
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_idx]}, please enter a column:")

    while True:
        # Read and validate input
        col_letter = get_valid_input(cols)
        col_index = ord(col_letter) - ord('A')

        # Try to drop checker
        placed_row = drop_checker(board, col_index, players[current_player_idx])

        # Clear and print updated board each turn attempt
        clear_screen()
        print_board(board)

        if placed_row is None:
            # Column full: player loses the turn
            print(f"Column {col_letter} is full. Player {players[current_player_idx]} loses the turn.")
            # Next player's turn
            current_player_idx = next_player_index(current_player_idx, num_players)
            print(f"Player {players[current_player_idx]}, please enter a column:")
            continue

        # Check for win
        if check_win(board, players[current_player_idx]):
            print(f"Player {players[current_player_idx]} won!")
            return

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, num_players)
        print(f"Player {players[current_player_idx]}, please enter a column:")


def main():
    random.seed()  # Seed with system time or OS randomness
    game_loop(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
