import os
import random
import string

# Constants (you can change these for testing)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
WIN_LENGTH = 4

CHECKERS_ALL = ["X", "O", "V", "H", "M"]
CHECKERS = CHECKERS_ALL[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Header letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))
    # Top border
    print("+" + "---+" * cols)
    # Rows
    for r in range(len(board)):
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+" + "---+" * cols)


def column_letter_to_index(letter):
    letter = letter.upper()
    if len(letter) != 1:
        return None
    if letter < 'A' or letter > 'Z':
        return None
    idx = ord(letter) - ord('A')
    return idx


def valid_column_input(s, cols):
    idx = column_letter_to_index(s)
    if idx is None:
        return False
    return 0 <= idx < cols


def drop_checker(board, col_index, checker):
    # Place checker in the lowest empty cell of the column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return (r, col_index)
    return None  # column full


def check_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r = start_r
    c = start_c
    while 0 <= r < rows and 0 <= c < cols:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += dr
        c += dc
    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        if check_direction(board, r, 0, 0, 1, checker):
            return True

    # Vertical
    for c in range(cols):
        if check_direction(board, 0, c, 1, 0, checker):
            return True

    # Diagonal down-right (\)
    # Start from top row and leftmost column
    for c in range(cols):
        if check_direction(board, 0, c, 1, 1, checker):
            return True
    for r in range(1, rows):
        if check_direction(board, r, 0, 1, 1, checker):
            return True

    # Diagonal up-right (/)
    for c in range(cols):
        if check_direction(board, rows - 1, c, -1, 1, checker):
            return True
    for r in range(rows - 2, -1, -1):
        if check_direction(board, r, 0, -1, 1, checker):
            return True

    return False


def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Basic checks for constraints
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return

    board = create_board(ROWS, COLS)

    # Randomly choose first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Game loop
    while True:
        print_board(board)
        current_checker = CHECKERS[current_player_index]

        # Prompt user input
        user_input = ""
        while True:
            print(f"Player {current_checker}, please enter a column:")
            user_input = input().strip().upper()
            if valid_column_input(user_input, COLS):
                break
            else:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")

        col = column_letter_to_index(user_input)

        # Try to place checker
        placed_pos = drop_checker(board, col, current_checker)

        # After action, print updated board
        print_board(board)

        if placed_pos is None:
            # Column full: turn lost
            print(f"Column {user_input} is full. Turn lost.")
            # Next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Continue to next turn
            continue

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
