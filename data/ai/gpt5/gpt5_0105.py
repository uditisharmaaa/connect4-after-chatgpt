import os
import random
import sys

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # Must be <= 26 (A..Z)
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]  # In order, first NUM_PLAYERS used


def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def clear_screen():
    # Clear the terminal screen (Unix/Linux/Mac)
    os.system('clear')


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    header_letters = []
    for i in range(cols):
        header_letters.append(chr(ord('A') + i))
    print("  " + "   ".join(header_letters))

    # Top border
    print("+" + ("---+" * cols))

    # Each row
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+" + ("---+" * cols))


def is_valid_column_letter(letter, cols):
    if len(letter) != 1:
        return False
    if not letter.isalpha():
        return False
    letter = letter.upper()
    if letter < 'A' or ord(letter) >= ord('A') + cols:
        return False
    return True


def letter_to_col(letter):
    return ord(letter.upper()) - ord('A')


def get_next_open_row(board, col):
    rows = len(board)
    # Start from bottom row and go up
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None  # Column is full


def drop_checker(board, row, col, checker):
    board[row][col] = checker


def check_win(board, row, col, checker):
    # Check 4 in a row in all directions that pass through (row, col)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1

        # Move in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Move in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def board_is_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Basic validations for constants
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)

    # Initialize game
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board
    print_board(board)

    while True:
        current_checker = players[current_player_index]

        # Prompt for input
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip()

        # Validate input (retry until valid letter in range)
        while not is_valid_column_letter(user_input, COLS):
            print("Invalid input. Please enter a valid column letter (e.g., A, B, C):")
            user_input = input().strip()

        col = letter_to_col(user_input)

        # Try to place checker
        row = get_next_open_row(board, col)
        if row is None:
            # Column full: lose the turn
            print_board(board)
            print(f"Column {user_input.upper()} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Place the checker
        drop_checker(board, row, col, current_checker)

        # Print updated board
        print_board(board)

        # Check for a win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_is_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
