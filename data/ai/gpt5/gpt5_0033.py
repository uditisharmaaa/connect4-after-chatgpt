import os
import random
import string

# Constants (submission requires 6 rows, 7 cols, 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # From 2 to 5

CHECKERS = ["X", "O", "V", "H", "M"]  # In order


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)

    # Top border
    border = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(border)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(border)


def get_column_index_from_input(user_input, cols):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return None
    letters = string.ascii_uppercase[:cols]
    if user_input not in letters:
        return None
    return letters.index(user_input)


def drop_checker(board, col, checker):
    # Place checker in the lowest empty row of the given column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None  # Column full


def is_board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    nr += dr
                    nc += dc
    return False


def main():
    # Basic validations for constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]
        user_input = input(f"Player {current_checker}, please enter a column: ")

        col_index = get_column_index_from_input(user_input, COLS)
        if col_index is None:
            # Invalid input, ask again (do not switch player)
            continue

        placed_row = drop_checker(board, col_index, current_checker)
        if placed_row is None:
            # Column full, player loses the turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
