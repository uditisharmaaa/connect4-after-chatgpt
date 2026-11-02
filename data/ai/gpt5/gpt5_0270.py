import os
import random

# Constants (as required for submission)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Can be between 2 and 5

# Player markers in order
MARKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    cols = len(board[0])
    # Header letters
    header_letters = []
    for i in range(cols):
        header_letters.append(chr(ord('A') + i))
    print("  " + "   ".join(header_letters))
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(len(board)):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))

def in_bounds_col(col_letter):
    if len(col_letter) != 1:
        return False
    if not ('A' <= col_letter <= chr(ord('A') + COLS - 1)):
        return False
    return True

def get_col_index(col_letter):
    return ord(col_letter) - ord('A')

def find_row_to_place(board, col_index):
    # Find from bottom up
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return None

def check_win(board, marker):
    rows = len(board)
    cols = len(board[0])
    target = 4

    # Horizontal
    for r in range(rows):
        for c in range(cols - target + 1):
            ok = True
            for k in range(target):
                if board[r][c + k] != marker:
                    ok = False
                    break
            if ok:
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - target + 1):
            ok = True
            for k in range(target):
                if board[r + k][c] != marker:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal down-right
    for r in range(rows - target + 1):
        for c in range(cols - target + 1):
            ok = True
            for k in range(target):
                if board[r + k][c + k] != marker:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal up-right
    for r in range(target - 1, rows):
        for c in range(cols - target + 1):
            ok = True
            for k in range(target):
                if board[r - k][c + k] != marker:
                    ok = False
                    break
            if ok:
                return True

    return False

def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    if COLS > 26:
        print("Maximum number of columns is 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return

    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_marker = MARKERS[current_player_index]
        prompt_range = "A-" + chr(ord('A') + COLS - 1)
        user_input = None

        # Input validation loop (only for invalid input format/range)
        while True:
            print(f"Player {current_marker}, please enter a column:")
            raw = input().strip().upper()
            if in_bounds_col(raw):
                user_input = raw
                break
            else:
                print(f"Invalid input. Please enter a column letter between {prompt_range}.")

        col_index = get_col_index(user_input)
        row_index = find_row_to_place(board, col_index)

        if row_index is None:
            # Column full: turn lost
            clear_screen()
            print_board(board)
            print(f"Column {user_input} is full. Turn lost.")
            # Next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Place checker
        board[row_index][col_index] = current_marker

        # Check for win
        if check_win(board, current_marker):
            clear_screen()
            print_board(board)
            print(f"Player {current_marker} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
