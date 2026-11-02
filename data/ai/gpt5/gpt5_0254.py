import os
import random

# Constants (you can change these for testing, but submission should be 6x7 with 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    labels = []
    for i in range(cols):
        labels.append(chr(ord('A') + i))
    return labels

def print_board(board):
    labels = column_labels(len(board[0]))
    # Header
    print("  " + "   ".join(labels))
    # Separator and rows
    sep = "+" + "+".join(["---"] * len(labels)) + "+"
    for r in range(len(board)):
        print(sep)
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def get_valid_input(prompt, valid_labels):
    while True:
        user_in = input(prompt).strip()
        if len(user_in) == 1 and user_in.isalpha():
            user_in = user_in.upper()
            if user_in in valid_labels:
                return user_in
        # Invalid input; ask again without losing turn
        # No explicit error message required, keep prompting
        continue

def find_row_for_column(board, col_index):
    # Start from bottom row upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return None  # Column full

def place_checker(board, col_index, checker):
    row_index = find_row_for_column(board, col_index)
    if row_index is None:
        return False  # Column full
    board[row_index][col_index] = checker
    return True

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win_for_checker(board, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                        count += 1
                    else:
                        break
                if count >= 4:
                    return True
    return False

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Sanity constraints
    cols = max(1, min(COLS, 26))
    rows = max(1, ROWS)
    num_players = max(2, min(NUM_PLAYERS, 5))
    players = CHECKERS[:num_players]

    board = create_board(rows, cols)
    labels = column_labels(cols)

    # Random starting player
    current_player_index = random.randint(0, num_players - 1)

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        current_checker = players[current_player_index]
        # Prompt
        user_label = get_valid_input(f"Player {current_checker}, please enter a column: ", labels)
        col_index = labels.index(user_label)

        # Attempt to place
        placed = place_checker(board, col_index, current_checker)

        if not placed:
            # Column full: turn lost
            clear_screen()
            print_board(board)
            # Move to next player
            current_player_index = (current_player_index + 1) % num_players
            # Continue to next turn
            continue

        # After placement, check win
        if check_win_for_checker(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next turn
        clear_screen()
        print_board(board)
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
