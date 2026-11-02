import os
import random
import string

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26
PLAYER_COUNT = 2  # Allowed: 2..5

# Checker symbols for up to 5 players, in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Validation of constants
if not (2 <= PLAYER_COUNT <= 5):
    raise ValueError("PLAYER_COUNT must be between 2 and 5.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26.")


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)

    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def get_column_index_from_input(user_input, cols):
    if len(user_input) != 1:
        return None
    ch = user_input.upper()
    letters = string.ascii_uppercase[:cols]
    if ch in letters:
        return letters.index(ch)
    return None


def prompt_for_column(current_checker, cols):
    while True:
        try:
            user_in = input(f"Player {current_checker}, please enter a column: ").strip()
        except EOFError:
            # Treat EOF as invalid; continue prompting
            continue
        col_idx = get_column_index_from_input(user_in, cols)
        if col_idx is None:
            print("Invalid input. Please enter a valid column letter.")
            continue
        return col_idx


def place_checker(board, col_idx, checker):
    rows = len(board)
    # Start from bottom row, place in first empty slot
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r
    return None  # Column full


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    # Draw if no spaces left
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Initialize players and board
    players = CHECKERS[:PLAYER_COUNT]
    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_idx = random.randrange(len(players))

    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_idx]

        # Prompt for move
        col_idx = prompt_for_column(current_checker, COLS)

        # Try to place the checker
        row_placed = place_checker(board, col_idx, current_checker)
        if row_placed is None:
            # Column full: turn lost
            print("Column is full. Turn is invalid and is lost. Press Enter to continue...")
            try:
                input()
            except EOFError:
                pass
            current_idx = (current_idx + 1) % len(players)
            clear_screen()
            print_board(board)
            continue

        # After a valid placement, check for win/draw
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % len(players)
        clear_screen()
        print_board(board)


if __name__ == "__main__":
    main()
