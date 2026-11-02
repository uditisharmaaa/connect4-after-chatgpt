import os
import random
import string

# ==============================
# Configuration (submission requirement: 6 rows x 7 columns, 2 players)
# ==============================
ROWS = 6
COLS = 7  # Max 26 due to A-Z labeling
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # In order

# ==============================
# Utility and Game Functions
# ==============================
def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A.. up to number of columns (max 26)
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    labels = column_labels(len(board[0]))
    # Header
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * len(labels)) + "+"
    print(header)
    print(sep)
    for r in range(len(board)):
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(board[r][c] if board[r][c] != "" else " ")
        print("| " + " | ".join(row_cells) + " |")
        print(sep)


def get_player_order(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    return PLAYER_CHECKERS[:num_players]


def get_column_from_input(prompt, cols):
    labels = column_labels(cols)
    label_set = set(labels)
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue
        # Accept lowercase but convert to uppercase
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter (e.g., A).")
            continue
        col_letter = user_input.upper()
        if col_letter not in label_set:
            print(f"Invalid column. Please choose one of: {', '.join(labels)}")
            continue
        return labels.index(col_letter), col_letter


def place_checker(board, col_idx, checker):
    # Place in the lowest available row in this column.
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True, row
    return False, None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_direction(board, start_r, start_c, dr, dc, needed=4):
    rows, cols = len(board), len(board[0])
    start_val = board[start_r][start_c]
    if start_val == " ":
        return False
    for i in range(1, needed):
        nr, nc = start_r + dr * i, start_c + dc * i
        if not in_bounds(nr, nc, rows, cols) or board[nr][nc] != start_val:
            return False
    return True


def check_win(board):
    rows, cols = len(board), len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == " ":
                continue
            for dr, dc in directions:
                if check_direction(board, r, c, dr, dc, needed=4):
                    return True, board[r][c]
    return False, None


def check_draw(board):
    # Draw if no spaces left
    for row in board:
        if " " in row:
            return False
    return True


def game_loop():
    if COLS > 26:
        raise ValueError("Maximum supported number of columns is 26 (A-Z).")

    players = get_player_order(NUM_PLAYERS)
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randint(0, len(players) - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        col_idx, col_letter = get_column_from_input(prompt, COLS)

        placed, row = place_checker(board, col_idx, checker)
        clear_screen()
        print_board(board)

        if not placed:
            print(f"Column {col_letter} is full. Turn lost.")
            # Turn is lost, move to next player
            current_player_idx = (current_player_idx + 1) % len(players)
            # Check for draw even if not placed (edge-case safety)
            if check_draw(board):
                print("It's a draw!")
                break
            continue

        # Check win after a valid placement
        won, who = check_win(board)
        if won:
            print(f"Player {who} won!")
            break

        # Check draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % len(players)


def main():
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")


if __name__ == "__main__":
    main()
