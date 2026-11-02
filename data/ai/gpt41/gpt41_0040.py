import os
import random
import string

# === Constants ===
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission. Can be up to 5.
PLAYER_MARKS = ["X", "O", "V", "H", "M"]

# Max supported columns: 26 (A-Z)
COLUMN_HEADERS = list(string.ascii_uppercase[:BOARD_COLS])


def clear_screen():
    os.system('clear')  # for Linux/Unix terminal


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Print column headers
    print("  " + "   ".join(COLUMN_HEADERS))
    print("+---" * BOARD_COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * BOARD_COLS + "+")


def get_valid_column_input(board):
    while True:
        col_input = input(f"Please enter a column: ").strip().upper()
        if len(col_input) == 1 and col_input in COLUMN_HEADERS:
            col = COLUMN_HEADERS.index(col_input)
            # Check if column is not full
            if board[0][col] == " ":
                return col
            else:
                print("This column is full. You lose your turn.")
                return None
        else:
            print(
                "Invalid input. Please enter a valid column letter corresponding to the board."
            )


def place_checker(board, col, mark):
    # Place in the lowest possible row in that column
    for row in reversed(range(BOARD_ROWS)):
        if board[row][col] == " ":
            board[row][col] = mark
            return row, col
    # Should not be called if column is full! But safeguard
    return None, None


def check_win(board, row, col, mark):
    # Directions: horizontal, vertical, diag (down-right), diag (down-left)
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # current checker counts as 1
        # Check in + direction
        r, c = row + dr, col + dc
        while (
            0 <= r < BOARD_ROWS
            and 0 <= c < BOARD_COLS
            and board[r][c] == mark
        ):
            count += 1
            r += dr
            c += dc
        # Check in - direction
        r, c = row - dr, col - dc
        while (
            0 <= r < BOARD_ROWS
            and 0 <= c < BOARD_COLS
            and board[r][c] == mark
        ):
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False


def check_draw(board):
    # If the very top row has any empty spaces, not a draw
    return all(cell != " " for cell in board[0])


def main():
    # Setup
    board = create_board(BOARD_ROWS, BOARD_COLS)
    player_marks = PLAYER_MARKS[:NUM_PLAYERS]
    player_names = [f"Player {mark}" for mark in player_marks]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    clear_screen()
    print_board(board)
    print(f"{player_names[current_player]} will start!")

    while not game_over:
        print()
        print_board(board)
        mark = player_marks[current_player]
        player_label = player_names[current_player]
        print(f"{player_label} ({mark}), ", end="")
        col = get_valid_column_input(board)
        if col is None:
            # Invalid due to full column; lose turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row, col_placed = place_checker(board, col, mark)
        clear_screen()
        if check_win(board, row, col_placed, mark):
            print_board(board)
            print(f"{player_label} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
