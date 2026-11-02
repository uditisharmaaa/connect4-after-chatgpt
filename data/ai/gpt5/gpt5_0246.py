import os
import random

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # allowed: 2 to 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Ensure limits
COLS = max(1, min(COLS, 26))
NUM_PLAYERS = max(2, min(NUM_PLAYERS, len(CHECKERS)))


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board, labels):
    # Header with column letters
    print("  " + "   ".join(labels))
    # Separator line
    sep = "+" + "+".join(["---"] * len(labels)) + "+"
    for r in range(len(board)):
        print(sep)
        # Row content
        row_cells = []
        for c in range(len(labels)):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def get_valid_column_input(labels):
    # Keep asking until a valid column letter is entered
    while True:
        user_input = input("Please enter a column: ").strip()
        if not user_input:
            print("Invalid input. Enter one of:", ", ".join(labels))
            continue
        # Accept lowercase but treat as uppercase
        user_input = user_input.upper()
        if len(user_input) != 1 or user_input < "A" or user_input > labels[-1]:
            print("Invalid input. Enter one of:", ", ".join(labels))
            continue
        return labels.index(user_input)


def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r  # return the row where placed
    return None  # column full


def count_in_direction(board, start_r, start_c, dr, dc, checker):
    count = 0
    r, c = start_r, start_c
    rows = len(board)
    cols = len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win_from_cell(board, r, c, checker):
    # Check four directions: horizontal, vertical, diag1, diag2
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # Count both ways from the placed cell
        total = (
            count_in_direction(board, r, c, dr, dc, checker)
            + count_in_direction(board, r, c, -dr, -dc, checker)
            - 1  # counted center twice
        )
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    # Draw if no spaces left in top row (or anywhere)
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    labels = column_labels(COLS)
    board = create_board(ROWS, COLS)

    # Prepare players' checkers
    players = CHECKERS[:NUM_PLAYERS]

    # Random starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial screen
    clear_screen()
    print_board(board, labels)
    print(f"Player {players[current_player_idx]}, please enter a column:")

    while True:
        # Get input for current player
        col = get_valid_column_input(labels)

        # Try to drop checker
        row_placed = drop_checker(board, col, players[current_player_idx])

        # Clear and print board after the attempt
        clear_screen()
        print_board(board, labels)

        if row_placed is None:
            # Column full: player loses turn
            print(f"Column {labels[col]} is full. Player {players[current_player_idx]} loses the turn.")
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            # Check for win from the placed position
            checker = players[current_player_idx]
            if check_win_from_cell(board, row_placed, col, checker):
                print(f"Player {checker} won!")
                break

            # Check for draw
            if is_draw(board):
                print("The game is a draw.")
                break

            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

        # Prompt next turn
        print(f"Player {players[current_player_idx]}, please enter a column:")


if __name__ == "__main__":
    main()
