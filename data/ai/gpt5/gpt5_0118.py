import os
import random
import string

# Constants (you can change these to test different configurations)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    # Return list of labels 'A', 'B', ..., up to number of columns (max 26)
    return list(string.ascii_uppercase[:cols])

def print_board(board):
    cols = len(board[0])
    labels = column_labels(cols)
    # Print header labels
    header = "  " + "   ".join(labels)
    print(header)
    # Build separator line
    sep = "+" + "+".join(["---"] * cols) + "+"
    # Print each row
    for r in range(len(board)):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def get_valid_input(cols):
    labels = column_labels(cols)
    while True:
        user_input = input().strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            print("Please enter a column:")
            continue
        ch = user_input.upper()
        if ch not in labels:
            print("Invalid input. Please enter a valid column letter.")
            print("Please enter a column:")
            continue
        return labels.index(ch), ch

def drop_checker(board, col_index, checker):
    # Place checker in the lowest available row in given column.
    # Returns the row index where checker was placed, or None if column full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win_from(board, start_r, start_c, checker):
    # Check all directions from the last placed checker for WIN_LENGTH in a row
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = start_r + dr, start_c + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = start_r - dr, start_c - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for r in board:
        for cell in r:
            if cell == " ":
                return False
    return True

def main():
    # Basic validations for constants
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Show initial board
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_index]}, please enter a column:")

    # Game loop
    while True:
        # Get input
        col_index, col_label = get_valid_input(COLS)

        # Attempt to drop checker
        placed_row = drop_checker(board, col_index, players[current_player_index])

        # Clear and print board after the attempt
        clear_screen()
        print_board(board)

        if placed_row is None:
            # Column full, player loses turn
            print(f"Column {col_label} is full. Player {players[current_player_index]} loses the turn.")
            # Switch player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Check for win
            checker = players[current_player_index]
            if check_win_from(board, placed_row, col_index, checker):
                print(f"Player {checker} won!")
                break
            # Check for draw
            if board_full(board):
                print("It's a draw!")
                break
            # Switch player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

        # Prompt next player
        print(f"Player {players[current_player_index]}, please enter a column:")

if __name__ == "__main__":
    main()
