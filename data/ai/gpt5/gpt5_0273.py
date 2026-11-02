import os
import random
import string

# Constants (adjustable)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    # Header
    print("  " + "   ".join(letters))
    # Rows
    for r in range(len(board)):
        print("+---" * cols + "+")
        row_str = ""
        for c in range(cols):
            row_str += f"| {board[r][c]} "
        row_str += "|"
        print(row_str)
    print("+---" * cols + "+")

def get_column_input(valid_cols_set):
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Enter a single letter column (e.g., A, B, C).")
            continue
        if user_input not in valid_cols_set:
            print("Column out of range. Choose a valid column letter.")
            continue
        return user_input

def drop_checker(board, col_index, checker):
    # Place the checker in the lowest available row of the column.
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None  # Column is full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, last_r, last_c, checker):
    # Check for 4 in a row through the last placed checker.
    # Directions: (dr, dc)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Count the last placed checker
        # Check positive direction
        r, c = last_r + dr, last_c + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check negative direction
        r, c = last_r - dr, last_c - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Validate constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)
    col_letters = [string.ascii_uppercase[i] for i in range(COLS)]
    valid_cols_set = set(col_letters)

    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_index]}, you start!")

    while True:
        print(f"Player {players[current_player_index]}, please enter a column:")
        col_letter = get_column_input(valid_cols_set)
        col_index = ord(col_letter) - ord('A')

        result = drop_checker(board, col_index, players[current_player_index])

        # Clear and print the board after the attempt
        clear_screen()
        print_board(board)

        if result is None:
            # Column is full; turn is lost
            print(f"Column {col_letter} is full. Turn lost.")
            # No win check, just move to next player
            current_player_index = (current_player_index + 1) * 1 % NUM_PLAYERS
            # Check for draw (optional after a lost turn)
            if check_draw(board):
                print("It's a draw!")
                break
            continue

        last_r, last_c = result

        # Check for win
        if check_win(board, last_r, last_c, players[current_player_index]):
            print(f"Player {players[current_player_index]} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
